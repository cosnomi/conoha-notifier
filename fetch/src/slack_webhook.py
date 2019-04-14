import requests
import os
import json

USERNAME = "ConoHa 料金通知"


def send_slack_message(month, amount):
    payload = {
        "username": USERNAME,
        "icon_url": os.environ['SLACK_ICON_URL'],
        "text": "{}月分の請求額は{}円です。".format(month, amount)
    }
    requests.post(
        os.environ['SLACK_WEBHOOK_URL'],
        data=json.dumps(payload).encode("utf-8"))
