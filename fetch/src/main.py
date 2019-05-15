import calendar
from config import read_config
from datetime import datetime
import requests
from zaim_push import push_payment_to_zaim
from slack_webhook import send_slack_message
from dotenv import load_dotenv
from typing import Dict
from invoice import Invoice, InvoiceItem

load_dotenv()


def lambda_handler(event, context):
    config = read_config()
    token = get_token(
        config['CONOHA_TOKEN_URL'],
        get_token_request_payload(config['CONOHA_API_USER'],
                                  config['CONOHA_API_PW'],
                                  config['CONOHA_TENANT_ID']))
    year = event.get('year', datetime.now().year)
    month = event.get('month', datetime.now().month)
    amount = get_payment(config['CONOHA_ACCOUNT_SERVICE_URL'], 50, year, month,
                         token, config['CONOHA_DATE_FORMAT'])
    push_payment_to_zaim(
        amount=amount,
        date=datetime(year, month,
                      calendar.monthrange(year, month)[1]),
    )
    send_slack_message(month, amount)


def get_token(token_url: str, req_payload) -> str:
    res = requests.post(token_url, json=req_payload).json()
    if res is None:
        raise ConnectionError
    return res['access']['token']['id']


def get_token_request_payload(api_user: str, api_pw: str, tenant_id: str):
    return {
        'auth': {
            'passwordCredentials': {
                'username': api_user,
                'password': api_pw
            },
            'tenantId': tenant_id
        }
    }


def get_payment(account_service_url: str, limit: int, year: int, month: int,
                token: str, conoha_date_format: str):
    res = requests.get(
        account_service_url + '/billing-invoices?limit={}'.format(limit),
        headers={
            'X-Auth-Token': token
        }).json()
    print(res)
    pay = 0  # 合計
    for invoice in res['billing_invoices']:
        invoice_datetime = datetime.strptime(invoice['invoice_date'],
                                             conoha_date_format)
        if invoice_datetime.year == year and invoice_datetime.month == month:
            pay += int(invoice['bill_plus_tax'])
            get_detailed_info(account_service_url, invoice["invoice_id"], token)

    return pay


def get_detailed_info(account_service_url: str, invoice_id: int,
                      token: str) -> InvoiceItem:
    res = requests.get(
        account_service_url + '/billing-invoices/{}'.format(invoice_id),
        headers={
            'X-Auth-Token': token
        }).json()
    invoice_item = InvoiceItem(
        quantity=res["quantity"], name=res["product_name"])
    return invoice_item


if __name__ == "__main__":
    import os
    event: Dict[str, int] = {}
    if "MOCK_DATE" in os.environ.keys():
        mock_date = datetime.strptime(os.environ["MOCK_DATE"],
                                      "%Y-%m-%d %H:%M:%S")
        event = {
            "year": mock_date.year,
            "month": mock_date.month,
        }
    lambda_handler(event, {})
