import pandas as pd
import datetime as dt


class MarketTable:
    def __init__(self, currency_json, json_status=None):

        self.currency_json = currency_json
        self.json_status = json_status
        self.num_of_markets = None

    def get_table_comment(self, currency):

        # gets the dataframe
        markets_data_frame = self.create_market_df()
        table_row = ""

        # abstracts the market type and price from the dataframe
        for index, row in markets_data_frame.iterrows():
            # stores the currency type and currency price info
            currency_type = str(markets_data_frame.loc[index, 'market'])
            currency_price = str(round(float(markets_data_frame.loc[index, 'price']), 2))

            # adds a 0 if the last digit after the decimal is 1 digit long
            if len(currency_price.split(".")[1]) == 1:
                currency_price = currency_price + "0"

            # creates the string for the market type and the rounded price
            table_row = table_row + currency_type + "|" + "$" + currency_price + "\n"

        # putting together the table names
        column_names = "Market | Price (USD) per 1 unit\n"
        cell_alignment = ":-----------:|:-----------:\n"

        complete_table = '**Top ' + str(markets_data_frame.shape[0]) + " " + currency.upper() + ' Exchanges @ ' \
                         + str(dt.datetime.now().strftime(
            '%Y %b %d | %I:%M%p EST')) + "**" + '\n\n' + column_names + cell_alignment + table_row

        if markets_data_frame.shape[0] > 2:
            return complete_table
        else:
            return False

    def create_market_df(self):

        # converts the market portion of the dictionary into a list
        markets_list = self.currency_json['ticker']['markets']
        # only go through the rest of the code if there are at least 2 market exchange data AND
        # also if 'success' is not false
        markets_df = pd.DataFrame(markets_list)

        # sorts the value and then resets the index values in ascending form
        markets_df.sort_values('price', ascending=False, inplace=True)
        markets_df.reset_index(drop=True, inplace=True)

        # makes a list of rows to drop
        index_to_delete = []
        for index, row in markets_df.iterrows():

            # value of the row 'index' within the column volume
            if markets_df.loc[index, 'volume'] <= 50:
                index_to_delete.append(int(index))

        markets_df.drop(markets_df.index[index_to_delete], axis=0, inplace=True)
        markets_df.drop('volume', axis=1, inplace=True)

        # creates a dataframe that is the top 5 market with correct index
        if markets_df.shape[0] < 5:
            markets_df = markets_df.head(markets_df.shape[0])
        else:
            markets_df = markets_df.head(5)

        return markets_df

    # gets the status of the json file
    def get_json_status(self):
        # converts the market portion of the dictionary into a list
        if self.currency_json['success'] is False:
            self.json_status = False
        else:
            markets_list = self.currency_json['ticker']['markets']
            # checking to see if there is enough markets to pass the json status
            if len(markets_list) < 2:
                self.json_status = False
            else:
                self.json_status = True

        return self.json_status
