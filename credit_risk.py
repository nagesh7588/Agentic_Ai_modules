# Credit Risk Prediction Module
# Predicts probability of default for a customer

import joblib

class CreditRiskPredictor:
    def __init__(self):
        self.model = joblib.load('credit_risk_model.pkl')

    def predict(self, customer_profile: dict) -> dict:
        import pandas as pd
        # Build a single-row DataFrame from input
        df = pd.DataFrame([customer_profile])
        # List of all features used in training
        features = [
            'person_age', 'person_income', 'person_emp_length', 'loan_percent_income',
            'cb_person_cred_hist_length', 'person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'
        ]
        categorical = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
        # One-hot encode categoricals
        df = pd.get_dummies(df, columns=categorical)
        # Load training columns from model (assume model was trained with X.columns)
        # For simplicity, hardcode columns here (should match X.columns from training)
        model_columns = self.model.feature_names_in_ if hasattr(self.model, 'feature_names_in_') else None
        if model_columns is not None:
            df = df.reindex(columns=model_columns, fill_value=0)
        else:
            # Fallback: use all columns in df
            pass
        # Predict
        risk_score = self.model.predict_proba(df)[0][1]
        category = 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low'
        return {'risk_score': float(risk_score), 'risk_category': category}
