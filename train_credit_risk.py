# Clean, train, and test Credit Risk model
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv('credit_risk_data.csv')
# Clean data (drop missing, convert types)
data = data.dropna()
# Select features (example: age, income, emp_length, percent_income, cred_hist_length, home_ownership, loan_intent, loan_grade, cb_person_default_on_file)
features = [
    'person_age', 'person_income', 'person_emp_length', 'loan_percent_income',
    'cb_person_cred_hist_length', 'person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'
]
# Convert categorical columns to dummies
categorical = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
data = pd.get_dummies(data, columns=categorical)
X = data.drop(['loan_status'], axis=1)
y = data['loan_status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
preds = model.predict(X_test)
print('Credit Risk Model Accuracy:', accuracy_score(y_test, preds))
joblib.dump(model, 'credit_risk_model.pkl')
