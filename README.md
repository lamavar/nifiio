# nifiio
Python scraper to obtain detailed information about NSE (Nifty) indices. For a given index this can be used to obtain:
* Stock name
* Industry/Sector
* Symbol
* ISIN Code
* Weight in Index

## Requirements
* Python 3.6
* Python libraries: requests, re, csv and json

## Usage

### To get weight information using a stock's NSE symbol
```
>>> from nifiio import Nifiio
>>> nii = Nifiio()
>>> weights = nii.get_nse_index_weights('NIFTY 50')
>>> weights.get('HDFCBANK')
10.33
```

### To get the list of stocks in an index with related information like Industry/Sector and ISIN, and their respective weights
```
>>> data = nii.get_stocks_and_weights(index_name='NIFTY50 Value 20')
>>>	for stock in data:
>>>		for k,v in stock.items():
>>>			print(k, ':', v)
>>>		print()

Company Name : Bajaj Auto Ltd.
Industry : AUTOMOBILE
Symbol : BAJAJ-AUTO
Series : EQ
ISIN Code : INE917I01010
Weightage : 2.8

Company Name : Bharat Petroleum Corporation Ltd.
Industry : ENERGY
Symbol : BPCL
Series : EQ
ISIN Code : INE029A01011
Weightage : 1.92
...
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments
