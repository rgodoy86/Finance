class Indicators:

    def __init__(self):
        pass

    ## Simple Media Average
    def SMA(self, df, period=9):
        df["SMA_" + str(period)] = df.loc[:,"Close"].rolling(window=period).mean()
        return df

    # Exponential Media Average
    def EMA(self, df, period=9):
        df["EMA_" + str(period)] = df.loc[:,"Close"].ewm(span=period, adjust=False).mean()
        return df