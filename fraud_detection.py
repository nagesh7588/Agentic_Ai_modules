# Fraud Detection Module
# Detects fraudulent transactions using anomaly detection

import joblib

class FraudDetector:
    def __init__(self):
        self.model = joblib.load('fraud_detection_model.pkl')

    def detect(self, transaction_details: dict) -> dict:
        import pandas as pd
        # Build a single-row DataFrame from input
        df = pd.DataFrame([transaction_details])
        # One-hot encode categorical features
        df = pd.get_dummies(df, columns=['transaction_type', 'location'])
        # Ensure all expected columns are present
        expected = [
            'transaction_amount', 'account_age',
            'transaction_type_payment', 'transaction_type_transfer', 'transaction_type_withdrawal',
            'location_CA', 'location_NY', 'location_TX'
        ]
        for col in expected:
            if col not in df.columns:
                df[col] = 0
        df = df[expected]
        # Predict
        prob = self.model.predict_proba(df)[0][1]
        fraud_status = 'Fraud' if prob > 0.5 else 'Not Fraud'
        return {'fraud_probability': float(prob), 'fraud_status': fraud_status}
