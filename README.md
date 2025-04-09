# Fraud Detection System

This project implements an end-to-end fraud detection system using machine learning. The system processes transaction data, trains a fraud detection model, and generates reports using Gemini Gen AI.

## Project Structure

```
fraud-detection/
│
├── notebooks/                           # Jupyter notebooks for development
│   ├── EDA_and_Preprocessing.ipynb      # Exploratory Data Analysis & Preprocessing
│   ├── Model_Training.ipynb             # Model training and evaluation
│   └── Model_Deployment.ipynb           # Model deployment to .pkl
│
├── scripts/                             # Processing and simulation scripts
│   ├── preprocessing_pipeline.py        # Data preprocessing pipeline
│   └── fraud_simulation.py              # Fraud prediction and report generation
│
├── model/                               # Trained models
│   └── model.pkl                        # Serialized fraud detection model
│
└── aws_bucket/                          # AWS S3 bucket structure
    ├── input/                           # New transaction data for processing
    ├── processed/                       # Processed data from pipeline
    └── output/                          # Generated fraud reports
```

## Workflow Overview

1. **Data Preparation**:
   - Raw data is preprocessed (cleaning, transformation, encoding)
   - EDA performed to understand data characteristics

2. **Model Training**:
   - Model trained on historical transaction data
   - Serialized as `model.pkl` for deployment

3. **AWS Deployment**:
   - New data uploaded to `input/` folder in S3 bucket
   - EC2 and EMR instances launched for processing
   - PySpark processes the data using the deployed model

4. **Processing Pipeline**:
   - `preprocessing_pipeline.py` processes new data
   - Results stored in `processed/` folder

5. **Fraud Simulation & Reporting**:
   - `fraud_simulation.py` makes predictions using the model
   - Generates reports with Gemini Gen AI
   - Reports saved in `output/` folder

## Setup Instructions

### Prerequisites
- Python 3.8+
- AWS account with S3, EC2, and EMR access
- Required Python packages (see requirements.txt)

### Deployment Steps

1. Upload model and scripts to AWS:
   ```bash
   aws s3 cp model/model.pkl s3://fraudetection/model/
   aws s3 cp scripts/ s3://fraudetection/scripts/ --recursive
   ```

2. Launch EC2 and EMR instances:
   ```bash
   # Configure your instances as needed
   ```

3. Process new data:
   ```bash
   spark-submit --deploy-mode cluster s3://fraudetection/scripts/preprocessing_pipeline.py
   ```

4. Generate fraud report:
   ```bash
   python3 fraud_simulation.py --input processed/ --output output/
   ```

## Script Details

### `preprocessing_pipeline.py`
- Performs data cleaning and transformation
- Handles missing values and feature engineering
- Outputs processed data ready for prediction

### `fraud_simulation.py`
- Loads the trained model
- Makes predictions on processed data
- Generates fraud analysis report using Gemini Gen AI

## Model Information
- Algorithm: [Specify your model type, e.g., Random Forest, XGBoost]
- Features used: [List important features]
- Performance metrics: [Include accuracy, precision, recall, etc.]

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
