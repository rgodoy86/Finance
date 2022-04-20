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

  ### Average True Range - ATR
  # https://www.investopedia.com/terms/a/atr.asp
  #
  def ATR(self, period=14):

    atr_title = "ATR"

    high_low = self._indicators_df['High'] - self._indicators_df['Low']
    high_cp = np.abs(self._indicators_df['High'] - self._indicators_df['Close'].shift())
    low_cp = np.abs(self._indicators_df['Low'] - self._indicators_df['Close'].shift())
    
    df = pd.concat([high_low, high_cp, low_cp], axis=1)
    true_range = np.max(df, axis=1)

    self._indicators_df[atr_title] = true_range.rolling(period).mean()

    #Create and plot the graph
    plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
    plt.plot(self._indicators_df[atr_title],  label="ATR") # plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)

    plt.title("Average True Range")
    plt.legend()
    plt.show()

    return self._indicators_df
  
  ### Chaiking Money Flow (CMF)
  # https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/chaikin-money-flow-cmf/
  # Main: trend indicator
  # Type: zero cross
  # 
  # Above zero - bullish behavior (Up Trend)
  # Below zero - bearing behavior (Down Trend)
  #

  def chaiking_money_flow(self, period=20, plot=False, threshold=0):
    full_title = "Chaiking Money Flow"
    title = "CMF"
    header = "Output CMF"

    self._indicators_df["cmfm"] = (((self._indicators_df["Close"] - self._indicators_df["Low"]) - (self._indicators_df["High"] - self._indicators_df["Close"])) / 
                                   (self._indicators_df["High"] - self._indicators_df["Low"]))
    
    self._indicators_df["cmfv"] = self._indicators_df["cmfm"] * self._indicators_df["Volume"]

    self._indicators_df[title] = self._indicators_df['cmfv'].rolling(window=period).mean() / self._indicators_df['Volume'].rolling(window=period).mean() 
    self._indicators_df.drop(["cmfm","cmfv"], inplace=True, axis=1)

    # Indicator Output
    self._indicators_df.loc[self._indicators_df[title] > 0, header] = True # Buy
    self._indicators_df.loc[self._indicators_df[title] <= 0, header] = False # Sell

    #Create and plot the graph
    if (plot is True):
      plt.figure(figsize=(12.2,4.5))
      plt.plot( self._indicators_df[title], color="lightgreen", label=title)
      plt.axhline(y=threshold, color='tomato', linestyle='--')

      plt.title(full_title)
      plt.legend(loc='upper left')
      plt.show()

    return self._indicators_df
  
  ### Exponential Moving Average
  # https://www.investopedia.com/terms/m/movingaverage.asp
  #
  def EMA(self, period=9):

    header = "Output EMA"
    self._indicators_df["EMA"] = self._indicators_df.loc[:,"Close"].ewm(span=period,adjust=False).mean()
    self._indicators_df[header] = self._indicators_df["Close"] > self._indicators_df["EMA"]

    return self._indicators_df

    ### Heikin Ashi 
  # https://www.investopedia.com/trading/heikin-ashi-better-candlestick/#:~:text=Heikin%2DAshi%2C%20also%20sometimes%20spelled,and%20trends%20easier%20to%20analyze.
  # https://tradewithpython.com/constructing-heikin-ashi-candlesticks-using-python
  #
  #
  def heikin_ashi(self, plot=False):
    header = "Output HA"
    title = "Heiking Ashi"

    self._indicators_df["HA Close"] = self._indicators_df["Open"] + self._indicators_df["High"] + self._indicators_df["Low"] + self._indicators_df["Close"]
    self._indicators_df["HA Close"] = round(self._indicators_df["HA Close"] / 4, 2)

    self._indicators_df["HA Open"] = np.nan
    col_idx = self._indicators_df.columns.get_loc("HA Open")

    for i in range(len(self._indicators_df)):
      if i == 0:
        self._indicators_df.iat[0,col_idx] = round(((self._indicators_df["Open"].iloc[0] + self._indicators_df["Close"].iloc[0])/2),2)
      else:
        self._indicators_df.iat[i,col_idx] = round(((self._indicators_df["HA Open"].iloc[i-1] + self._indicators_df["HA Close"].iloc[i-1])/2),2)

    self._indicators_df["HA High"] = round(self._indicators_df[["HA Close","HA Open", "High"]].max(axis=1),2)
    self._indicators_df["HA Low"] = round(self._indicators_df[["HA Close","HA Open", "Low"]].min(axis=1),2)

    # Indicator Output
    self._indicators_df["tmp"] = self._indicators_df["HA Close"] > self._indicators_df["HA Open"]
    self._indicators_df["tmp2"] = self._indicators_df["tmp"].shift(1)

    self._indicators_df[header] = (self._indicators_df["tmp"] ^ self._indicators_df["tmp2"])
    self._indicators_df[header] = self._indicators_df[header]  &  (self._indicators_df["tmp"] == False) # True => Exit Signal

    self._indicators_df.drop(["tmp", "tmp2"], axis=1, inplace=True)

    if (plot is True):
      fig = go.Figure(data=[go.Candlestick(x=self._indicators_df.index,
                                            open=self._indicators_df["HA Open"],
                                            high=self._indicators_df["HA High"],
                                            low=self._indicators_df["HA Low"],
                                            close=self._indicators_df["HA Close"])
                            ])
     
      fig.update_layout( 
                title = title + ' Chart', 
                xaxis_title = 'Date', 
                yaxis_title = 'Price')
      fig.show()

    return self._indicators_df

   ### Money Flow Index
  def money_flow_index(self, period=14):
    mfi_title = "MFI"

    #Calculate the typical price
    typical_price = (self._indicators_df['Close'] + self._indicators_df['High'] + self._indicators_df['Low']) / 3
    
    #Calculate the money flow
    money_flow = typical_price * self._indicators_df['Volume']

    #Get all of the positive and negative money flows 
    #where the current typical price is higher than the previous day's typical price, we will append that days money flow to a positive list
    #and where the current typical price is lower than the previous day's typical price, we will append that days money flow to a negative list
    #and set any other value to 0 to be used when summing

    positive_flow =[] #Create a empty list called positive flow
    negative_flow = [] #Create a empty list called negative flow
    #Loop through the typical price 
    for i in range(1, len(typical_price)):
      if typical_price[i] > typical_price[i-1]: #if the present typical price is greater than yesterdays typical price
        positive_flow.append(money_flow[i-1])# Then append money flow at position i-1 to the positive flow list
        negative_flow.append(0) #Append 0 to the negative flow list
      
      elif typical_price[i] < typical_price[i-1]:#if the present typical price is less than yesterdays typical price
        negative_flow.append(money_flow[i-1])# Then append money flow at position i-1 to negative flow list
        positive_flow.append(0)#Append 0 to the positive flow list
      
      else: #Append 0 if the present typical price is equal to yesterdays typical price
        positive_flow.append(0)
        negative_flow.append(0)
    
    #Get all of the positive and negative money flows within the time period
    positive_mf =[]
    negative_mf = [] 

    #Get all of the positive money flows within the time period
    for i in range(period-1, len(positive_flow)):
      positive_mf.append(sum(positive_flow[i+1-period : i+1]))
    
    #Get all of the negative money flows within the time period  
    for i in range(period-1, len(negative_flow)):
      negative_mf.append(sum(negative_flow[i+1-period : i+1]))

    # Calculate MFI
    mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf)  + np.array(negative_mf) ))
    
    # Filling up the 14 blank values to match main dataframe length
    tmp_array = np.empty((1,period,))
    tmp_array[:] = np.nan

    # Adding it into the main dataframe
    self._indicators_df[mfi_title] = np.concatenate((tmp_array[0], mfi))

    #Create and plot the graph
    plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
    plt.plot( self._indicators_df[mfi_title],  label='Money Flow Index') # plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
    plt.axhline(10, linestyle='--', color = 'orange')                               # Over Sold line (Buy)
    plt.axhline(20, linestyle='--',color = 'blue')                                  # Over Sold Line (Buy)
    plt.axhline(80, linestyle='--', color = 'blue')                                 # Over Bought line (Sell)
    plt.axhline(90, linestyle='--', color = 'orange')                               # Over Bought line (Sell)

    plt.title('Money Flow Index')
    plt.legend(["MFI", "10 - Oversold line (Buy)", "20 - Oversold line (Buy)", "80 - Overbought line (Sell)", "90 - Overbought line (Sell)"], loc='upper left')
    plt.show()

    return self._indicators_df

  
  ### On Balance Volume
  # https://www.investopedia.com/terms/r/relative_vigor_index.asp
  # https://medium.com/codex/implementing-the-relative-vigor-index-and-backtesting-a-trading-strategy-with-python-d317afc0923a
  # https://www.investopedia.com/terms/o/onbalancevolume.asp
  #
  # Main: trend indicator
  # Type: oscillator
  # 
  # Above zero - bullish behavior (Up Trend)
  # Below zero - bearing behavior (Down Trend)
  #
  def OBV(self, plot=False):
    header = "Output OBV"

    self._indicators_df.loc[self._indicators_df["Close"] > self._indicators_df["Close"].shift(1), "Vol"] = self._indicators_df["Volume"]
    self._indicators_df.loc[self._indicators_df["Close"] < self._indicators_df["Close"].shift(1), "Vol"] = self._indicators_df["Volume"] * (-1)
    self._indicators_df.loc[self._indicators_df["Close"] == self._indicators_df["Close"].shift(1), "Vol"] = 0

    self._indicators_df[header] = self._indicators_df["Vol"].cumsum()
    self._indicators_df.drop(["Vol"], axis=1, inplace=True)

    #Create and plot the graph
    if (plot is True):
      plt.figure(figsize=(12.2,4.5))
      plt.plot( self._indicators_df[header], color="lightblue", label="OBV")

      plt.title(header)
      plt.legend(loc='upper left')
      plt.show()

    return self._indicators_df

  
  ### Simple Moving Average
  # https://www.investopedia.com/terms/m/movingaverage.asp
  #
  def SMA(self, period=9):

    header = "Output SMA"
    self._indicators_df["SMA"] = self._indicators_df.loc[:,"Close"].rolling(window=period).mean()
    self._indicators_df[header] = self._indicators_df["Close"] > self._indicators_df["SMA"]

    return self._indicators_df
