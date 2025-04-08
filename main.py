from fastapi import FastAPI, Header, HTTPException, Request, status
import uvicorn
from typing import Optional
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.get("/", response_model=dict)
def home():
    return {"message": "GitHub Webhook is running!"}

@app.post("/webhook")
async def webhook_handler(
    request: Request,
    x_github_event: Optional[str] = Header(None)
):
    logging.info(f"Raw X-GitHub-Event header: {x_github_event}")
    if not x_github_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-GitHub-Event header"
        )

    event = x_github_event.strip().lower()
    payload = await request.json()
    logging.info(f"Received event: {x_github_event} with payload: {payload}")

    if x_github_event == "ping":
        return {"message": "pong", "event": event, "payload": payload}

    if x_github_event == "push":
        logging.info("Processing push event")
        return {"message": "Push event received", "payload": payload}

    if x_github_event == "commit":
        logging.info("Processing commit event")
        return {"message": "Commit event received", "payload": payload}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported event type: {x_github_event}"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
