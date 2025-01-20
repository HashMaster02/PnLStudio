from fastapi import Request
from Core.models import Filters
import json


async def format_filters(request: Request, call_next):
    # Read and parse the request body
    body_bytes = await request.body()
    try:
        body = json.loads(body_bytes)

        body['accounts'] = [account.upper() for account in body['accounts']]
        body['security'] = body['security'].upper()
        body['start_date'] = body['start_date']
        body['end_date'] = body['end_date']
        body['pnl_type'] = body['pnl_type'].lower()

        request._body = json.dumps(body).encode()  # Update the request body
    except json.JSONDecodeError:
        # If body is not JSON, continue
        pass


    response = await call_next(request)
    return response