# Fraud Detection with Apache Spark & AWS

This project implements a scalable **fraud detection system** using **Apache Spark on AWS EMR**.  
It processes large financial transaction datasets, applies machine learning models, and stores predictions and reports in **AWS S3**.

## 🚀 Workflow:
1. **Upload Data & Model to S3** – Store validation dataset & trained model.
2. **Launch AWS EMR Cluster** – Set up Apache Spark for distributed processing.
3. **Load Data & Model in Spark** – Use PySpark for scalable ML inference.
4. **Run Predictions using UDFs** – Apply the ML model across large datasets.
5. **Save Results & Reports to S3** – Store predictions & generate AI-powered fraud analysis reports.

## 📦 Technologies Used:
- **Apache Spark (PySpark)**
- **AWS S3, EMR, Boto3**
- **Scikit-learn / XGBoost**
- **Python, Pandas, Joblib**

## 📂 Project Structure:
```
📦 fraud-detection-spark
 ┣ 📂 notebooks/            # Jupyter notebooks for local testing
 ┣ 📂 scripts/              # PySpark scripts for AWS EMR
 ┣ 📂 models/               # Trained ML models (.pkl) 
 ┣ 📂 data/                 # Sample dataset (validation set)
 ┣ 📂 reports/              # AI-generated fraud reports
 ┣ 📜 README.md             # Project documentation
```

## 🔧 Setup & Usage:
1. Clone the repository:  
   ```sh
   git clone https://github.com/yashvisharma1204/fraud-detection-spark.git
   ```
2. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```
3. Upload dataset & model to AWS S3:
   ```sh
   aws s3 cp validation_data.csv s3://your-bucket-name/data/
   aws s3 cp fraud_detection_model.pkl s3://your-bucket-name/models/
   ```
4. Run predictions using Spark on AWS EMR.

## 📜 License:
MIT License
```
