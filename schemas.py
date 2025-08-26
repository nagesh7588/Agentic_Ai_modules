from pydantic import BaseModel

class CustomerProfile(BaseModel):
    financial_history: str
    income: float
    credit_score: float
    repayment_patterns: str

class TransactionDetails(BaseModel):
    amount: float
    device: str
    location: str
    frequency: int
    history: str

class CustomerData(BaseModel):
    demographics: str
    interactions: str
    complaints: str
    transaction_frequency: int

class ChatbotQuery(BaseModel):
    query: str

class ChatbotRoute(BaseModel):
    module: str
    data: dict
