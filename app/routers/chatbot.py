from fastapi import APIRouter
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

client = genai.Client(api_key=api_key)

class ChatbotRequest(BaseModel):
    message: str

class ChatbotResponse(BaseModel):
    response: str

@router.post("/ask", response_model=ChatbotResponse)
def ask_chatbot(request: ChatbotRequest):
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents= f"You are a financial expert, teaching teens financial literacy. You will use easy to understand language, analogies, and encourage the student in their learning. Their query is: {request.message}. Please respond in the most appropriate manner to help them learn."
    )
    print(response.text)
    if response.text:
        return ChatbotResponse(response=response.text)
    else:
        return ChatbotResponse(response="Looks like we had an error - whoops!")
