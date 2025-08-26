# Clean, train, and test Churn Prediction model
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv('churn_prediction_data.csv')
# Clean data (drop missing, convert types)
data = data.dropna()
data['tenure'] = data['tenure'].astype(int)
# Select relevant features
features = [
    'tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen'
]
categorical = ['gender', 'Contract', 'PaymentMethod', 'InternetService', 'PhoneService', 'Partner', 'Dependents', 'PaperlessBilling']
data = pd.get_dummies(data, columns=categorical)
# Only keep numeric columns for X
X = data.drop(['customerID', 'Churn'], axis=1)
X = X.select_dtypes(include=['number'])
y = data['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
preds = model.predict(X_test)
print('Churn Prediction Model Accuracy:', accuracy_score(y_test, preds))
joblib.dump(model, 'churn_prediction_model.pkl')
