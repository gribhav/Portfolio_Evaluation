import os
import pandas as pd
import numpy as np

file_path = os.path.join(os.path.dirname(__file__), 'Nordea_stabil_avkastning.csv')


df = pd.read_csv(file_path, sep=',', encoding='utf-8')

def set_datetime(dataframe):
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])

set_datetime(df)
df.info()
print(df)

new_df = df.dropna()
new_df.reset_index(0)
print(new_df)
new_df.info()

TRADING_DAYS = 2
returns = np.log(new_df['Adj Close']/df['Adj Close'].shift(1))
returns.fillna(0, inplace=True)
new_df['Daily Volatility'] = returns.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
new_df['Daily Volatility'].fillna(0,inplace = True)
print(new_df.tail())

TRADING_DAYS = 252
returns = np.log(new_df['Adj Close']/df['Adj Close'].shift(1))
returns.fillna(0, inplace=True)
new_df['Annual Volatility'] = returns.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
new_df['Annual Volatility'].fillna(0,inplace = True)
print(new_df.tail())

new_df['Daily Returns'] = new_df['Adj Close'].pct_change()
average_annual_volatility = new_df['Annual Volatility'].mean()
average_daily_volatility = new_df['Daily Volatility'].mean()

new_df['Normed Return'] = new_df['Adj Close']/new_df.iloc[0]['Adj Close']

average_return = new_df['Daily Returns'].mean()*252
sharpe_ratio = (average_return)/(average_daily_volatility)

plt.figure(figsize = (10,6))
plt.scatter(new_df['Date'],new_df['Daily Returns'], marker = '.', alpha = 0.5)
plt.xlabel('Date')
plt.ylabel('Daily Returns')
