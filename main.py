from fastapi import FastAPI, Request, Header, HTTPException
import uvicorn
import hmac
import hashlib
import os
app = FastAPI()

GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "senha")
def signature_valid(payload: bytes, signature_header: str)-> bool:
    if not signature_header or "=" not in signature_header:
        return False
    sha_name, received_signature = signature_header.split("=")
    if sha_name != "sha256":
        return False

    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected = mac.hexdigest()

    return hmac.compare_digest(expected, received_signature)

@app.get("/")
def home():
    return "GitHub Webhook is running!", 200


@app.post("/webhook")
async def webhook_handler(
    request: Request,
    x_github_event: str = Header("ping")
):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not signature_valid(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = await request.json()

    if x_github_event == "ping":
        print("Received ping from GitHub!")
    elif x_github_event == "push":
        print("Received a push event with the following commits:")
        for commit in data.get("commits", []):
            print(" -", commit["message"])
    else:
        print(f"Received GitHub event: {x_github_event}")

    # 5. Return a 200 OK response so GitHub knows we received it
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


