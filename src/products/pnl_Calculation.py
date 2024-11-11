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
st.subheader('Mark To Market (MTM) PnL:')
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
price_updates['time'] = pd.to_datetime(price_updates['time'])
price_updates.sort_values(by='time', inplace=True)

'''
st.code(loading_code, language='python')

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
st.code(eodToSod, language='python')

st.subheader('Aggregate Total Position with Cumulative Position and Price')
st.write('Add sod and intra-day trades and get the mid price of the symbol at the time of trades. To get the mid price \
of a sym at a time, we are going to merge by symbols and as of the trade time.')

merge_code = '''
total_positions = pd.concat([sod_positions, trades]).reset_index(drop=True)
trades_with_price = pd.merge_asof(left=total_positions, right=price_updates, on='time', by='symbol', allow_exact_matches=True, direction='backward')
'''
st.code(merge_code, language='python')

st.write('trade price for SOD trades are going to be mid price at SOD')
sod_price = '''
trades_with_price.loc[trades_with_price['trade_type']=='SOD', 'trade_price'] = trades_with_price.loc[trades_with_price['trade_type']=='SOD', 'mid_price']
'''
st.code(sod_price, language='python')

cumulative_pos = '''
trades_with_price['cumulative_position'] = trades_with_price.loc[:,['symbol', 'trade_size']].groupby('symbol').cumsum()
'''
st.code(cumulative_pos, language='python')

st.subheader('Calculate Overnight and Trading PnL')

st.write('For calculating overnight and trading pnl, we need only trade price and mid price at the time of the trade.\
         We can calculate both of them in the following way.')
pnl_calculation_code = '''
#overnight pnl
sod_filt = trades_with_price['trade_type'] == 'SOD'
trades_with_price.loc[sod_filt, 'overnight_pnl'] = trades_with_price.loc[sod_filt, 'position']*(trades_with_price.loc[sod_filt, 'trade_price'] - trades_with_price.loc[sod_filt, 'eod_price'])

#trading pnl
id_filt = trades_with_price['trade_type'] == 'ID'
trades_with_price.loc[id_filt, 'trading_pnl'] = trades_with_price.loc[id_filt, 'trade_size']*(trades_with_price.loc[id_filt, 'mid_price'] - trades_with_price.loc[id_filt, 'trade_price'])

trades_with_price['overnight_pnl'] = trades_with_price['overnight_pnl'].fillna(0)
trades_with_price['trading_pnl'] = trades_with_price['trading_pnl'].fillna(0)

trades_with_price['overnight_pnl'] = trades_with_price.loc[:,['symbol','overnight_pnl']].groupby('symbol').cumsum()
trades_with_price['trading_pnl'] = trades_with_price.loc[:,['symbol','trading_pnl']].groupby('symbol').cumsum()
'''

st.header('Calculating MTM PnL')
st.write('The MTM PnL changes every price update even if there are no more trades. So, unlike overnight and trading PnL,\
 we should try to capture the PnL generated during each price updates. For that, we can _asofmerge_ _trades_with_price_ table\
with _price_updates_ table. Since _price_updates_ table has all the price update, it should be on the left for merging.\
Also, after merging, we will have the intermittent positions during each price update. Then, mtm pnl is just the position\
at each price update multiplied by change in the mid price since last price update.')

mtm_pnl_code = '''
all_pnl = pd.merge_asof(price_updates, trades_with_price.drop(['position', 'eod_price','trade_size', 'trade_type', 'trade_price', 'mid_price'], axis=1), on='time', by='symbol', allow_exact_matches=True, direction='backward')
all_pnl['delta_mid_price'] = all_pnl.loc[:,['symbol','mid_price']].groupby('symbol').diff()
all_pnl['mtm_pnl'] = all_pnl['delta_mid_price'] * all_pnl['cumulative_position']
all_pnl['mtm_pnl'] = all_pnl['mtm_pnl'].fillna(0)
all_pnl['total_pnl'] = all_pnl['overnight_pnl'] + all_pnl['trading_pnl'] + all_pnl['mtm_pnl']
mtm_pnl.loc[:, ['time','overnight_pnl','trading_pnl', 'total_pnl']]
'''

st.code(mtm_pnl_code, language='python')

st.header('Visualizing the book PnL')

book_pnl_code = '''
book_pnl = all_pnl.groupby(['time']).sum()
book_pnl['symbol'] = 'book'
book_pnl.reset_index(inplace=True)
book_pnl = book_pnl.loc[:,['time', 'symbol', 'overnight_pnl', 'trading_pnl', 'mtm_pnl', 'total_pnl']]
'''

st.code(book_pnl_code, language='python')

visualizing_code = '''
book_pnl_plot = book_pnl.drop('symbol', axis=1).melt('time', var_name='pnl_type', value_name = 'pnl')
sns.lineplot(data = book_pnl_plot, x='time', y = 'pnl', hue = 'pnl_type')
'''

st.code(visualizing_code, language='python')












