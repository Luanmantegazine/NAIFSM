import hmac
import requests
import json
import os
import datetime
import hashlib
import time


class WebhookPublisher:
    def __init__(self, webhook_url, secret_key=None):
        self.webhook_url = webhook_url
        self.secret_key = secret_key

    def sign_payload(self, payload):
        """Creates an HMAC signature for the payload using the secret key."""
        if not self.secret_key:
            return {}
        # Serialize the payload using consistent settings
        payload_json = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload_json.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return {'X-Signature': signature}

    def send_webhook(self, payload):
        """Prepares the payload, signs it, and sends it as a POST request."""
        # Ensure the payload has a 'timestamp'; convert it to ISO 8601 format
        timestamp = payload.get('timestamp', int(time.time()))
        payload['timestamp'] = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        headers = {'Content-Type': 'application/json'}
        headers.update(self.sign_payload(payload))

        # Serialize payload to JSON before sending
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
    # Set up the webhook publisher with the receiver's endpoint and a secret key
    webhook_url = "http://localhost:8000/"  # Change as needed to match your receiver URL
    secret_key = 'l12345'

    webhook_client = WebhookPublisher(webhook_url=webhook_url, secret_key=secret_key)

    # Create an event payload
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
