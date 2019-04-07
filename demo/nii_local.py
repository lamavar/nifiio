import json, csv
import re
import os

class NiiLocalDemo:

    def __init__(self):
        self.local_file_base_path = 'C:/nifiio/files/'
        self.input_file_dir = 'input_files/'
        self.output_file_dir = 'output_files/'
        self.weight_file_path = 'C:/nifiio/files/SectorialIndexData{0}.js'
        self.stocklist_file_path = 'C:/nifiio/files/ind_{0}list.csv'
        self.nse_weight_regex_pattern = '"label":"(.*?)"'
        self.json_ext = '.json'
        self.csv_ext = '.csv'
        self.weightage_field_name = 'Weightage'

    def get_stocklist_with_weights(self, index_name, write_to_file=False, file_types=None, write_to_file_path=None):
        
        stock_list = self.parse_stocklist_file(index_name = index_name)
        weight_dict = self.parse_weight_file(index_name = index_name)
        trim_index_name = re.sub(r'\s+', '', index_name)

        # merge weight from list of weights into stock data using symbol
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
                except Exception as ex:
                    print(ex)
                    print('Error creating directory!')

            if 'csv' in file_types:
                print('Writing to csv file.')
                # field_names.append(self.weightage_field_name)
                # output_file\
                #     = self.local_file_base_path + self.output_file_dir\
                #     + 'index_data_weights_{}'.format(trim_index_name) + self.csv_ext
                output_file = write_to_file_path + 'index_data_weights_{}'.format(trim_index_name) + self.csv_ext
                #get field names from stock list    
                for stock in stock_list[:1]:
                    # print("Stocklist iteration")
                    field_names = list(stock.keys())

                with open(output_file, 'w', newline='') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=field_names)
                    print('Fieldnames: ', field_names)
                    writer.writeheader()
                    writer.writerows(stock_list)

            if 'json' in file_types:
                print('Writing to json file.')
                # output_file\
                #     = self.local_file_base_path + self.output_file_dir\
                #     + 'index_data_weights_{}'.format(trim_index_name) + self.json_ext
                output_file = write_to_file_path + 'index_data_weights_{}'.format(trim_index_name) + self.json_ext
                with open(output_file, 'w') as outfile:
                    json.dump(stock_list, outfile)
        else:
            print('Skipped writing to file')

        return stock_list
    
    def parse_stocklist_file(self, index_name):

        trim_index_name = re.sub(r'\s+', '', index_name)
        file_path = self.stocklist_file_path.format(trim_index_name.lower())
        print('Reading csv file: ', file_path)

        with open(file_path, newline='') as infile:
            reader = csv.DictReader(infile)
            stock_list = list(reader)
            # field_names = list(reader.fieldnames)
        
        return stock_list

    def parse_weight_file(self, index_name):        
        
        weight_regex_pattern = self.nse_weight_regex_pattern
        w_file_path = self.weight_file_path.format(index_name)
        print('File path: ', w_file_path)

        with open(w_file_path) as dataFile:
            file_text = dataFile.read()

        # print(fileText)
        pattern = re.compile(weight_regex_pattern)
        index_weight_data = pattern.findall(file_text)

        # label field in file contains data in the form "label": "<symbol><whitepace><weight%>""
        # convert to dict form by splitting label values separated by whitespace
        weight_data_dict = dict(st.rsplit(' ', 1) for st in index_weight_data)
        # print(weight_data_dict)
        # strip out the percentage sign from weight and convert to float
        weight_int_dict =\
                    {key : float(value.replace('%','')) for key, value in weight_data_dict.items()}
          
        return weight_int_dict