import plotly.graph_objects as go

class Indicators:

  def __init__(self, ohlc_df):
    self._indicators_df = ohlc_df
    self._ohlcv_list = ['Open','High','Low','Close','Volume']
    
    #Create and plot the graph

    fig = go.Figure(data=[go.Candlestick(x=self._indicators_df.index,
                                          open=self._indicators_df["Open"],
                                          high=self._indicators_df["High"],
                                          low=self._indicators_df["Low"],
                                          close=self._indicators_df["Close"])
    ])
    
    fig.update_layout(
        title = "Candlestick", 
        xaxis_title = "Date", 
        yaxis_title = "Price")
    fig.show()    

  ### Getters / Setters
  def get_indicators_df(self):
    return self._indicators_df

  def get_indicators_df(self, ohlc_df):
    self._indicators_df = ohlc_df
    return self._indicators_df
   
  ### Aroon
  # https://www.investopedia.com/terms/a/aroon.asp
  # Main: trend indicator
  # Type: two line cross
  # 
  # Aroon Up is above the Aroon Down - bullish behavior (Up Trend)
  # Aroon Down is above the Aroon Up - bearing behavior (Down Trend)
  # Crossovers of the two lines can signal trend changes
  #
  def aroon(self, period=14, plot=False):
    self._period = period
    up_header = "Aroon Up"
    down_header = "Aroon Down"
    header = "Output Aroon"

    self._indicators_df[up_header] = 100 * self._indicators_df.High.rolling(period + 1).apply(lambda x: x.argmax()) / period
    self._indicators_df[down_header] = 100 * self._indicators_df.Low.rolling(period + 1).apply(lambda x: x.argmin()) / period

    # Indicator Output
    self._indicators_df.loc[self._indicators_df[up_header] > self._indicators_df[down_header], header] = True   # Up > Down
    self._indicators_df.loc[self._indicators_df[up_header] <= self._indicators_df[down_header], header] = False 

    if (plot is True):
      #Create and plot the graph
      plt.figure(figsize=(12.2,4.5))
      plt.plot(self._indicators_df[up_header], color="lightblue",  label=up_header) 
      plt.plot(self._indicators_df[down_header], color="tomato"  ,label=down_header) 

      plt.title("Aroon Up and Down")
      plt.legend(loc='upper left')
      plt.show()

    self._indicators_df.drop([up_header, down_header], axis=1, inplace=True)
    return self._indicators_df
  
  ### Exponential Moving Average
  def EMA(self, period=9):

    header = "Output EMA"
    self._indicators_df["EMA"] = self._indicators_df.loc[:,"Close"].ewm(span=period,adjust=False).mean()
    self._indicators_df[header] = self._indicators_df["Close"] > self._indicators_df["EMA"]

    return self._indicators_df

  ### Simple Moving Average
  def SMA(self, period=9):

    header = "Output SMA"
    self._indicators_df["SMA"] = self._indicators_df.loc[:,"Close"].rolling(window=period).mean()
    self._indicators_df[header] = self._indicators_df["Close"] > self._indicators_df["SMA"]

    return self._indicators_df
