import joblib
import pandas as pd
import boto3
import time
import re
import google.generativeai as genai
from pyspark.sql import SparkSession

# Step 1: Start Spark and Load Parquet
spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

print("📦 Reading processed Parquet data from HDFS...")
df_spark = spark.read.parquet("hdfs:///user/hadoop/processed/processed_data.parquet")

# Step 2: Convert to Pandas DataFrame
print("🔁 Converting to Pandas DataFrame...")
df = df_spark.toPandas()

# Step 3: Load pipeline model from S3
print("⬇️ Downloading model pipeline from S3...")
s3 = boto3.client('s3')
bucket_name = 'frauddetection-bucket'
model_key = 'models/model_pipeline.joblib'
s3.download_file(bucket_name, model_key, 'model_pipeline.joblib')

print("🧠 Loading model pipeline...")
pipeline = joblib.load('model_pipeline.joblib')
print("✅ Pipeline loaded successfully.")

# Step 4: Predict fraud (pipeline handles preprocessing)
print("🔎 Running predictions...")
df['Fraud_Prediction'] = pipeline.predict(df)
print("✅ Predictions complete.")

# Step 5: Generate AI Report with Gemini
print("📄 Generating AI summary report...")

genai.configure(api_key="YOUR_GOOGLE_API_KEY")
gemini = genai.GenerativeModel("gemini-1.5-pro")

# Basic summary
total_txns = len(df)
fraud_count = (df['Fraud_Prediction'] == 1).sum()
fraud_percent = round((fraud_count / total_txns) * 100, 2)

summary = f"""
Fraud Detection Report:

Total Transactions: {total_txns}
🚨 Fraudulent Transactions Detected: {fraud_count}
📈 Fraud Percentage: {fraud_percent}%
"""

short_summary = summary[:1500]

def generate_in_chunks(model, text, max_len=500):
    chunks = [text[i:i + max_len] for i in range(0, len(text), max_len)]
    responses = []
    for i, chunk in enumerate(chunks):
        try:
            print(f"🤖 Generating AI chunk {i+1}/{len(chunks)}...")
            res = model.generate_content(f"Please analyze this fraud report:\n{chunk}")
            responses.append(res.text)
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error in chunk {i+1}: {e}")
            responses.append("Error")
    return "\n".join(responses)

ai_output = generate_in_chunks(gemini, short_summary)

def clean_text(text):
    return re.sub(r"\\", "", text)

final_report = clean_text(ai_output)

# Step 6: Upload results to S3
print("📤 Uploading report and predictions to S3...")

# Upload AI-generated report
s3.put_object(Bucket=bucket_name, Key="output/fraud_analysis_report.txt", Body=final_report.encode("utf-8"))

# Save CSV with predictions and upload
df.to_csv("fraud_predictions.csv", index=False)
s3.upload_file("fraud_predictions.csv", bucket_name, "output/fraud_predictions.csv")

print("✅ Done! Report and predictions uploaded to S3.")
 yeh model+ai report
