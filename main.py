from fastapi import FastAPI, Request, Header, HTTPException
import uvicorn
from typing import Optional, Dict
import hmac
import hashlib
import json
import os
app = FastAPI()


@app.get("/")
def home():
    return "GitHub Webhook is running!", 200


@app.post("/webhook")
async def webhook_handler(
        x_github_event: Optional[str] = Header(None)
):
    # Processar eventos do GitHub
    if x_github_event == "ping":
        return {"message": "Hi! This is a FastAPI webhook"}

    if x_github_event != "push":
        raise HTTPException(400, "Unsupported event type")

    # Carregar payload e configurações


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


