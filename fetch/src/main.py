import calendar
from config import read_config
from datetime import datetime
import requests
from zaim_push import push_payment_to_zaim
from slack_webhook import send_slack_message
from dotenv import load_dotenv
from typing import Dict, List
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
    invoices = get_payment(config['CONOHA_ACCOUNT_SERVICE_URL'], 50, year,
                           month, token, config['CONOHA_DATE_FORMAT'])
    push_payment_to_zaim(
        amount=sum([i.bill_plus_tax for i in invoices]),
        date=datetime(year, month,
                      calendar.monthrange(year, month)[1]),
    )
    send_slack_message(month, invoices)


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
                token: str, conoha_date_format: str) -> List[Invoice]:
    res = requests.get(
        account_service_url + '/billing-invoices?limit={}'.format(limit),
        headers={
            'X-Auth-Token': token
        }).json()
    print(res)

    invoice_list: List[Invoice] = []

    for invoice in res['billing_invoices']:
        invoice_datetime = datetime.strptime(invoice['invoice_date'],
                                             conoha_date_format)
        if invoice_datetime.year == year and invoice_datetime.month == month:
            invoice_list.append(
                Invoice(
                    invoice_date=invoice_datetime,
                    bill_plus_tax=invoice['bill_plus_tax'],
                    detailed=get_detailed_info(account_service_url,
                                               invoice["invoice_id"], token)))

    return invoice_list


def get_detailed_info(account_service_url: str, invoice_id: int,
                      token: str) -> List[InvoiceItem]:
    items = requests.get(
        account_service_url + '/billing-invoices/{}'.format(invoice_id),
        headers={
            'X-Auth-Token': token
        }).json()["billing_invoice"]["items"]
    invoice_items: List[InvoiceItem] = [
        InvoiceItem(
            quantity=item["quantity"],
            name=item["product_name"],
            unit_price=float(item["unit_price"])) for item in items
    ]
    return invoice_items


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
