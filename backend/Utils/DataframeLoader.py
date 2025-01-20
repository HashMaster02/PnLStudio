from Utils.db import get_all_records
from typing import List, Dict
import pandas as pd


async def load_dataframes():
    try:
        records = await get_all_records()

        if records is None:
            raise

        dataframes = {'total': pd.DataFrame(),
                      'realized_total': pd.DataFrame(),
                      'unrealized_total': pd.DataFrame()}

        for record in records:
            statement_data = record.model_dump()
            total_total_data = statement_data.pop('total_total')
            realized_total_data = statement_data.pop('realized_total')
            unrealized_total_data = statement_data.pop('unrealized_total')

            statement_df = construct_statement_df(statement_data)

            realized_total_df = construct_total_df(realized_total_data, statement_df)
            unrealized_total_df = construct_total_df(unrealized_total_data, statement_df)
            total_df = construct_total_df(total_total_data, statement_df)

            total_df.insert(loc=3, column='total_total', value=[total_total_data['value']])
            realized_total_df.insert(loc=3, column='realized_total', value=[realized_total_data['value']])
            unrealized_total_df.insert(loc=3, column='unrealized_total', value=[unrealized_total_data['value']])

            dataframes['total'] = pd.concat([dataframes['total'], total_df], axis=0, ignore_index=True)
            dataframes['realized_total'] = pd.concat([dataframes['realized_total'], realized_total_df], axis=0, ignore_index=True)
            dataframes['unrealized_total'] = pd.concat([dataframes['unrealized_total'], unrealized_total_df], axis=0, ignore_index=True)

        return dataframes
    except Exception as e:
        print(f"Something went wrong while loading data from the database: {e}")


def remove_properties(obj: Dict, properties: List[str]):
    for prop in properties:
        obj.pop(prop)


def construct_total_df(realized_total_data: Dict, statement_df: pd.DataFrame):
    try:
        exclude = ['id',
                   'total_total', 'total_total_id',
                   'unrealized_total', 'unrealized_total_id',
                   'realized_total', 'realized_total_id']
        remove_properties(realized_total_data, ['id', 'statement', 'statement_id'])

        # Add securities to dataframe
        for security_record in realized_total_data['securities']:
            remove_properties(security_record, exclude)
        sec_df = pd.DataFrame(realized_total_data['securities'])
        pivoted_sec_df = sec_df.pivot_table(index=[], columns='symbol', values='value', aggfunc='first', dropna=False)
        securities_df = pivoted_sec_df.reset_index(drop=True)

        # Prepend statement data
        realized_total_df = pd.concat([statement_df, securities_df], axis=1)
        return realized_total_df
    except Exception as e:
        print(f"Error while constructing realized total dataframe: {e}")
        raise


def construct_statement_df(statement_data: Dict):
    statement_data.pop('id')
    return pd.DataFrame([statement_data])
