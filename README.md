<div align="center">

🛡️ End-to-End Fraud Detection System on AWS
</div>

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

📖 1. Business Context & Project Goal
In the digital economy, financial fraud poses a significant threat to businesses and consumers alike, leading to billions of dollars in losses annually. Proactively identifying and preventing fraudulent transactions is paramount for maintaining customer trust and financial stability.

The Goal: This project addresses this challenge by designing and deploying a scalable, end-to-end fraud detection pipeline on the AWS cloud. The system ingests raw transaction data, processes it at scale using Apache Spark, predicts fraudulent activity with a machine learning model, and generates insightful reports using Gemini Gen AI.

This repository is presented as a complete case study, as if I were a Data Engineer tasked with building a production-ready fraud detection system for a financial services company.

🏛️ 2. The Technical Solution: A Cloud-Based ML Pipeline
To handle the high volume and velocity of financial data, I architected a robust, cloud-native pipeline using AWS services. This ensures the solution is scalable, automated, and capable of processing data in large batches.

Data Lake & Storage (AWS S3): An S3 bucket serves as the central data lake, with a structured hierarchy for raw input data (input/), cleaned data (processed/), and final fraud reports (output/).

Large-Scale Data Processing (AWS EMR & Spark): An EMR cluster running Apache Spark is used to execute the preprocessing_pipeline.py script. This allows for distributed, parallel processing of massive transaction datasets, ensuring the ETL process is fast and efficient.

Machine Learning Inference: The fraud_simulation.py script loads a pre-trained machine learning model (model.pkl) to score the processed transactions and identify potential fraud.

Automated Reporting (Gemini Gen AI): After prediction, the simulation script leverages the Gemini API to synthesize the results into human-readable, actionable reports for the risk analysis team.

🧠 3. Model Insights & Key Findings
A Random Forest Classifier was trained on the dataset due to its robustness and ability to handle imbalanced classes.

Performance Metrics: The model was evaluated on its ability to correctly identify fraudulent transactions while minimizing false positives.

Precision: High precision ensures that when the model flags a transaction as fraudulent, it is highly likely to be correct.

Recall: High recall ensures that the model successfully identifies a large percentage of all actual fraudulent transactions.

Key Predictive Features: The most influential features in detecting fraud were found to be:

Transaction Amount

Transaction Category (e.g., online shopping, travel)

Time of Day

Customer Age

☁️ 4. AWS Deployment & Execution Guide
This section provides the technical steps to deploy and run the entire pipeline on AWS.

✅ Step 1: IAM & S3 Bucket Setup
Create an IAM Role for EC2/EMR with the following policies: AmazonS3FullAccess, AmazonEMRFullAccessPolicy_v2, AmazonEC2FullAccess, CloudWatchLogsFullAccess.

Create and configure the S3 bucket:

# Create the bucket
aws s3 mb s3://fraudetection

# Create the folder structure
aws s3api put-object --bucket fraudetection --key input/
aws s3api put-object --bucket fraudetection --key processed/
aws s3api put-object --bucket fraudetection --key output/
aws s3api put-object --bucket fraudetection --key model/
aws s3api put-object --bucket fraudetection --key scripts/
aws s3api put-object --bucket fraudetection --key logs/

Upload project files to S3:

aws s3 cp model/model.pkl s3://fraudetection/model/
aws s3 cp scripts/ s3://fraudetection/scripts/ --recursive

📊 Step 2: Launch the EMR Cluster
Launch a 3-node EMR cluster. Ensure you have an EC2 Key Pair (your-key) created in your AWS account.

aws emr create-cluster \
    --name "FraudDetectionCluster" \
    --release-label emr-6.9.0 \
    --applications Name=Spark Name=Hadoop \
    --ec2-attributes KeyName=your-key,InstanceProfile=EMR_EC2_DefaultRole \
    --instance-type m5.xlarge --instance-count 3 \
    --use-default-roles \
    --log-uri s3://fraudetection/logs/

🔄 Step 3: Execute the Pipeline on EMR
Connect to the EMR master node via SSH and run the processing and prediction jobs.

# 1. Run the Spark preprocessing job
spark-submit --deploy-mode cluster \
    s3://fraudetection/scripts/preprocessing_pipeline.py \
    --input s3://fraudetection/input/ \
    --output s3://fraudetection/processed/

# 2. Run the fraud detection and reporting job
python3 s3://fraudetection/scripts/fraud_simulation.py \
    --model s3://fraudetection/model/model.pkl \
    --input s3://fraudetection/processed/ \
    --output s3://fraudetection/output/

🧹 Step 4: Cleanup
After the jobs are complete, terminate the EMR cluster and delete the S3 bucket to avoid ongoing charges.

# Terminate the cluster (replace with your cluster ID)
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXX

# Empty and delete the S3 bucket
aws s3 rm s3://fraudetection --recursive
aws s3 rb s3://fraudetection


## 🤝 Contributing

Pull requests and feedback are welcome! Please open issues for major changes or suggestions.

## 📜 License
[MIT License](https://choosealicense.com/licenses/mit/)


