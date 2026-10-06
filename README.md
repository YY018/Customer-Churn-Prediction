# Customer Churn Prediction

A machine learning project that predicts customer churn using the IBM Telco Customer Churn dataset.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Joblib

## Machine Learning Models

- Logistic Regression
- Random Forest
- Gradient Boosting
- Tuned Gradient Boosting

## Final Model Performance

| Metric | Score |
|---|---:|
| Accuracy | 79.91% |
| Precision | 65.74% |
| Recall | 50.80% |
| F1 Score | 57.32% |
| ROC-AUC | 84.60% |

## Features

The model uses customer demographics, tenure, services, contract type, payment method, and billing information to predict customer churn probability.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
