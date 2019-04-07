"""
MIT License

Copyright (c) 2019 lamavar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json, csv
import re
import requests
import os
from constants import (nse_stock_list_url_dict, nse_weight_regex_pattern, index_weight_url, stock_list_url)

class Nifiio:
    def __init__(self):
        self.json_ext = '.json'
        self.csv_ext = '.csv'
        self.weightage_field_name = 'Weightage'
        
    def get_nse_index_weights(self, index_name):
        """
        Returns a dictionary of all the stocks and their corresponding weights in the index.

        :param index_name: Name of the index
        :rtype: dict
        """
        #prepare and send request to fetch data
        print("Fetching data for index {}".format(index_name))
        url = index_weight_url.format(index_name.upper())
        # print('URL: {}'.format(url))         
        response = requests.get(url, timeout=10)
        print('Request URL: {}'.format(response.url))
        response_text = None
        
        if response.status_code != 200:
            print('Failed to get data: ', response.status_code)
            return None
        else:
            response_text = response.text
            
            #Compile regex and search in response text to fetch 'label:' <weight> from response 
            if response_text is not None:
                print('Response received - parsing')
                # nse_json_regex_pattern = self.nse_weight_regex_pattern
                # pattern = re.compile(nse_json_regex_pattern)
                index_weight_data = nse_weight_regex_pattern.findall(response_text)
                # print(index_weight_data)

                #convert to dict form
                weight_data_dict = dict(st.rsplit(' ', 1) for st in index_weight_data)
                # print(weight_data_dict)
                weight_int_dict =\
                            {key : float(value.replace('%','')) for key, value in weight_data_dict.items()}
                
                return weight_int_dict
            else:
                print('Error: Response is empty!')
                return None
    
    
    def get_nse_index_stocklist(self, index_name):
        """
        Returns a list of stocks in the index as a list of `OrderedDict` types.
        Each `OrderedDict` represents information of a stock in the index. Weights are not included.
        
        :param index_name: Name of the index
        :rtype: OrderedDict
        """
        #prepare and send request to fetch data
        if index_name in nse_stock_list_url_dict:
            url = nse_stock_list_url_dict.get(index_name)
        else:
            trim_index_name = re.sub(r'\s+', '', index_name)
            print("Fetching list of stocks for index {}".format(index_name))
            url = stock_list_url.format(trim_index_name.lower())

        response = requests.get(url, timeout=10)
        print('Request URL: {}'.format(response.url))

        if response.status_code != 200:
            print('Failed to get data: ', response.status_code)
            return None
        else:
            response_text_split = response.text.splitlines()
            if response is not None:
                print('Response received - reading csv')            
                reader = csv.DictReader(response_text_split)
                stock_list = list(reader)                                
                return stock_list
            else:
                print('Error: Response is empty!')
                return None

    def get_stocks_and_weights(self, index_name, write_to_file=False, file_types=None, write_to_file_path=None):
        """Combines fetched stock data together with weights for a more comprehensive list containing details of stocks in the index, each stock represented by an `OrderedDict`.
        Data fetched can also be written to csv and json depending on the optional params.
        
        :param index_name: Name of the index
        :rtype: OrderedDict       
        """
        
        stock_list = self.get_nse_index_stocklist(index_name = index_name)
        weight_dict = self.get_nse_index_weights(index_name = index_name)
        trim_index_name = re.sub(r'\s+', '', index_name)

        if stock_list is None or weight_dict is None:
            print('Couldn\'t fetch stock data and/or weights!')
            return None

        # merge weight from list of weights into stock data using symbol
        print('Merging weights and stock info')
        for stock in stock_list:
            symbol = stock.get('Symbol')
            # print('Getting weight for symbol: {}'.format(symbol))
            weight = weight_dict.get(symbol)
            # print('Weight for {0} is {1}'.format(symbol, weight))
            stock[self.weightage_field_name] = weight
        
        if write_to_file is True:
            write_to_file_path = '' if write_to_file_path is None else str(write_to_file_path)
            if not os.path.isdir(write_to_file_path) and write_to_file_path is not None:
                print('Creating new directory')
                try:
                    os.makedirs(write_to_file_path)
                except OSError:
                    print('Error creating directory!')
                    return stock_list

            if 'csv' in file_types:
                print('Writing to csv file.')
                output_file = write_to_file_path + 'index_data_weights_{}'.format(trim_index_name) + self.csv_ext

                #get field names from stock list    
                for stock in stock_list[:1]:
                    field_names = list(stock.keys())

                with open(output_file, 'w', newline='') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=field_names)
                    print('Field names: ', field_names)
                    writer.writeheader()
                    writer.writerows(stock_list)
            
            if 'json' in file_types:
                print('Writing to json file.')
                output_file = write_to_file_path + 'index_data_weights_{}'.format(trim_index_name) + self.json_ext

                with open(output_file, 'w') as outfile:
                    json.dump(stock_list, outfile)            
        else:
            print('Skipped writing to file')

        return stock_list