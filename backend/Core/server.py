import uvicorn
import Core.models as Models
from fastapi import FastAPI, APIRouter, Request
from Core.handlers import ( get_topdown_bottomup_securities, get_available_tickers,
                            get_available_accounts, get_graph_data, get_card_data)

router = APIRouter(prefix="/api")

@router.get("/accounts")
def get_accounts():
    try:
        data = get_available_accounts(router.dataframes['total'])
        return {"status": 200, 
                "message": "accounts retrieved successfully",
                "data": data}
    except Exception as e:
        return {"status":500 , "message": f"Error retrieving available accounts: {e}", "data": None}

@router.get("/security-tickers")
def get_tickers():
    try:
        data = get_available_tickers(router.dataframes['total'])
        return {"status": 200, 
                "message": "ticker retrieved successfully",
                "data": data}
    except Exception as e:
        return {"status":500 , "message": f"Error retrieving available tickers: {e}", "data": None}

@router.post("/card-data")
def get_cards(filters: Models.Filters):
    try:
        data = get_card_data(router.dataframes["total"], filters) # any of the dataframes will do here
        return {"status": 200, 
                "message": "card data retrieved successfully",
                "data": data}
    except Exception as e:
        return {"status":500 , "message": f"Error retrieving card data: {e}", "data": None}

@router.post("/graph-data")
def get_totals(filters: Models.Filters):
    try:
        data = get_graph_data(router.dataframes[filters.pnl_type], filters)
        return {"status": 200, 
                "message": "graph data retrieved successfully",
                "data": data}
    except Exception as e:
        return {"status":500 , "message": f"Error retrieving {filters.pnl_type} graph data: {e}", "data": None}

@router.post("/top-down-bottom-up")
def get_top_down_stocks(filters: Models.Filters):
    try:
        top_bottom_stocks = get_topdown_bottomup_securities(filters, router.dataframes[filters.pnl_type])
        return {"status": 200, 
                "message": "Top-down and Bottom-up securities data retrieved successfully", 
                "data": top_bottom_stocks}
    except Exception as e:
        return {"status":500 , "message": f"Error retrieving top-down and bottom-up securities data: {e}", "data": None}
