import os
import sys

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(f"{dirname}/../nifiio"))
from nifiio import Nifiio

WRITE_TO_FILE_PATH = "C:/nifiio/files/broad_201904/"

broad_indices = ['NIFTY 50',
    'NIFTY NEXT 50',
    'NIFTY 100',
    'NIFTY 200',
    'NIFTY 500',
    'NIFTY MIDCAP 150',
    'NIFTY MIDCAP 50',
    'NIFTY MIDCAP 100',
    'NIFTY SMALLCAP 250',
    'NIFTY SMALLCAP 50',
    'NIFTY SMALLCAP 100',
    'NIFTY LARGEMIDCAP 250',
    'NIFTY MIDSMALLCAP 400']
strategy_indices = ['NIFTY100 Low Volatility 30',
    'NIFTY Alpha 50',
    'NIFTY Dividend Opportunities 50',
    'NIFTY Growth Sectors 15',
    'NIFTY High Beta 50',
    'NIFTY Low Volatility 50',
    'NIFTY Alpha Low-Volatility 30',
    'NIFTY Quality Low-Volatility 30',
    'NIFTY Alpha Quality Low-Volatility 30',
    'NIFTY Alpha Quality Value Low-Volatility 30',
    'NIFTY100 QUALITY 30',
    'NIFTY50 Value 20',
    'NIFTY500 VALUE 50']
# strategy_indices.append('NIFTY200 QUALITY 30')
sectoral_indices = ['NIFTY Auto',
    'NIFTY Bank',
    'NIFTY Financial Services',
    'NIFTY FMCG',
    'NIFTY IT',
    'NIFTY Media',
    'NIFTY Metal',
    'NIFTY Pharma',
    'NIFTY Private Bank',
    'NIFTY PSU Bank',
    'NIFTY Realty']

nii = Nifiio() # pylint: disable=not-callable

"""Loop over list of indices
"""
# for index in broad_indices:
#     # data = nii.get_nse_index_stocklist(index)
#     # data = nii.get_nse_index_weights(index)
#     data = nii.get_stocks_and_weights(index, write_to_file=True, file_types=['json', 'csv'], write_to_file_path=WRITE_TO_FILE_PATH)
#     if data is None:
#         print('Error fetching for index: {}'.format(index))
#     else:
#         print('Sample data for index: {}'.format(index))
#         # print(list(data.items())[1])
#         print(data[:1])

"""single index stocks and weights combined"""
data = nii.get_stocks_and_weights(index_name='NIFTY50 Value 20')

# single index stock list
# data = nii.get_nse_index_stocklist(index_name='NIFTY500 VALUE 50')

# for stock in data:
#     for k,v in stock.items():
#         print(k, ':', v)
#     print()

# single index weights only
# data = nii.get_nse_index_weights(index_name = 'NIFTY500 VALUE 50')
print(data)

"""single index stocks and weights combined and write to file"""
# nii.get_stocks_and_weights(index_name='NIFTY500 VALUE 50', write_to_file=True, file_types=['json', 'csv'], write_to_file_path=f"{dirname}/../files/")

#local testing
# from nii_local import NiiLocalDemo
# niil = NiiLocalDemo()
# data = niil.get_stocklist_with_weights(index_name='NIFTY 50', write_to_file=False)
# data = niil.parse_weight_file(index_name='NIFTY 50', write_to_file=True)
