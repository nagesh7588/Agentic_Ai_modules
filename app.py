from flask import Flask, request, jsonify, render_template_string
from auth import authenticate_user
from credit_risk import CreditRiskPredictor
from fraud_detection import FraudDetector
from churn_prediction import ChurnPredictor
from chatbot_assistant import ChatbotAssistant

app = Flask(__name__)

credit_risk = CreditRiskPredictor()
fraud_detector = FraudDetector()
churn_predictor = ChurnPredictor()
chatbot = ChatbotAssistant(credit_risk, fraud_detector, churn_predictor)

# Authentication decorator
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '')
        if not authenticate_user(token):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/credit-risk', methods=['POST'])
def credit_risk_endpoint():
    # Accept both JSON and form data
    if request.is_json:
        input_data = request.get_json()
    else:
        input_data = {k: request.form[k] for k in request.form}
    # Map form fields to model features
    # Example: person_age, person_income, person_emp_length, loan_percent_income, cb_person_cred_hist_length, home_ownership, loan_intent, loan_grade, cb_person_default_on_file
    features = ['person_age', 'person_income', 'person_emp_length', 'loan_percent_income', 'cb_person_cred_hist_length', 'person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
    # Convert types as needed
    for f in ['person_age', 'person_income', 'person_emp_length', 'loan_percent_income', 'cb_person_cred_hist_length']:
        if f in input_data:
            input_data[f] = float(input_data[f])
    result = credit_risk.predict(input_data)
    return jsonify(result)

@app.route('/fraud-detection', methods=['POST'])
def fraud_detection_endpoint():
    if request.is_json:
        input_data = request.get_json()
    else:
        input_data = {k: request.form[k] for k in request.form}
    # Map form fields to model features
    features = ['Time'] + [f'V{i}' for i in range(1,29)] + ['Amount']
    for f in features:
        if f in input_data:
            input_data[f] = float(input_data[f])
    result = fraud_detector.detect(input_data)
    return jsonify(result)

@app.route('/churn-prediction', methods=['POST'])
def churn_prediction_endpoint():
    if request.is_json:
        input_data = request.get_json()
    else:
        input_data = {k: request.form[k] for k in request.form}
    # Map form fields to model features
    features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
    for f in features:
        if f in input_data:
            input_data[f] = float(input_data[f])
    result = churn_predictor.predict(input_data)
    return jsonify(result)

@app.route('/chatbot', methods=['POST'])
@require_auth
def chatbot_endpoint():
    data = request.get_json()
    query = data.get('query', '')
    response = chatbot.answer_query(query)
    return jsonify({'response': response})

@app.route('/chatbot/route', methods=['POST'])
@require_auth
def chatbot_route_endpoint():
    data = request.get_json()
    module = data.get('module', '')
    payload = data.get('data', {})
    result = chatbot.handle_input(module, payload)
    return jsonify(result)


# Dashboard HTML template
dashboard_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Agentic AI Chatbot Automations – BFSI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .panel { border: 1px solid #ccc; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
        .result { background: #f9f9f9; padding: 10px; margin-top: 10px; border-radius: 4px; }
    </style>
    <script>
    function submitForm(formId, url, resultId) {
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            let html = '<table>';
            for (const [k, v] of Object.entries(data)) {
                html += `<tr><td><b>${k}</b></td><td>${v}</td></tr>`;
            }
            html += '</table>';
            document.getElementById(resultId).innerHTML = html;
        });
        return false;
    }
    </script>
</head>
<body>
    <h1>Agentic AI Chatbot Automations – BFSI</h1>
    <div class="panel">
        <form id="creditForm" onsubmit="return submitForm('creditForm', '/credit-risk', 'creditResult')" autocomplete="off">
            <h2>Credit Risk Prediction</h2>
            <label>Age: <input name="person_age" type="number" required></label><br>
            <label>Annual Income: <input name="person_income" type="number" step="any" required></label><br>
            <label>Employment Length (years): <input name="person_emp_length" type="number" step="any" required></label><br>
            <label>Percent Income to Loan: <input name="loan_percent_income" type="number" step="any" required></label><br>
            <label>Credit History Length: <input name="cb_person_cred_hist_length" type="number" required></label><br>
            <label>Home Ownership: <select name="person_home_ownership"><option>RENT</option><option>OWN</option><option>MORTGAGE</option><option>OTHER</option></select></label><br>
            <label>Loan Intent: <select name="loan_intent"><option>PERSONAL</option><option>EDUCATION</option><option>MEDICAL</option><option>VENTURE</option><option>HOMEIMPROVEMENT</option><option>DEBTCONSOLIDATION</option></select></label><br>
            <label>Loan Grade: <select name="loan_grade"><option>A</option><option>B</option><option>C</option><option>D</option><option>E</option><option>F</option></select></label><br>
            <label>Default on File: <select name="cb_person_default_on_file"><option>N</option><option>Y</option></select></label><br>
            <button type="submit">Predict Risk</button>
        </form>
        <div id="creditResult" class="result"></div>
    </div>
    <div class="panel">
        <form id="fraudForm" onsubmit="return submitForm('fraudForm', '/fraud-detection', 'fraudResult')" autocomplete="off">
            <h2>Fraud Detection</h2>
            <label>Time: <input name="Time" type="number" required></label><br>
            <label>V1: <input name="V1" type="number" step="any" required></label><br>
            <label>V2: <input name="V2" type="number" step="any" required></label><br>
            <label>V3: <input name="V3" type="number" step="any" required></label><br>
            <label>Amount: <input name="Amount" type="number" step="any" required></label><br>
            <button type="submit">Detect Fraud</button>
        </form>
        <div id="fraudResult" class="result"></div>
    </div>
    <div class="panel">
        <form id="churnForm" onsubmit="return submitForm('churnForm', '/churn-prediction', 'churnResult')" autocomplete="off">
            <h2>Customer Churn Prediction</h2>
            <label>Tenure (months): <input name="tenure" type="number" required></label><br>
            <label>Monthly Charges: <input name="MonthlyCharges" type="number" step="any" required></label><br>
            <label>Total Charges: <input name="TotalCharges" type="number" step="any" required></label><br>
            <label>Senior Citizen: <select name="SeniorCitizen"><option value="0">No</option><option value="1">Yes</option></select></label><br>
            <button type="submit">Predict Churn</button>
        </form>
        <div id="churnResult" class="result"></div>
    </div>
</body>
</html>
'''

# Dashboard route
@app.route('/', methods=['GET'])
def dashboard():
    return render_template_string(dashboard_html)

if __name__ == '__main__':
    app.run(debug=True)
