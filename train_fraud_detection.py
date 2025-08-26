# Clean, train, and test Fraud Detection model
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv('fraud_detection_data.csv')
# Clean data (drop missing, convert types)
data = data.dropna()
# Use only selected features
features = ['Time', 'V1', 'V2', 'V3', 'Amount']
X = data[features]
y = data['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
preds = model.predict(X_test)
print('Fraud Detection Model Accuracy:', accuracy_score(y_test, preds))
joblib.dump(model, 'fraud_detection_model.pkl')
