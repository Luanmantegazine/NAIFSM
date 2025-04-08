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

        headers = {'Content-Type': 'application/json'}

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

    webhook_url = "http://localhost:8000/"  # Change as needed to match your receiver URL

    webhook_client = WebhookPublisher(webhook_url=webhook_url)

    event_payload = {
        "event": "push",
        "repository": {
            "name": "NAIFSM",
            "url": "https://github.com/Luanmantegazine/NAIFSM"
        },
        "pusher": {
            "name": "luanmantegazine"
        },
        # Using the current Unix timestamp
        "timestamp": int(time.time()),
    }

    # Send the webhook event
    webhook_client.send_webhook(event_payload)
