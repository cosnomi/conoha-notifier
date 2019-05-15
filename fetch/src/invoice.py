from datetime import datetime
from typing import NamedTuple, List


class InvoiceItem(NamedTuple):
    quantity: int
    name: str
    unit_price: float


class Invoice(NamedTuple):
    invoice_date: datetime
    bill_plus_tax: int
    detailed: List[InvoiceItem]