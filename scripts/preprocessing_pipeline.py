from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofweek, hour, datediff, to_date
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.ml import Pipeline

# Start Spark session
spark = SparkSession.builder.appName("FraudDetectionPreprocessing").getOrCreate()

# Load raw data from S3
s3_input_path = "s3://frauddetection-bucket/input/raw_data.csv"
df = spark.read.csv(s3_input_path, header=True, inferSchema=True)

# Drop unnecessary columns
drop_columns = ['Unnamed: 0', 'cc_num', 'merchant', 'first', 'last', 'street', 'city', 'state', 'zip', 
                'lat', 'long', 'city_pop', 'job', 'trans_num', 'unix_time', 'merch_lat', 'merch_long', 'dob']
df = df.drop(*drop_columns)

# Convert timestamp column to date format
df = df.withColumn("trans_date_trans_time", to_date(col("trans_date_trans_time")))

# Extract hour and weekday
df = df.withColumn("trans_hour", hour(col("trans_date_trans_time")))
df = df.withColumn("trans_day_of_week", dayofweek(col("trans_date_trans_time")))

# One-hot encode categorical columns using pipeline
indexers = [StringIndexer(inputCol=column, outputCol=column+"_index", handleInvalid="keep") 
            for column in ["category", "gender"]]
encoders = [OneHotEncoder(inputCol=column+"_index", outputCol=column+"_vec") 
            for column in ["category", "gender"]]

pipeline = Pipeline(stages=indexers + encoders)
df = pipeline.fit(df).transform(df)

# Drop original categorical and intermediate index columns
df = df.drop("category", "gender", "category_index", "gender_index", "trans_day_of_week", "trans_date_trans_time")

# Save processed data back to S3 in Parquet format
s3_output_path = "s3://frauddetection-bucket/processed/processed_data.parquet"
df.write.mode("overwrite").parquet(s3_output_path)

print("✅ Processed dataset saved as Parquet to S3!")

# Stop Spark session
spark.stop()
