import re

nse_stock_list_url_dict = {
            "NIFTY100 Low Volatility 30" : "https://www.nseindia.com/content/indices/ind_Nifty100LowVolatility30list.csv",
            "NIFTY100 QUALITY 30" : "http://www.niftyindices.com/IndexConstituent/ind_nifty100Quality30list.csv",
            "NIFTY Alpha 50" : "https://www.nseindia.com/content/indices/ind_nifty_Alpha_Index.csv",
            "NIFTY Dividend Opportunities 50" : "https://www.nseindia.com/content/indices/ind_niftydivopp50list.csv",
            "NIFTY Growth Sectors 15" : "https://www.nseindia.com/content/indices/ind_NiftyGrowth_Sectors15_Index.csv",
            "NIFTY High Beta 50" : "https://www.nseindia.com/content/indices/nifty_High_Beta50_Index.csv",
            "NIFTY Low Volatility 50" : "https://www.nseindia.com/content/indices/nifty_Low_Volatility50_Index.csv",
            "NIFTY Alpha Low-Volatility 30" : "http://www.niftyindices.com/IndexConstituent/ind_nifty_alpha_lowvol30list.csv",
            "NIFTY Quality Low-Volatility 30" : "http://www.niftyindices.com/IndexConstituent/ind_nifty_quality_lowvol30list.csv",
            "NIFTY50 Value 20" : "http://www.niftyindices.com/IndexConstituent/ind_Nifty50_Value20.csv",
            "NIFTY500 VALUE 50" : "http://www.niftyindices.com/IndexConstituent/ind_nifty500Value50_list.csv",
            "NIFTY200 QUALITY 30" : "http://www.niftyindices.com/IndexConstituent/ind_nifty200Quality30_list.csv",
            "NIFTY Alpha Quality Value Low-Volatility 30" : "http://www.niftyindices.com/IndexConstituent/ind_nifty_alpha_quality_value_lowvol30list.csv",
            "NIFTY Alpha Quality Low-Volatility 30" : "http://www.niftyindices.com/IndexConstituent/ind_nifty_alpha_quality_lowvol30list.csv",
            "NIFTY Financial Services" : "https://www.nseindia.com/content/indices/ind_niftyfinancelist.csv",
            "NIFTY Private Bank" : "https://www.nseindia.com/content/indices/ind_nifty_privatebanklist.csv"
        } 

nse_weight_regex_pattern = re.compile('"label":"(.*?)"')

stocks_csv_url = 'http://www.nseindia.com/content/equities/EQUITY_L.csv'
index_weight_url = 'http://iislliveblob.niftyindices.com/jsonfiles/SectorialIndex/SectorialIndexData{0}.js'
stock_list_url = 'https://www.nseindia.com/content/indices/ind_{0}list.csv'