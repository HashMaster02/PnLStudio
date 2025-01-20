import os
import csv
import pandas as pd
import numpy as np
from dateutil import parser as dateparser


class FileProcessor:

    def __init__(self, trades_dir=None, debug_level=1):

        # Setup directories
        if trades_dir is None:
            trades_dir = 'trades'

        self.root_dir = os.getcwd()
        self.trades_dir = os.path.join(self.root_dir, trades_dir)
        self.debug_level = debug_level

        # Verify directories exist
        if not os.path.exists(self.trades_dir):
            raise FileNotFoundError(f"Trades directory not found: {self.trades_dir}")

    def debug_print(self, message, level=1):
        """
        Print debug messages based on debug level
        level 0: no debug output
        level 1: function entry/exit
        level 2: summary information
        level 3: detailed debugging
        """
        if self.debug_level >= level:
            print(f"[DEBUG-L{level}] {message}")

    def extract_trade_data(self, file):
        """Parse CSV file and extract trade data including the statement and account info,
            and a pandas dataframe with the trade data."""

        self.debug_print("Entering parse_csv()", 1)

        file_path = os.path.join(self.trades_dir, file)

        # First pass: get statement and account information
        statement_info = {}
        account_info = {}

        self.debug_print(f"Opening file: {file_path}", 2)
        with open(file_path, 'r') as file:
            # Print first few rows for debugging
            self.debug_print("First few rows of the file:", 2)
            for i, line in enumerate(file):

                if i < 5:  # Print first 5 rows
                    self.debug_print(f"Row {i}: {line.strip()}", 2)
                row = next(csv.reader([line]))

                # Stop scanning if we are no longer in the Statement or Account Information section
                if not any('Statement' in str(cell) or 'Account Info' in str(cell) for cell in row):
                    break

                # Try to get all statement information
                if 'Statement' in row and row[1] != 'Header':
                    self.debug_print(f"Row Found for Statement: {row}", 2)
                    if len(row) >= 4 and row[0] == 'Statement' and row[2] == 'Period':
                        statement_period = self.parse_statement_period(row)
                        statement_info.update(statement_period)
                        if statement_period:
                            self.debug_print(f"Successfully parsed statement period: {statement_period}", 2)
                    else:
                        label, value = self.parse_statement_info(row)
                        statement_info.setdefault(label, value)
                        if label and value:
                            self.debug_print(f"Successfully parsed statement {label}: {value}", 2)

                # Try to get all account information
                if 'Account Information' in row and row[1] != 'Header':
                    self.debug_print(f"Row Found for Account Information: {row}", 2)
                    label, value = self.parse_account_info(row)
                    account_info.setdefault(label, value)
                    if label and value:
                        self.debug_print(f"Successfully parsed account {label}: {value}", 2)

        self.debug_print("Statement period not found in database, continuing with full processing", 2)

        filtered_rows = []
        parsed_symbols = []
        errors = []
        headers = None

        # Second pass: process all trade data
        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            self.debug_print("Starting full CSV parsing...", 2)
            row_count = 0

            for row in reader:
                row_count += 1
                self.debug_print(f"Processing row {row_count}: {row}", 3)

                # Find headers
                if len(row) >= 2 and 'Realized & Unrealized Performance Summary' in row[0] and row[1] == 'Header':
                    headers = row
                    self.debug_print(f"Found headers: {headers}", 2)
                    continue

                # Process trade data
                if headers and len(row) >= 3 and 'Realized & Unrealized Performance Summary' in row[0]:
                    trade_type = row[2]
                    if any(type_match in trade_type for type_match in
                           ['Stocks', 'Equity and Index Options', 'Futures']):
                        try:
                            symbol_data = self.parse_symbol(row[3], trade_type)
                            filtered_rows.append(row)
                            parsed_symbols.append(symbol_data)
                            self.debug_print(f"Found matching trade type: {trade_type}", 2)
                        except ValueError as ve:
                            errors.append(f"Row {row_count}: {str(ve)}")
                            self.debug_print(f"Error processing row {row_count}: {str(ve)}", 1)

        if errors:
            error_msg = "\n".join(errors)
            self.debug_print(f"Encountered errors while processing:\n{error_msg}", 1)
            raise ValueError(f"Failed to process some futures symbols:\n{error_msg}")

        if not filtered_rows:
            self.debug_print("No matching trade data found in the CSV", 1)
            raise ValueError("No matching trade data found in the CSV")

        # Create DataFrame with proper headers
        df = pd.DataFrame(filtered_rows, columns=headers)

        # Add symbol component columns
        symbol_df = pd.DataFrame(parsed_symbols)

        # Combine the original data with parsed symbol components
        df = pd.concat([df, symbol_df], axis=1)

        self.debug_print("Exiting parse_csv()", 1)
        return df, statement_info, account_info

    def load_prepared_data(self, file):
        '''Load data from a prepared CSV file into a pandas dataframe'''

        try:
            file_path = os.path.join(self.trades_dir, file)
            
            df = pd.read_csv(file_path).replace({np.nan: None})

            return df
        except:
            print(f"Something went wrong while loading prepared CSV file: {e}" )
            raise

    def parse_statement_info(self, row):
        """Parse statement information (excluding period) from row"""
        self.debug_print("Entering parse_statement_period()", 1)
        statement_labels = {"BrokerName": "broker",
                            "BrokerAddress": "broker_address",
                            "WhenGenerated": "date_generated",
                            "Title": "title",
                            }

        try:
            if len(row) >= 4 and row[0] == 'Statement':
                if row[2] == 'WhenGenerated':
                    split_string = row[3].split(" ")
                    date_time, timezone = " ".join(split_string[:-1]), split_string[-1]
                    label, value = statement_labels[row[2]], dateparser.parse(date_time).strftime('%Y-%m-%d, %H:%M:%S')
                    self.debug_print(f"Found {label}: {value} {timezone}", 2)
                    return label, f"{value} {timezone}"
                else:
                    label, value = statement_labels[row[2]], row[3]
                    self.debug_print(f"Found {label}: {value}", 2)
                    return label, value
        except Exception as e:
            self.debug_print(f"Error parsing statement information: {str(e)}", 1)
            return None

        self.debug_print("Exiting parse_statement_information()", 1)
        return None

    def parse_statement_period(self, row):
        """Parse statement period from row"""
        self.debug_print("Entering parse_statement_period()", 1)

        try:
            date_str = row[3].strip('"').strip()
            dates = [d.strip() for d in date_str.split('-')]

            try:
                # Parse first date
                start_date = dateparser.parse(dates[0]).strftime('%Y-%m-%d')

                # If range exists, parse second date, otherwise use start date
                end_date = dateparser.parse(dates[1]).strftime('%Y-%m-%d') if len(dates) > 1 else start_date

                self.debug_print(f"Found statement period: {start_date} to {end_date}", 2)
                return {'start_date': start_date, 'end_date': end_date}

            except (ValueError, IndexError) as e:
                self.debug_print(f"Error parsing date string: {str(e)}", 1)
                return None

        except Exception as e:
            self.debug_print(f"Error parsing statement period: {str(e)}", 1)
            return None

    def parse_account_info(self, row):
        """
        Parse account information from the Account Information row
        Expected format: 'Account Information' in first column, 'Account' in third column
        Account number will be in fourth column
        """
        account_labels = {"Name": "holder",
                          "Account": "id",
                          "Account Type": "type",
                          "Customer Type": "customer_type",
                          "Account Capabilities": "capabilities",
                          "Base Currency": "base_currency"
                          }
        try:
            if len(row) >= 4 and row[0] == 'Account Information':
                label, value = account_labels[row[2]], row[3]
                self.debug_print(f"Found {label}: {value}", 2)
                return label, value
        except Exception as e:
            self.debug_print(f"Error parsing account info: {str(e)}", 1)
        return None

    def parse_symbol(self, symbol, trade_type):
        """
        Parse symbol based on trade type and return a dictionary of components
        Args:
            symbol: The trading symbol
            trade_type: Type of trade (Stocks, Equity and Index Options, Futures)
        Returns:
            Dictionary containing symbol components and underlying
        Raises:
            ValueError: If a futures symbol is not found in the replacement dictionary
        """
        self.debug_print("Entering parse_symbol()", 1)
        self.debug_print(f"Processing symbol: {symbol}, trade_type: {trade_type}", 3)

        try:
            result = {
                'original_symbol': symbol.lower(),
                'trade_type': trade_type,
                'underlying': None,
                'expiry': None,
                'strike': None,
                'option_type': None
            }

            replacement_dict = {
                # CL replacements
                'CLN4': 'cl', 'CLQ4': 'cl', 'MCLN4': 'cl', 'MCLV4': 'cl', 'MCLX4': 'cl', 'MCLZ4': 'cl', 'MCLF5': 'cl',
                # M2K replacements
                'M2KM4': 'm2k', 'M2KU4': 'm2k', 'M2KZ4': 'm2k',
                # MES replacements
                'MESM4': 'mes', 'M3SU4': 'mes', 'MESZ4': 'mes', 'MESU4': 'mes',
                # MGC replacements
                'MGCQ4': 'mgc', 'MGCV4': 'mgc', 'MGCZ4': 'mgc', 'MGCG5': 'mgc',
                # MHG replacements
                'MHGQ4': 'mhg', 'MHGV4': 'mhg', 'MHGX4': 'mhg', 'MHGZ4': 'mhg', "MHGN4": 'mhg',
                # MNQ replacements
                'MNQM4': 'mnq', 'MNQU4': 'mnq', 'MNQZ4': 'mnq',
                # MNG replacements
                'MNGQ4': 'mng', 'MNGV4': 'mng', 'MNGZ4': 'mng', 'MNGN4': 'mng',
                # Other replacements
                'QIU4': 'qi',
                'YMU4': 'ym'
            }

            if trade_type == 'Stocks':
                result['underlying'] = symbol.lower()
                self.debug_print(f"Stock trade - using symbol as underlying: {symbol}", 2)

            elif trade_type == 'Equity and Index Options':
                components = symbol.split()
                if len(components) >= 4:
                    result.update({
                        'underlying': components[0].lower(),
                        'expiry': components[1].lower(),
                        'strike': components[2],
                        'option_type': components[3].lower()
                    })
                    self.debug_print(f"Option components parsed: {result}", 2)
                else:
                    self.debug_print(f"Invalid option format: {symbol}", 2)
                    result['underlying'] = symbol

            elif trade_type == 'Futures':
                if symbol in replacement_dict:
                    result['underlying'] = replacement_dict[symbol]
                    self.debug_print(f"Futures trade - mapped {symbol} to {result['underlying']}", 2)
                else:
                    error_msg = f"No mapping found for futures symbol: {symbol}"
                    self.debug_print(f"Error: {error_msg}", 1)
                    raise ValueError(error_msg)

            else:
                result['underlying'] = symbol
                self.debug_print(f"Unknown trade type: {trade_type}, using original symbol", 2)

            return result

        except ValueError as ve:
            # Re-raise ValueError for futures mapping errors
            raise
        except Exception as e:
            self.debug_print(f"Error processing symbol {symbol}: {str(e)}", 1)
            return {'original_symbol': symbol, 'underlying': symbol, 'trade_type': trade_type}
        finally:
            self.debug_print("Exiting parse_symbol()", 1)

    def extract_nav_values(self, file):
        """Extract NAV and related values from CSV file"""
        self.debug_print("Entering extract_nav_values()", 1)
        file_path = os.path.join(self.trades_dir, file)

        # Initialize with default values (0.0)
        nav_values = {
            'ending_value': 0.0,
            'time_weighted_rr': 0.0,
            'starting_value': 0.0,
            'realized_pl': 0.0,
            'change_in_unrealized_pl': 0.0,
            'transferred_pl_adjustments': 0.0,
            'deposits_and_withdrawals': 0.0,
            'position_transfers': 0.0,
            'dividends': 0.0,
            'withholding_tax': 0.0,
            'dividend_accruals': 0.0,
            'interest': 0.0,
            'interest_accruals': 0.0,
            'other_fee': 0.0
        }

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    row = next(csv.reader([line]))
                    self.debug_print(f"Processing row: {row}", 3)

                    if len(row) >= 4:  # Ensure row has enough columns
                        # Handle Change in NAV rows
                        if row[0] == 'Change in NAV':
                            field_mapping = {
                                'Starting Value': 'starting_value',
                                'Ending Value': 'ending_value',
                                'Realized P/L': 'realized_pl',
                                'Change in Unrealized P/L': 'change_in_unrealized_pl',
                                'Transferred P/L Adjustments': 'transferred_pl_adjustments',
                                'Deposits & Withdrawals': 'deposits_and_withdrawals',
                                'Position Transfers': 'position_transfers',
                                'Dividends': 'dividends',
                                'Withholding Tax': 'withholding_tax',
                                'Change in Dividend Accruals': 'dividend_accruals',
                                'Interest': 'interest',
                                'Change in Interest Accruals': 'interest_accruals',
                                'Other Fees': 'other_fee'
                            }

                            if row[2] in field_mapping:
                                try:
                                    value = float(row[3].replace(',', '').replace('$', ''))
                                    nav_values[field_mapping[row[2]]] = value
                                    self.debug_print(f"Found {field_mapping[row[2]]}: {value}", 2)
                                except ValueError:
                                    self.debug_print(f"Could not convert value for {row[2]}: {row[3]}", 2)

                        # Handle Time Weighted Rate of Return
                        elif row[0] == 'Time Weighted Rate of Return':
                            try:
                                value = float(row[3].replace('%', '').replace(',', ''))
                                nav_values['time_weighted_rr'] = value
                                self.debug_print(f"Found time_weighted_rr: {value}", 2)
                            except ValueError:
                                self.debug_print(f"Could not convert Time Weighted RR: {row[3]}", 2)

            self.debug_print("NAV values extracted:", 2)
            for key, value in nav_values.items():
                self.debug_print(f"{key}: {value}", 2)

            return nav_values

        except Exception as e:
            self.debug_print(f"Error extracting NAV values: {str(e)}", 1)
            return nav_values  # Return dictionary with default values if there's an error
        finally:
            self.debug_print("Exiting extract_nav_values()", 1)

    def get_csv_files(self):
        files = []
        for file in os.listdir(self.trades_dir):
            if file.endswith('.csv') and os.path.isfile(os.path.join(self.trades_dir, file)):
                files.append(file)

        return files
