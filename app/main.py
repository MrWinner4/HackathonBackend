from dotenv import load_dotenv
from .routers import users, piggybank, goals, lessons, stories, chatbot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import os
import uvicorn

load_dotenv()

# Initialize Firebase Admin SDK - Simplified
try:
    firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
    
    if firebase_credentials:
        # Use service account credentials from environment variable
        import json
        cred_dict = json.loads(firebase_credentials)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin SDK initialized successfully with service account")
    else:
        print("⚠️  FIREBASE_CREDENTIALS not set. Firebase Admin SDK not initialized.")
        
except ValueError:
    print("ℹ️  Firebase Admin SDK already initialized")
except Exception as e:
    print(f"❌ Firebase Admin initialization failed: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render sets this
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(piggybank.router)
app.include_router(goals.router)
app.include_router(lessons.router)
app.include_router(stories.router)
app.include_router(chatbot.router)