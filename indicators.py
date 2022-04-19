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
