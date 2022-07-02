#Imports
import pandas as pd
import os
import streamlit as st
import numpy as np
import datetime as dt
from twelvedata import TDClient
from opensea import OpenseaAPI
from opensea import utils
from MCForecastTools import MCSimulation 


#All Functions


#Opensea API Key
opensea_api = OpenseaAPI(apikey="7913a9c0377249d2998900d7ce6d38b3")   #University of Toronto's API KEY. I applied for an opensea api but have not received it yet

#Twelve Data API Key
td = TDClient(apikey="d1d0c43b0fb445518d1435c2b90c9cdc") 

#Cryptocurrency DF Function
def create_ts(user_inputc, td):
        ts = td.time_series(
            symbol = user_inputc,
            exchange = "Binance",
            interval = '1day',
            outputsize=5000,
            start_date = '2020-01-15',
            end_date = dt.date.today(),
            timezone="America/New_York",
            )
        crypto_df = ts.as_pandas()
        crypto_df = crypto_df.round(2)
        return crypto_df

#BTC DataFrame
btc = td.time_series(
        symbol = 'BTC/USD',
        exchange = "Binance",
        interval = '1day',
        outputsize=5000,
        start_date = '2020-01-01',
        end_date = dt.date.today(),
        timezone="America/New_York",
        )
btc_df = btc.as_pandas()
btc_df = btc_df.round(2)
        
    #ETH DataFrame
eth = td.time_series(
        symbol = 'ETH/USD',
        exchange = "Binance",
        interval = '1day',
        outputsize=5000,
        start_date = '2020-01-01',
        end_date = dt.date.today(),
        timezone="America/New_York",
        )
eth_df = eth.as_pandas()
eth_df = eth_df.round(2)

#XRP DataFrame
xrp = td.time_series(
        symbol = 'XRP/USD',
        exchange = "Binance",
        interval = '1day',
        outputsize=5000,
        start_date = '2020-01-01',
        end_date = dt.date.today(),
        timezone="America/New_York",
        )
xrp_df = xrp.as_pandas()
xrp_df = xrp_df.round(2)

#BNB DataFrame
bnb = td.time_series(
        symbol = 'BNB/USD',
        exchange = "Binance",
        interval = '1day',
        outputsize=5000,
        start_date = '2020-01-01',
        end_date = dt.date.today(),
        timezone="America/New_York",
        )
bnb_df = bnb.as_pandas()
bnb_df = bnb_df.round(2)

#SOL DataFrame
sol = td.time_series(
        symbol = 'SOL/USD',
        exchange = "Binance",
        interval = '1day',
        outputsize=5000,
        start_date = '2020-01-01',
        end_date = dt.date.today(),
        timezone="America/New_York",
        )
sol_df = sol.as_pandas()
sol_df = sol_df.round(2)

#ADA DataFrame
ada = td.time_series(
        symbol = 'ADA/USD',
        exchange = "Binance",
        interval = '1day',
        outputsize=5000,
        start_date = '2020-01-01',
        end_date = dt.date.today(),
        timezone="America/New_York",
        )
ada_df = ada.as_pandas()
ada_df = ada_df.round(2)

#LUNA DataFrame
luna = td.time_series(
        symbol = 'LUNAt/USD',
        exchange = "Binance",
        interval = '1day',
        outputsize=5000,
        start_date = '2020-01-01',
        end_date = dt.date.today(),
        timezone="America/New_York",
        )
luna_df = luna.as_pandas()
luna_df = luna_df.round(2)

