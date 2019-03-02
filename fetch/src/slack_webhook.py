import requests
import os
import json


def send_slack_message(month, amount):
    payload = {"text": "{}月分の請求額は{}円です。".format(month, amount)}
    requests.post(
        os.environ['SLACK_WEBHOOK_URL'],
        data=json.dumps(payload).encode("utf-8"))
