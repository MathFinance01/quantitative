import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns


st.title('Calculation of PnL Attributions')
st.header('What is PnL attributions?')
st.write('Generally, from a trading desk, pnl reports are sent out at the end of the day. The report should include \
         all the relevant details that is going to explain the PnL generated for that day. It is important for the managment\
         to know the key areas that are costing the firm maybe a little too much money. So, the management might ask the traders\
         to prepare the something called \'PnL explain\' or \'PnL attribution report\'. PnL attribution is attributing total PnL \
         into multiple types of PnLs such as:')

st.subheader('Trading PnL:')
st.write('PnL generated during the trade execution wrt the mid at the time of trade')
st.subheader('Overnight PnL:')
st.write('PnL generated from the last EOD till today\'s SOD')
st.subheader('MTM PnL:')
st.write('PnL generated on a position due to the market movements')
st.write('There are many other types of PnL attributions that the trader might be interested in.')
st.write('In this article, we will calculate PnL attribution of a portfolio and plot those different attributions.\
         We are going to calculate the attributions overnight, mark to market and trading. The sum of all the attributions\
         will be the total pnl.')

st.write('I will be using Pandas to calculate the PnLs.')
st.write('A portfolio with the following eod positions is being used:')

trades = pd.read_csv('src/products/data/trades.csv')
eod_positions = pd.read_csv('src/products/data/eod_positions.csv')
price_updates = pd.read_csv('src/products/data/price_updates.csv').sort_values(by='time').reset_index(drop=True)
st.dataframe(eod_positions)
st.write('Following are the hypothetical trades that occurred:')
st.dataframe(trades)
st.write('Price updates for each of the symbols is listed below:')
st.dataframe(price_updates)

st.subheader('Loading and cleaning the files:')
st.write('Most time, the files that given will not be in the right format. For example, time format might not be uniform,\
         or the same columns might have different names such as \'sym\' for \'symbol\'. You would want to remove such inconsistencies\
         before doing any calculations.')

loading_code = '''
trades = pd.read_csv('trades.csv')
eod_positions = pd.read_csv('eod_positions.csv')
price_updates = pd.read_csv('price_updates.csv')

trades['time'] = pd.to_datetime(trades['time'])
price_updates['time'] = pd.to_datetime(price_updates['time'])
price_updates.rename(columns = {'sym':'symbol'}, inplace=True)
'''
st.code(loading_code, language='Python')

st.subheader('Transfer of EOD Positions:')
st.write('We have the EOD positions of the last trading day. We would like to transfer it to today\'s starting position.\
         We would then use EOD price and Today\'s SOD price to calculate _Overnight_ _PnL_. The SOD positions are traeated\
         like trades with market mid as the trade price. Also, we need to add a marker\
         to identify SOD trades. For that, we add _trade_type_ column that can take only two values:\'SOD\' and \'ID\'\
         signifying Intra Day trades and Start Of the Day trades')

eodToSod = '''
sod_positions = eod_positions
sod_positions['time'] = pd.to_datetime('09:30') # Marking 9:30 as the SOD
sod_positions['trade_size'] = sod_positions['position']
column_order = ['time', 'symbol','position','eod_price', 'trade_size']
sod_positions = sod_positions[column_order]
sod_positions.loc[:,'trade_type'] = ['SOD']*sod_positions.shape[0]

trades['time'] = pd.to_datetime(trades['time'])
trades.loc[:,'trade_type'] = ['ID']*trades.shape[0]
'''
st.code(eodToSod, language='Python')











