# Customer Churn Prediction Module
# Predicts likelihood of customer leaving the service

import joblib

class ChurnPredictor:
    def __init__(self):
        self.model = joblib.load('churn_prediction_model.pkl')

    def predict(self, customer_data: dict) -> dict:
        import pandas as pd
        # Build a single-row DataFrame from input
        df = pd.DataFrame([customer_data])
        features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
        model_columns = self.model.feature_names_in_ if hasattr(self.model, 'feature_names_in_') else None
        if model_columns is not None:
            df = df.reindex(columns=model_columns, fill_value=0)
        # Predict
        prob = self.model.predict_proba(df)[0][1]
        strategy = 'Send personalized offer' if prob > 0.5 else 'Maintain engagement'
        return {'churn_probability': float(prob), 'retention_strategy': strategy}
