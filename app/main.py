from .routers import users, piggybank
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import uvicorn

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
