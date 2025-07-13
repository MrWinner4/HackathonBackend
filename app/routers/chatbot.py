from dis import Instruction
from google.genai.types import GenerateContentConfig
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

client = genai.Client(api_key=api_key)

chat = client.chats.create(model="gemini-2.5-flash")


class ChatbotRequest(BaseModel):
    message: str

class ChatbotResponse(BaseModel):
    response: str

@router.post("/ask", response_model=ChatbotResponse)
def ask_chatbot(request: ChatbotRequest):
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents= f" The student's query is: {request.message}. Please respond in the most appropriate manner to help them learn.",
    config=types.GenerateContentConfig(
        system_instruction="You are a financial expert, teaching teens financial literacy. You will use easy to understand language, occasional analogies, and encourage the student in their learning. Make your responses bite sized, so that teens can understand them quickly, get to the point and answer the question. Do not ask any questions to the user, simply finish your response without any hanging questions or unanswered bits."
    )
    )
    print(response.text)
    if response.text:
        return ChatbotResponse(response=response.text)
    else:
        return ChatbotResponse(response="Looks like we had an error - whoops!")
