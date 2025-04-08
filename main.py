import json
import logging
import hmac
import hashlib

from typing import Optional
from fastapi import FastAPI, Request, Header, HTTPException, status
import uvicorn

WEBHOOK_SECRET = "12345"


def verify_signature(payload_body: bytes, signature: str) -> bool:
    computed_signature = hmac.new(WEBHOOK_SECRET.encode(), payload_body, hashlib.sha256).hexdigest()
    if signature.startswith("sha256="):
        signature = signature.split("sha256=")[1]
    return hmac.compare_digest(computed_signature, signature)


app = FastAPI()

logging.basicConfig(level=logging.INFO)


@app.get("/", response_model=dict)
def home():
    return {"message": "GitHub Webhook is running!"}


@app.post("/webhook")
async def webhook_handler(
        request: Request,
        x_github_event: Optional[str] = Header(None),
        x_hub_signature_256: Optional[str] = Header(None)
):
    body_bytes = await request.body()

    logging.info(f"Raw X-GitHub-Event header: {x_github_event}")

    if not x_github_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-GitHub-Event header"
        )
    if not x_hub_signature_256:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-Hub-Signature-256 header"
        )

    if not verify_signature(body_bytes, x_hub_signature_256):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        )

    payload = json.loads(body_bytes)

    logging.info(f"Received event: {x_github_event} with payload: {payload}")

    event = x_github_event.strip().lower()

    if event == "ping":
        return {"message": "pong", "event": event, "payload": payload}

    if event == "push":
        logging.info("Processing push event")
        return {"message": "Push event received", "payload": payload}

    if event == "commit":
        logging.info("Processing commit event")
        return {"message": "Commit event received", "payload": payload}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported event type: {x_github_event}"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
