import hmac
import requests
import json
import os
import datetime
import hashlib
import time


class WebhookPublisher:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_webhook(self, payload):
        timestamp = payload.get('timestamp', int(time.time()))
        payload['timestamp'] = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        event_type = payload.get("event", "push")

        headers = {
            'Content-Type': 'application/json',
            'X-GitHub-Event': event_type
        }

        payload_json = json.dumps(payload)
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

    webhook_url = "https://12d7-2804-14d-4c85-97de-211b-499f-fde5-121d.ngrok-free.app/webhook"  # Change as needed to match your receiver URL

    webhook_client = WebhookPublisher(webhook_url=webhook_url)

    event_payload = {
        "event": "push",
        "ref": "main",
        "repository": {
            "id": 660779886,
            "name": "NAIFSM",
            "full_name": "Luanmantegazine/NAIFSM",
            "url": "https://github.com/Luanmantegazine/NAIFSM"
        },
        "pusher": {
            "name": "Luanmantegazine",

        },
        "commits": [
            {
                "id": "c1d2e3f4",
                "message": "Initial commit",
                "timestamp": "2020-01-01T12:00:00Z",
                "url": "https://github.com/Luanmantegazine/NAIFSM/commit/c1d2e3f4",
                "author": {
                    "name": "Luanmantegazine",
                }
            },

        ],
        # Using the current Unix timestamp
        "timestamp": int(time.time()),
    }

    # Send the webhook event
    webhook_client.send_webhook(event_payload)
