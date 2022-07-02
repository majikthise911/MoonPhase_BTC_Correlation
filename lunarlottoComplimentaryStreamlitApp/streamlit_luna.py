from matplotlib.pyplot import table
import pandas as pd
import os
import streamlit as st
import numpy as np
import datetime as dt
from twelvedata import TDClient
from opensea import OpenseaAPI
from opensea import utils
from MCForecastTools import MCSimulation 
import yfinance as yf
import CustomModule as cm

st.sidebar.header("""LunarLotto Crypto Search Web App""")
selected_crypto = st.sidebar.text_input("Enter a valid crypto ticker...")

button_clicked = st.sidebar.button("SEARCH")

#opensea api key
opensea_api = OpenseaAPI(apikey="7913a9c0377249d2998900d7ce6d38b3") #University of Toronto's API KEY. I applied for an opensea api but have not received it yet
#twelvedata api key
td = TDClient(apikey="8089ba354a6c47afae8eac99a65e32e7") 

if button_clicked == "SEARCH":
    main()


def main():
    #OHLC CHECKBOX
    OHLCtab = st.sidebar.checkbox("OHLC Table")
    if OHLCtab:
        st.subheader("""**OHLC Data** for """ + selected_crypto)
        crypto_df_new = cm.create_ts(selected_crypto, td)
        #crypto_df_close = crypto_df_new.drop(columns=['open','high', 'low'])
        #pct_change_raw = crypto_df_close.pct_change()
        st.write(crypto_df_new)
    
    #SHARPE CHECKBOX
    sharpeCrypto = st.sidebar.checkbox("Percentage Change/Sharpe Ratio")
    if sharpeCrypto:
        st.header(f'{selected_crypto} Data')
        st.write(cm.create_ts(selected_crypto, td)) 
        # Define Data Frame
        crypto_df_new = cm.create_ts(selected_crypto, td)
        crypto_df_close = crypto_df_new.drop(columns= ['open','high','low'])
        pct_change_raw = crypto_df_close.pct_change()

        # Rename and assign pct_change_raw columns to pct_change 
        pct_change= pct_change_raw.rename(columns= {'close':'daily_return'}).dropna().copy()

        # Creating two Columns for comparison
        col1Pct, col2Sharpe = st.columns([2, 1])
            

        # Defining the two columns
        #Column 1 for Pct Change
        with col1Pct:
            # Pct Change Data
            st.subheader('Percentage Change')
            st.write(pct_change)

            #Column 2 for Sharpe Ratios
        with col2Sharpe:
            # Sharpe Ratio Data
            st.subheader('Sharpe Ratio')
                
            # Calculate annualized Standard Deviation
            std_annual = (pct_change.std()*np.sqrt(252))
            
            # Calculate annualized Mean Return
            mean_returns_annual = (pct_change.mean()*252)
            
            # Calculate annualized Sharpe Ratio
            sharpe_ratio = (mean_returns_annual/std_annual)
            st.write(sharpe_ratio)
            #Pct Change Graph
            st.subheader('Percentage Change Chart')
            #Line Chart for Percentage Change
            st.line_chart(pct_change, width=5000, height=200, use_container_width=True)
    
    
    #CMULATIVE RETURNS CHECBOX
    cumulReturns = st.sidebar.checkbox("Cumulative Returns")
    if cumulReturns:
        crypto_df_new = cm.create_ts(selected_crypto, td)
        crypto_df_close = crypto_df_new.drop(columns= ['open','high','low'])
        pct_change_raw = crypto_df_close.pct_change()
            
        # Rename and assign pct_change_raw columns to pct_change 
        pct_change= pct_change_raw.rename(columns= {'close':'daily_return'}).dropna().copy()

        # Create cumulative returns subheader 
        st.subheader ('Cumulative Returns')

        # Calculate cumulative returns subheader 
        cumulative_returns = (1+pct_change).cumprod()
        st.write(cumulative_returns )
        st.line_chart(cumulative_returns, width=5000, height=200, use_container_width=True)
    
    #2YR SHARPE 
    twoYrPrAndSharpe= st.sidebar.checkbox("Two Year Percentage Change/Sharpe Ratio")
    if twoYrPrAndSharpe:
        st.header("Two Year Sharpe Ratios and % Change for")
        #Sample Cryptocurrencies
        st.subheader('Sample Set of Cryptos(Last 2 Years)')

            #BTC, ETH, XRP, BNB, SOL, ADA and LUNA dataframe
        btc_df = (cm.btc_df)
        eth_df = (cm.eth_df)
        xrp_df = (cm.xrp_df)
        bnb_df = (cm.bnb_df)
        sol_df = (cm.sol_df)
        ada_df = (cm.ada_df)
        luna_df = (cm.luna_df)
            
        #Editing dataframe
        BTC1 = btc_df.drop(columns=['open', 'high', 'low'], axis=1)
        ETH1 = eth_df.drop(columns=['open', 'high', 'low'], axis=1)
        XRP = xrp_df.drop(columns=['open', 'high', 'low'], axis=1)
        BNB = bnb_df.drop(columns=['open', 'high', 'low'], axis=1)
        SOL = sol_df.drop(columns=['open', 'high', 'low'], axis=1)
        ADA = ada_df.drop(columns=['open', 'high', 'low'], axis=1)
        LUNA = luna_df.drop(columns=['open', 'high', 'low'], axis=1)           

        #Concatenate DFs, getting pct change, getting sharpe ratio, and posting the images of graphs
        custom_df= pd.concat([BTC1,ETH1,XRP,BNB,SOL,ADA,LUNA],axis=1, keys=['BTC/USD', 'ETH/USD', 'XRP/USD', 'BNB/USD', 'SOL/USD', 'ADA/USD', 'LUNA/USD'])
        custom_pct_change= custom_df.pct_change().dropna().copy()
        # pic_pct = Image.open('pct.jpeg')
        st.subheader('Percentage Change')
        st.write(custom_pct_change)
        # st.image(pic_pct)
            
        custom_sharpe_ratios = ((custom_pct_change.mean()) * 252) / (custom_pct_change.std() * np.sqrt(252))
        custom_sharpe_ratios = pd.DataFrame(custom_sharpe_ratios)
        st.subheader('Sharpe Ratios')
        st.write(custom_sharpe_ratios)
    
    mcTenYear = st.sidebar.checkbox("Ten Year Monte Carlo Simulation")
        # Monte Carlo Simulation
        # Create BTC and ETH subheader for a Cryptocurrency Portfolio
    if mcTenYear:
        st.header('MonteCarlo Simulations'+ selected_crypto)
        st.subheader('Sample Cryptocurrency Prices')
        # BTC and ETH DataFrame
        btc_df = (cm.btc_df)
        eth_df = (cm.eth_df)

        # Edit BTC and ETH DataFrame
        BTC =btc_df.drop(columns=['open', 'high', 'low'], axis=1)
        ETH= eth_df.drop(columns=['open', 'high', 'low'], axis=1)

        # Concatenate DFs
        portfolio_df= pd.concat([BTC,ETH],axis=1, keys=['BTC/USD', 'ETH/USD'])
        st.write(portfolio_df)

        # Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
        MC_tenyear = MCSimulation(
            portfolio_data = portfolio_df,
            weights = [.70,.30],
            num_simulation = 100,
            num_trading_days = 252*10
                    )

            # Running a Monte Carlo simulation to forecast 10 years cumulative returns
        st.subheader('Monte Carlo Simulation: 10yr')
        MC_tenyear_calc = MC_tenyear.calc_cumulative_return()
        st.write(MC_tenyear_calc)
        # Fetch summary statistics from the 10yr Monte Carlo simulation results
        st.subheader('Monte Carlo Simulation: 10yr Summary Statistics')
        summary_statistics_ten = MC_tenyear.summarize_cumulative_return()

        # Print summary statistics
        st.write(summary_statistics_ten)

        # Set initial investment
        initial_investment = 20000  #it is always 20k in our projects including dry-run wallets

        # Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
        ci_lower = round(summary_statistics_ten[8]*initial_investment,2)
        ci_upper = round(summary_statistics_ten[9]*initial_investment,2)

        # Print results
        st.text(f"There is a 95% chance that an initial investment of ${initial_investment}"
                "in the portfolio over the next 10 years will end in the range:"
                f" ${ci_lower: 0.2f} and ${ci_upper: 0.2f}")


        

if __name__ == "__main__":
    main()