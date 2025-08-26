from fastapi import FastAPI, Request, Depends, HTTPException
from auth import authenticate_user
from credit_risk import CreditRiskPredictor
from fraud_detection import FraudDetector
from churn_prediction import ChurnPredictor
from chatbot_assistant import ChatbotAssistant
from schemas import CustomerProfile, TransactionDetails, CustomerData, ChatbotQuery, ChatbotRoute

app = FastAPI(title="Agentic AI Chatbot Automations – BFSI")

credit_risk = CreditRiskPredictor()
fraud_detector = FraudDetector()
churn_predictor = ChurnPredictor()
chatbot = ChatbotAssistant(credit_risk, fraud_detector, churn_predictor)

def get_token(request: Request):
    token = request.headers.get("Authorization", "")
    if not authenticate_user(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

@app.post("/credit-risk")
def credit_risk_endpoint(customer_profile: CustomerProfile, token: str = Depends(get_token)):
    return credit_risk.predict(customer_profile.dict())

@app.post("/fraud-detection")
def fraud_detection_endpoint(transaction_details: TransactionDetails, token: str = Depends(get_token)):
    return fraud_detector.detect(transaction_details.dict())

@app.post("/churn-prediction")
def churn_prediction_endpoint(customer_data: CustomerData, token: str = Depends(get_token)):
    return churn_predictor.predict(customer_data.dict())

@app.post("/chatbot")
def chatbot_endpoint(chatbot_query: ChatbotQuery, token: str = Depends(get_token)):
    return {"response": chatbot.answer_query(chatbot_query.query)}

@app.post("/chatbot/route")
def chatbot_route_endpoint(chatbot_route: ChatbotRoute, token: str = Depends(get_token)):
    return chatbot.handle_input(chatbot_route.module, chatbot_route.data)
