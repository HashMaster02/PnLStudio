from dateutil import parser as dateparser

def get_available_securities(dataframe):
    try:
        snake_case_columns = dataframe.columns[dataframe.columns.str.match('^[a-z][a-z0-9_]*$')]
        cols = dataframe.drop(columns=snake_case_columns)
        return cols.columns
    
    except Exception as e:
        print(f"Something went wrong while getting column headers: {e}")
        raise e

def get_available_accounts(dataframe):
    try:
        return dataframe['account_name'].unique()
    except Exception as e:
        print(f"Something went wrong while getting column headers: {e}")
        raise e

def get_total_gains(dataframe, accounts, end_date):

    try:
        # Ensure date format is correct (e.g. 2002-30-07)
        end= dateparser.parse(end_date).strftime('%Y-%m-%d')

        # Filter for specific account and date
        filtered_df = dataframe[
            (dataframe['account_name'].isin(accounts)) & 
            (dataframe['statement_end'] == end)
        ]

        if filtered_df.empty:
            raise Exception(f"No data found for account {accounts} on date {end_date}")

        # Sum values across all matching accounts
        total_gains = filtered_df.eval(
            'ending_value - transferred_pl_adjustments - deposits_and_withdrawals + dividends'
            '- starting_value + dividend_accruals - interest - interest_accruals + other_fee'
        ).sum()

        return total_gains

    except Exception as e:
        print(f"Something went wrong while calculating Total Gains: {e}")
        raise e

def get_realized_gains(dataframe, accounts, end_date):
    try:
        # Ensure date format is correct (e.g. 2002-30-07)
        end= dateparser.parse(end_date).strftime('%Y-%m-%d')

        # Filter for specific accounts and date
        filtered_df = dataframe[
            (dataframe['account_name'].isin(accounts)) & 
            (dataframe['statement_end'] == end)
        ]

        if filtered_df.empty:
            raise Exception(f"No data found for account(s) {accounts} on date {end_date}")

        # Sum realized_total across all matching accounts
        realized_gains = filtered_df['realized_pl'].sum()

        return realized_gains

    except Exception as e:
        print(f"Something went wrong while getting Realized Gains: {e}")
        raise e

def get_unrealized_gains(dataframe, accounts, end_date):
    try:
        # Ensure date format is correct (e.g. 2002-30-07)
        end= dateparser.parse(end_date).strftime('%Y-%m-%d')

        # Filter for specific accounts and date
        filtered_df = dataframe[
            (dataframe['account_name'].isin(accounts)) & 
            (dataframe['statement_end'] == end)
        ]

        if filtered_df.empty:
            raise Exception(f"No data found for account(s) {accounts} on date {end_date}")

        # Sum realized_total across all matching accounts
        unrealized_gains = filtered_df['change_in_unrealized_pl'].sum()

        return unrealized_gains

    except Exception as e:
        print(f"Something went wrong while getting Unrealized Gains: {e}")
        raise e

def get_interest(dataframe, accounts, end_date):
    try:
        # Ensure date format is correct (e.g. 2002-30-07)
        end= dateparser.parse(end_date).strftime('%Y-%m-%d')

        # Filter for specific accounts and date
        filtered_df = dataframe[
            (dataframe['account_name'].isin(accounts)) & 
            (dataframe['statement_end'] == end)
        ]

        if filtered_df.empty:
            raise Exception(f"No data found for account(s) {accounts} on date {end_date}")

        # Sum realized_total across all matching accounts
        interest = filtered_df['interest'].sum()

        return interest

    except Exception as e:
        print(f"Something went wrong while getting Interest: {e}")
        raise e

def get_dividends(dataframe, accounts, end_date):
    try:
        # Ensure date format is correct (e.g. 2002-30-07)
        end= dateparser.parse(end_date).strftime('%Y-%m-%d')

        # Filter for specific accounts and date
        filtered_df = dataframe[
            (dataframe['account_name'].isin(accounts)) & 
            (dataframe['statement_end'] == end)
        ]

        if filtered_df.empty:
            raise Exception(f"No data found for account(s) {accounts} on date {end_date}")

        # Sum realized_total across all matching accounts
        dividends = sum(filtered_df['dividends'] + filtered_df['dividend_accruals'])

        return dividends

    except Exception as e:
        print(f"Something went wrong while getting Dividends: {e}")
        raise e

def get_top_down(dataframe, end_date, accounts):
    try:
        # Filter for the specific date
        filtered_df = dataframe[
            (dataframe['statement_end'] == end_date) &
            (dataframe['account_name'].isin(accounts))
            ].sum().to_frame().T

        # Regex pattern for snake_case: starts with lowercase, contains only lowercase, numbers and underscores
        snake_case_pattern = '^[a-z][a-z0-9_]*$'
        
        # Get list of columns that match snake_case pattern
        snake_case_columns = filtered_df.columns[filtered_df.columns.str.match(snake_case_pattern)]
        
        # Drop snake_case columns and sort remaining columns
        sorted_df = filtered_df.drop(columns=snake_case_columns).sort_values(
            by=filtered_df.index[0], 
            axis=1, 
            ascending=False
        )

        sorted_values = [{"security":security, "value": value} for security, value in sorted_df.iloc[0].items()]

        return sorted_values
    except Exception as e:
        print(f"Something went wrong while getting bottom-up stocks: {e}")
        raise e

def get_bottom_up(dataframe, end_date, accounts):
    try:
        # Filter for the specific date
        filtered_df = dataframe[
            (dataframe['statement_end'] == end_date) &
            (dataframe['account_name'].isin(accounts))
            ].sum().to_frame().T

        # Regex pattern for snake_case: starts with lowercase, contains only lowercase, numbers and underscores
        snake_case_pattern = '^[a-z][a-z0-9_]*$'
        
        # Get list of columns that match snake_case pattern
        snake_case_columns = filtered_df.columns[filtered_df.columns.str.match(snake_case_pattern)]
        
        # Drop snake_case columns and sort remaining columns
        sorted_df = filtered_df.drop(columns=snake_case_columns).sort_values(
            by=filtered_df.index[0], 
            axis=1, 
            ascending=True
        )
        
        sorted_values = [{"security": security, "value": value} for security, value in sorted_df.iloc[0].items()]

        return sorted_values

    except Exception as e:
        print(f"Something went wrong while getting bottom-up stocks: {e}")
        raise e

def get_security_values(dataframe, accounts, start_date, end_date, security):
    try:

        # Ensure date format is correct (e.g. 2002-30-07)
        start = dateparser.parse(start_date).strftime('%Y-%m-%d')
        end= dateparser.parse(end_date).strftime('%Y-%m-%d')

        filtered_df = dataframe[
            (dataframe['account_name'].isin(accounts)) & 
            (dataframe['statement_end'] >= start) &
            (dataframe['statement_end'] <= end)
        ].groupby('statement_end').sum()

        if filtered_df.empty:
            raise Exception(f"No data found for account(s) {accounts} from {start} to {end}")

        # Get dates and values as separate arrays
        dates = filtered_df.index.tolist()
        values = filtered_df[security.upper()].tolist()

        return {"date": dates, "value": values}

    except Exception as e:
        print(f"Something went wrong while getting values for {security} from {start_date} to {end_date}: {e}")
        raise e