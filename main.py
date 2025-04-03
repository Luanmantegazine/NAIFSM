from fastapi import FastAPI, Request, Header, HTTPException
import uvicorn
import hmac
import hashlib
import os
app = FastAPI()

GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "senha")
def signature_valid(payload: bytes, signature_sha256: str, signature_sha1: str)-> bool:
    if signature_sha256:
        try:
            sha_name, signature = signature_sha256.split("=")
        except ValueError:
            return False

        if sha_name != "sha256":
            return False

        mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
        if hmac.compare_digest(mac.hexdigest(), signature):
            return True

        # Fallback to SHA-1 if available
    if signature_sha1:
        try:
            sha_name, signature = signature_sha1.split("=")
        except ValueError:
            return False

        if sha_name != "sha1":
            return False

        mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha1)
        if hmac.compare_digest(mac.hexdigest(), signature):
            return True

    return False

@app.get("/")
def home():
    return "GitHub Webhook is running!", 200


@app.post("/webhook")
async def webhook_handler(
    request: Request,
    x_github_event: str = Header("ping")
):
    body = await request.body()
    signature256 = request.headers.get("X-Hub-Signature-256")
    signature1 = request.headers.get("X-Hub-Signature-1")

    if not signature_valid(body, signature256, signature1):
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


