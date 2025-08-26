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
        features = ['Time', 'V1', 'V2', 'V3', 'Amount']
        model_columns = self.model.feature_names_in_ if hasattr(self.model, 'feature_names_in_') else None
        if model_columns is not None:
            df = df.reindex(columns=model_columns, fill_value=0)
        # Predict
        prob = self.model.predict_proba(df)[0][1]
        alert = prob > 0.5
        action = 'Review transaction' if alert else 'No action needed'
        return {'fraud_alert': alert, 'probability_score': float(prob), 'suggested_action': action}
