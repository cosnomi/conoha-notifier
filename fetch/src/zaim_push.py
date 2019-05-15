import zaim  # type: ignore
import os
from datetime import datetime


def push_payment_to_zaim(amount, date: datetime = None, name="ConoHa"):
    if date is None:
        date = datetime.now()
    api = zaim.Api(
        consumer_key=os.environ['ZAIM_CONSUMER_KEY'],
        consumer_secret=os.environ['ZAIM_CONSUMER_SECRET'],
        access_token=os.environ['ZAIM_ACCESS_TOKEN'],
        access_token_secret=os.environ['ZAIM_ACCESS_TOKEN_SECRET'])
    api.verify()
    api.payment(
        category_id=os.environ['ZAIM_CONOHA_CATEGORY_ID'],
        genre_id=os.environ['ZAIM_CONOHA_GENRE_ID'],
        from_account_id=os.environ['ZAIM_CONOHA_ACCOUNT_ID'],
        amount=amount,
        date=date.strftime('%Y-%m-%d'),
        name=name)
