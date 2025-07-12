from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class ChatbotRequest(BaseModel):
    message: str

class ChatbotResponse(BaseModel):
    response: str

@router.post("/ask", response_model=ChatbotResponse)
def ask_chatbot(request: ChatbotRequest):
    # For now, return a dummy response
    return ChatbotResponse(response="This is a dummy chatbot response.")
