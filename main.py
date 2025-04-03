from fastapi import FastAPI, Request, Header, HTTPException
import uvicorn
import hmac
import hashlib
import os
app = FastAPI()

@app.get("/")
def home():
    return "GitHub Webhook is running!", 200


@app.post("/webhook")
async def webhook_handler(payload: dict):
    if "after" in payload:
        return {"message": "There was a push event"}
    else:
        raise HTTPException(status_code=400, detail='no payload')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


