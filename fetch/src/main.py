import requests
from config import read_config
from datetime import datetime


def lambda_handler(event, context):
    config = read_config()
    token = get_token(
        config['CONOHA_TOKEN_URL'],
        get_token_request_payload(config['CONOHA_API_USER'],
                                  config['CONOHA_API_PW'],
                                  config['CONOHA_TENANT_ID']))
    get_payment(config['CONOHA_ACCOUNT_SERVICE_URL'], 50, event['year'],
                event['month'], token, config['CONOHA_DATE_FORMAT'])


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
    pay = 0  # 合計
    for invoice in res['billing_invoices']:
        invoice_datetime = datetime.strptime(invoice['invoice_date'],
                                             conoha_date_format)
        if invoice_datetime.year == year and invoice_datetime.month == month:
            pay += int(invoice['bill_plus_tax'])
    return pay