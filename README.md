<div align="center">

# 🛡️ End-to-End Fraud Detection System on AWS

<p align="center">
  <img src="https://img.shields.io/badge/-AWS-232F3E?logo=amazonaws&logoColor=white" alt="AWS"/>
  <img src="https://img.shields.io/badge/-Apache%20Spark-E25A1C?logo=apachespark&logoColor=white" alt="Apache Spark"/>
  <img src="https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/-Scikit--learn-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/-RandomForest-228B22?logo=tree&logoColor=white" alt="Random Forest"/>
  <img src="https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/-Gemini%20Gen%20AI-4285F4?logo=google&logoColor=white" alt="Gemini Gen AI"/>
</p>

</div> 

---

## 📖 1. Business Context & Project Goal  
In today’s digital economy, **financial fraud** is a growing threat, costing businesses and consumers billions annually. Proactively detecting and preventing fraudulent transactions is essential for **customer trust** and **financial stability**.  

**The Goal**: Build and deploy a **scalable, end-to-end fraud detection pipeline** on AWS.  
- Ingests raw transaction data  
- Processes it at scale using **Apache Spark**  
- Predicts fraud with a **machine learning model**  
- Generates **actionable reports** with Gemini Gen AI  

This repository is structured as a **real-world case study**, simulating the role of a Data Engineer tasked with delivering a production-ready fraud detection system.  

---

## 🏛️ 2. Technical Solution: A Cloud-Native ML Pipeline  
To handle the **high volume & velocity** of financial data, the pipeline is fully cloud-native, leveraging AWS services for **scalability, automation, and efficiency**.  

### ⚙️ Architecture Overview  
- **Data Lake & Storage (AWS S3):**  
  Centralized data lake with folders for raw data (`input/`), processed data (`processed/`), reports (`output/`), models, scripts, and logs.  

- **Large-Scale Processing (AWS EMR + Spark):**  
  Distributed ETL via `preprocessing_pipeline.py` for cleaning & feature engineering.  

- **Fraud Prediction (ML Inference):**  
  `fraud_simulation.py` loads a **Random Forest Classifier** (`model.pkl`) to detect suspicious transactions.  

- **Automated Reporting (Gemini Gen AI):**  
  Converts prediction outputs into **human-readable fraud reports** for risk teams.  

---

## 🧠 3. Model Insights & Key Findings  
The **Random Forest Classifier** was chosen for robustness and handling imbalanced data.  

**Key Metrics:**  
- 🎯 **Precision:** Ensures flagged fraud cases are highly reliable  
- 🔍 **Recall:** Captures the majority of fraudulent transactions  
- ⚖️ **Balance:** Minimized false positives while maximizing detection  

**Top Predictive Features:**  
- Transaction Amount  
- Transaction Category (e.g., shopping, travel)  
- Time of Day  
- Customer Age  

---

## ☁️ 4. AWS Deployment & Execution Guide  

### ✅ Step 1: IAM & S3 Setup  
```bash
# Create bucket
aws s3 mb s3://fraudetection

# Folder structure
aws s3api put-object --bucket fraudetection --key input/
aws s3api put-object --bucket fraudetection --key processed/
aws s3api put-object --bucket fraudetection --key output/
aws s3api put-object --bucket fraudetection --key model/
aws s3api put-object --bucket fraudetection --key scripts/
aws s3api put-object --bucket fraudetection --key logs/

# Upload files
aws s3 cp model/model.pkl s3://fraudetection/model/
aws s3 cp scripts/ s3://fraudetection/scripts/ --recursive
````

### 📊 Step 2: Launch EMR Cluster

```bash
aws emr create-cluster \
  --name "FraudDetectionCluster" \
  --release-label emr-6.9.0 \
  --applications Name=Spark Name=Hadoop \
  --ec2-attributes KeyName=your-key,InstanceProfile=EMR_EC2_DefaultRole \
  --instance-type m5.xlarge --instance-count 3 \
  --use-default-roles \
  --log-uri s3://fraudetection/logs/
```

### 🔄 Step 3: Run Pipeline Jobs

```bash
# 1. Preprocessing (Spark ETL)
spark-submit --deploy-mode cluster \
  s3://fraudetection/scripts/preprocessing_pipeline.py \
  --input s3://fraudetection/input/ \
  --output s3://fraudetection/processed/

# 2. Fraud Detection + Reporting
python3 s3://fraudetection/scripts/fraud_simulation.py \
  --model s3://fraudetection/model/model.pkl \
  --input s3://fraudetection/processed/ \
  --output s3://fraudetection/output/
```

### 🧹 Step 4: Cleanup

```bash
# Terminate cluster
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXX

# Remove S3 bucket
aws s3 rm s3://fraudetection --recursive
aws s3 rb s3://fraudetection
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests.

---

## 📜 License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).



