'''
Pydantic models for input validation. Primarily used with FastAPI routes in server.py
'''
from typing import List

from pydantic import BaseModel

class Account(BaseModel):
    id: str
    holder: str
    type: str
    customer_type: str
    capabilities: str
    base_currency: str

class Security(BaseModel):
    symbol: str
    name: str

class Summary(BaseModel):
    security: str
    period: str
    value: float

class Filters(BaseModel):
    accounts: List[str]
    security: str
    start_date: str
    end_date: str
    pnl_type: str