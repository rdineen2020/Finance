import time
import datetime
from numpy import nan
import pandas as pd
from pandas_datareader import data as web, test
import matplotlib.pyplot as plt

## Importing Data
ticker = 'BTC-USD'
period1 = int(time.mktime(datetime.datetime(2021, 11, 25, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2021, 12, 25, 23, 59).timetuple()))
interval = '1d'

start = time.perf_counter()

query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
df = pd.read_csv(query_string)

## 
'''
I want to buy when short term moving average is above long term
I want to short when short term moving average is below long term

To do this i need to define the function moving average
I need to then set up the conditions
'''

def moving_averages(input, window):
    return input.rolling(window).mean().tolist()

def test_method(func, input, window1, window2, plot_equity = False, trade_fee = 0, short_fee = 0 , plot_trades = False, color_long = "green", color_short = "red", colour_neutral = "gray", color_term1 = "darkorange", color_term2 = "darkblue", color_equity = "purple"):
    output1 = func(input['Close'], window1)
    output2 = func(input['Close'], window2)

    equity = [input['Close'][window2 -1]]
    prediction = []

    last = "neutral"
    

    if plot_equity or plot_trades:
        plt.plot(input['Date'], input['Close'], label = "Value")

    for i in enumerate(output1):
        if last == "long":
            equity.append((equity[-1] + input['Close'][i[0]] - input['Close'][i[0]-1]) * (1 - trade_fee))
        elif last == "short":
            equity.append((equity[-1] - input['Close'][i[0]] + input['Close'][i[0]-1]) * (1 - short_fee - trade_fee))
        elif last == "neutral":
            equity.append(equity[-1])
        

        if output1[i[0]] > output2[i[0]]:
            #long
            
            prediction.append(output1[i[0]] - output2[i[0]])
            
            if plot_trades and last != "long":
                plt.axvline(x=input['Date'][i[0]], color = color_long)
                
            last = "long"


        elif output1[i[0]] < output2[i[0]]:
            #short
            
            prediction.append(output2[i[0]] - output1[i[0]])

            if plot_trades and last != "short":
                plt.axvline(x=input['Date'][i[0]], color = color_short)
                
                
            last = "short"

        elif last == "neutral":
            #no data
            
            prediction.append(nan)
            if plot_trades:
                plt.axvline(x=input['Date'][i[0]], color = colour_neutral)

    equity.pop(0)  
    if plot_trades or plot_equity:
        
        if plot_trades:
            plt.plot(input['Date'], output1, color = color_term1, label = "Output1")
            plt.plot(input['Date'], output2, color = color_term2, label = "Output2")

        if plot_equity:
            plt.plot(input['Date'], equity, color_equity, label = "Equity")

        plt.xticks(rotation=270)
        plt.legend()
        plt.show()

test_method(moving_averages, df, 3, 5, trade_fee=0.002, short_fee= 0.002, plot_equity=True, plot_trades=True)


        