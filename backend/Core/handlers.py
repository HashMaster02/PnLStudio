from Utils.db import get_db
import Core.models as Model
import Utils.dataframeprocessor as dfprocessor
from pandas import DataFrame
import numpy as np

def get_topdown_bottomup_securities(filters: Model.Filters, dataframe: DataFrame):
    try:

        top_down = dfprocessor.get_top_down(dataframe=dataframe,
                                accounts=filters.accounts,
                                end_date=filters.end_date)
        bottom_up = dfprocessor.get_bottom_up(dataframe=dataframe,
                                accounts=filters.accounts,
                                end_date=filters.end_date)

        return {'top_down': top_down, 'bottom_up': bottom_up}

    except Exception as e:
        print(f"Error when retrieving top-down and bottom-up data: {e}")
        raise e

def get_available_tickers(dataframe: DataFrame):
    try:
        tickers = dfprocessor.get_available_securities(dataframe)
        return tickers.to_list()
    except Exception as e:
        print(f"Error when retrieving tickers: {e}")
        raise e

def get_available_accounts(dataframe: DataFrame):
    try:
        accounts = dfprocessor.get_available_accounts(dataframe)
        return accounts.tolist()
    except Exception as e:
        print(f"Error when retrieving tickers: {e}")
        raise e

def get_graph_data(dataframe: DataFrame, filters: Model.Filters):
    try:
        results = dfprocessor.get_security_values(dataframe=dataframe,
                                                security=filters.security.upper(), 
                                                accounts = [account.upper() for account in filters.accounts],
                                                start_date = filters.start_date, 
                                                end_date = filters.end_date)
        return results 
    except Exception as e:
        print(f"Error when retrieving graph data for {filters.security}: {e}")
        raise e

def get_card_data(dataframe: DataFrame, filters: Model.Filters):
    try:
        data = {
            "total_gains": dfprocessor.get_total_gains(dataframe, end_date=filters.end_date, accounts=filters.accounts),
            "realized_gains": dfprocessor.get_realized_gains(dataframe, end_date=filters.end_date, accounts=filters.accounts),
            "unrealized_gains": dfprocessor.get_unrealized_gains(dataframe, end_date=filters.end_date, accounts=filters.accounts),
            "interest": dfprocessor.get_interest(dataframe, end_date=filters.end_date, accounts=filters.accounts),
            "dividends": dfprocessor.get_dividends(dataframe, end_date=filters.end_date, accounts=filters.accounts) }
        return data
    except Exception as e:
        print(f"Error when retrieving card data for {filters.accounts} on {filters.end_date}: {e}")
        raise e
