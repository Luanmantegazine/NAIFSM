import json
import datetime
import time
import hashlib
import hmac
import requests


class WebhookPublisher:
    def __init__(self, webhook_url, secret):
        self.webhook_url = webhook_url
        self.secret = secret

    def send_webhook(self, payload):
        timestamp = payload.get('timestamp', int(time.time()))
        payload['timestamp'] = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        event_type = payload.get("event", "push")
        payload_json = json.dumps(payload)

        signature = hmac.new(self.secret.encode(), payload_json.encode(), hashlib.sha256).hexdigest()
        header_signature = "sha256=" + signature

        headers = {
            'Content-Type': 'application/json',
            'X-GitHub-Event': event_type,
            'X-Hub-Signature-256': header_signature
        }

        try:
            response = requests.post(
                self.webhook_url,
                data=payload_json,
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                print(f"Webhook successfully sent: {response.text}")
            else:
                print(f"Failed to send webhook: {response.status_code}, {response.text}")
        except requests.RequestException as e:
            print(f"Exception during webhook send: {e}")
            response = None
        return response


if __name__ == '__main__':
    webhook_url = "https://c430-2804-14d-4c85-97de-592-d8-dfff-cc94.ngrok-free.app/webhook"
    secret = "12345"
    publisher = WebhookPublisher(webhook_url=webhook_url, secret=secret)

    while True:

        sample_payload = {
            "event": "push",
            "message": "Commit realizado com sucesso!",
            "repo": "NAIFSM",
            "commit_id": str(int(time.time()))
        }
        publisher.send_webhook(sample_payload)
        time.sleep(10)
