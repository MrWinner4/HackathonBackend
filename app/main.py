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

# Initialize Firebase Admin SDK
try:
    # Get Firebase project ID from environment
    firebase_project_id = os.environ.get('FIREBASE_PROJECT_ID')
    
    if not firebase_project_id:
        print("Warning: FIREBASE_PROJECT_ID not set. Firebase Admin SDK may not work properly.")
    
    # Check if we have Firebase credentials in environment
    firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
    
    if firebase_credentials:
        # Use service account credentials from environment variable
        import json
        cred_dict = json.loads(firebase_credentials)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'projectId': firebase_project_id
        })
    else:
        # For production (Render), try to auto-detect credentials
        # This requires setting GOOGLE_APPLICATION_CREDENTIALS or using default credentials
        firebase_admin.initialize_app({
            'projectId': firebase_project_id
        })
        
except ValueError:
    # App already initialized
    pass
except Exception as e:
    print(f"Firebase Admin initialization failed: {e}")
    # Continue without Firebase Admin for now
    pass

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