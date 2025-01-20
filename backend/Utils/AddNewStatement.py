import asyncio
import pandas as pd
from pandas import DataFrame
from Utils.db import (add_new_statement, add_new_securities, statement_exists,
                      add_new_total_total, add_new_unrealized_total, add_new_realized_total)
from Utils.fileprocessor import FileProcessor


def split_df(dataframe: DataFrame):
    """
    This function takes a dataframe containing processed trades data
    and splits it into 2 dataframes: One contains the Statement Information
    and the other contains all the Securities.
    """

    snake_case_pattern = r'^[a-z]+(_[a-z]+)*$'  # Matches snake_case
    uppercase_pattern = r'^[A-Z_]+$'  # Matches UPPERCASE

    # Filter columns based on patterns
    statement_info = dataframe.filter(regex=snake_case_pattern, axis=1)
    securities = dataframe.filter(regex=uppercase_pattern, axis=1)
    return {"statement_info": statement_info, "security_info": securities}


async def add_data():
    try:

        fileproc = FileProcessor('trades', debug_level=0)
        files = fileproc.get_csv_files()

        trade_data = {}

        for file in files:
            df = fileproc.load_prepared_data(file)
            trade_data[file.strip('.csv')] = split_df(df)

        statement_data = []
        for data_type, frames in trade_data.items():
            statement_data.append(frames['statement_info'])

        # Construct Statement dataframe
        statement_info_df = pd.concat(statement_data, axis=1)  # concatenate dataframes along columns
        statement_info = statement_info_df.loc[:,
                         ~statement_info_df.columns.duplicated()]  # remove duplicate columns by keeping the first occurrence

        # Get remaining dataframes
        realized_total = trade_data['realized_total']['security_info']
        unrealized_total = trade_data['unrealized_total']['security_info']
        total = trade_data['total']['security_info']

        for i in range(len(statement_info.index)):
            statement_data = statement_info.iloc[i].to_dict()

            # If the statement exists, no need to process any of it again
            if await statement_exists(statement_data):
                continue

            total_total_val = statement_data.pop('total_total')
            realized_total_val = statement_data.pop('realized_total')
            unrealized_total_val = statement_data.pop('unrealized_total')

            # Add Statement record to DB
            statement_record = await add_new_statement(statement_data)

            # Add RealizedTotal record to DB
            realized_total_record = await add_new_realized_total({
                'statement_id': statement_record.id,
                'value': realized_total_val
            })

            # Add all RealizedTotal Securities to DB
            await add_new_securities(
                list(
                    map(lambda tup: {
                        "symbol": tup[0],
                        "value": tup[1],
                        "realized_total_id": realized_total_record.id
                    },
                        realized_total.iloc[i].items()
                        )
                )
            )

            # Add UnrealizedTotal record to DB
            unrealized_total_record = await add_new_unrealized_total({
                'statement_id': statement_record.id,
                'value': unrealized_total_val
            })

            # Add all UnrealizedTotal Securities to DB
            await add_new_securities(
                list(
                    map(lambda tup: {
                        "symbol": tup[0],
                        "value": tup[1],
                        "unrealized_total_id": unrealized_total_record.id
                    },
                        unrealized_total.iloc[i].items()
                        )
                )
            )

            # Add TotalTotal record to DB
            total_total_record = await add_new_total_total({
                'statement_id': statement_record.id,
                'value': total_total_val
            })

            # Add all TotalToal Securities to DB
            await add_new_securities(
                list(
                    map(lambda tup: {
                        "symbol": tup[0],
                        "value": tup[1],
                        "total_total_id": total_total_record.id
                    },
                        total.iloc[i].items()
                        )
                )
            )

    except Exception as e:
        print(f"Error while adding new data to db: {e}")

if __name__ == '__main__':
    asyncio.run(add_data())
