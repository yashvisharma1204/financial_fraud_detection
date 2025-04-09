# 🛡️ Fraud Detection System

An end-to-end fraud detection system using machine learning and AWS cloud infrastructure. It ingests transaction data, preprocesses it, predicts fraud using a trained model, and generates insightful reports using Gemini Gen AI.

---

## 📁 Project Structure (GitHub Repository Overview)

```
fraud-detection/
│
├── notebooks/                           # Jupyter notebooks for exploration & prototyping
│   ├── EDA_and_Preprocessing.ipynb      # Data cleaning, EDA, and preprocessing
│   ├── Model_Training.ipynb             # Model training, evaluation, metrics
│   └── Model_Deployment.ipynb           # Exporting model to .pkl for deployment
│
├── scripts/                             # Core scripts for production workflows
│   ├── preprocessing_pipeline.py        # End-to-end preprocessing script for raw data
│   └── fraud_simulation.py              # Loads model, predicts fraud, generates reports
│
├── model/                               # Stores trained ML models
│   └── model.pkl                        # Serialized fraud detection model
│
└── aws_bucket/                          # Represents AWS S3 bucket layout
    ├── input/                           # Uploads new raw transactions
    ├── processed/                       # Processed data post-cleaning
    └── output/                          # Fraud prediction reports
```

---

## 🚀 End-to-End Workflow

1. **Data Ingestion** → via `aws_bucket/input/`
2. **Preprocessing** → `preprocessing_pipeline.py` (via Spark on EMR)
3. **Prediction** → `fraud_simulation.py` uses `model.pkl`
4. **Report Generation** → Output to `aws_bucket/output/`

---

## ☁️ AWS Deployment Documentation (Core Focus)

### 1. ✅ IAM & Permissions

- Create a role with:
  - `AmazonS3FullAccess`
  - `AmazonEMRFullAccessPolicy_v2`
  - `AmazonEC2FullAccess`
  - `CloudWatchLogsFullAccess`
- Use the role in EC2/EMR setup for full operational access.

---

### 2. 🪣 S3 Bucket Configuration

Create S3 bucket and folder hierarchy:

```bash
aws s3 mb s3://fraudetection

# Optional: enforce access policy
aws s3api put-bucket-policy --bucket fraudetection --policy file://bucket-policy.json
```

**bucket-policy.json** (adjust `YOUR_ACCOUNT_ID`):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:role/EMR_EC2_DefaultRole"
    },
    "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::fraudetection", "arn:aws:s3:::fraudetection/*"]
  }]
}
```

Upload required files:

```bash
aws s3 cp model/model.pkl s3://fraudetection/model/
aws s3 cp scripts/ s3://fraudetection/scripts/ --recursive
```

---

### 3. 📊 Launch EMR Cluster

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

🧾 **Recommended Configs**:
- EMR 6.9.0 with Spark 3.3.1
- 1 Master, 2 Worker Nodes
- EC2 Key Pair required for SSH

---

### 4. 🔄 Run Data Pipeline & Simulation

**From EMR Master Node:**

```bash
# Run Preprocessing
spark-submit --deploy-mode cluster \
  s3://fraudetection/scripts/preprocessing_pipeline.py \
  --input s3://fraudetection/input/ \
  --output s3://fraudetection/processed/

# Run Fraud Detection
python3 fraud_simulation.py \
  --model s3://fraudetection/model/model.pkl \
  --input s3://fraudetection/processed/ \
  --output s3://fraudetection/output/
```

---

### 5. 🧹 Cleanup Resources

```bash
# Stop EMR
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXX

# Delete S3 data
aws s3 rm s3://fraudetection --recursive
aws s3 rb s3://fraudetection
```

---

## 🔍 Script Highlights

### `preprocessing_pipeline.py`
- Cleans and transforms raw transaction data
- Handles missing values, encodes features
- Outputs to S3 `processed/` directory

### `fraud_simulation.py`
- Loads trained `model.pkl`
- Predicts fraud
- Uses Gemini Gen AI to generate human-readable reports

---

## 🧠 Model Insights
- **Model**: e.g., Random Forest / XGBoost/Decsion Tree/Logistic Regression
- **Metrics**: Accuracy, Precision, Recall,Confusion Matrix
- **Top Features**: Amount, Category,Age , Time,Gender

---

## 🤝 Contributing

Pull requests and feedback are welcome! Please open issues for major changes or suggestions.

## 📜 License
[MIT License](https://choosealicense.com/licenses/mit/)

