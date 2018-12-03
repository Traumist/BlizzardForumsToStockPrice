# -*- coding: utf-8 -*
"""
Created on Fri Nov 23 07:59:24 2018
Program to take in forum post sentiments
and plot them on a scatter plot ranging from 1(positive) to -1 (negative)
@author: Brandon Reyes
"""
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import pandas_datareader as web

start = dt.datetime(2018,1,1)
end = dt.datetime(2019,1,1)

#Get Stock data and create percent change column
df1 = web.DataReader('ATVI', 'yahoo', start, end)
pctChange = []
for index, row in df1.iterrows():
    if row['Open'] > row['Close']:
        pct = ( row['Open']/row['Adj Close'] ) - 1
        pct = round(pct, 2)
        pctChange.append(pct)
    else:
        pct = ( row['Open']/row['Adj Close'] ) - 1
        pct = round(pct, 2)
        pctChange.append(pct)

df1['pct change'] = pctChange        
df1 = df1[['pct change', 'Adj Close']]
df1 = df1.reset_index(level=['Date'])



#read post data in and clean up data
#Expected column names: [threadTitle, datePosted, polarity, section])
finalData = pd.read_csv('75subjectivity.csv')
df = finalData.drop_duplicates(subset=['threadTitle'], keep='last')
df = df.dropna()
df = df.reset_index()

df = df[['datePosted','polarity','threadTitle','section']]
with open('droppedDupes.csv', 'w', encoding='utf-8') as f:
    df.to_csv(f, sep=',', header=True, encoding='utf-8')


#Resample to 1 Day per dot on graph
df = df.set_index(pd.DatetimeIndex(df['datePosted']))
df = df.between_time('00:00','23:59').resample('1D').mean()
df = df.reset_index()
df = df.dropna()
df = df[(df['datePosted'].dt.year >= 2018)]

#get mean of polarity to draw horizontal line on it
mean = df['polarity'].mean()

#write file with 1 Day resampled averages
with open('1D Averages.csv', 'w', encoding='utf-8') as f:
    df.to_csv(f, sep=',', header=True, encoding='utf-8')

dates = df['datePosted']
dates = [pd.to_datetime(d) for d in dates]

#merging two dataframes to get a correlation value
df.rename(columns={'datePosted':'Date'}, inplace=True)
df2 = pd.merge(df1, df, on=['Date'], how='left')
df2 = df2.dropna()
df_corr = df2['polarity'].corr(df2['pct change'])
print('Correlation between polarity and percent stock price change:', df_corr)

stockDates = df2['Date']
stockDates = [pd.to_datetime(dd) for dd in stockDates]

#Graphing sentiment on scatter plot
plt.scatter(dates, df['polarity'],
             c=df['polarity'], cmap='RdYlGn',vmin=-1.,vmax=1.)
plt.xticks(rotation=45)
plt.ylabel('Sentiment Polarity(-1 to 1)')
plt.xlabel('Date')
plt.margins(top=0.93,
bottom=0.215,
left=0.09,
right=0.91,
hspace=0.2,
wspace=0.2)

#Horizontal mean line
#plt.axhline(y=0,c='r',linestyle='-')



#Plot percent change over scatter plot
ax2 = plt.twinx()
ax2.set_ylabel('price', color='b')
ax2.plot(stockDates, df2['Adj Close'], color='b')


plt.show()
