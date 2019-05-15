import requests
import os
import json
from invoice import Invoice
from typing import List

USERNAME = "ConoHa 料金通知"


def send_slack_message(month, invoices: List[Invoice]):
    payload = {
        "username":
            USERNAME,
        "icon_url":
            os.environ['SLACK_ICON_URL'],
        "text":
            "{}月分の請求額は{}円です。".format(month,
                                     sum([i.bill_plus_tax for i in invoices]))
    }
    requests.post(
        os.environ['SLACK_WEBHOOK_URL'],
        data=json.dumps(payload).encode("utf-8"))
