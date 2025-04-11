import json
import logging
import hmac
import hashlib

from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, Header, HTTPException, status
from fastapi.responses import JSONResponse
import uvicorn

WEBHOOK_SECRET = "12345"

logger = logging.getLogger("github_webhook")
logging.basicConfig(level=logging.INFO)


def verify_signature(payload_body: bytes, signature: str) -> bool:
    computed_signature = hmac.new(WEBHOOK_SECRET.encode(), payload_body, hashlib.sha256).hexdigest()
    if signature.startswith("sha256="):
        signature = signature.split("sha256=")[1]
    return hmac.compare_digest(computed_signature, signature)


app = FastAPI()


@app.get("/", response_model=Dict[str, str])
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

    event_handlers = {
        "ping": lambda pl: {"message": "pong", "event": event, "payload": pl},
        "push": lambda pl: {"message": "Push event received", "payload": pl},
        "commit": lambda pl: {"message": "Commit event received", "payload": pl},
    }

    if event in event_handlers:
        response = event_handlers[event](payload)
        return JSONResponse(content=response)

    logger.warning("Unsupported event type: %s", event)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
