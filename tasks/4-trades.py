import pandas as pd
from datetime import datetime

# to do:
# create open, high, low & close prices (OHLC)
# Create total volume for each product and contract over a time interval.


trades = pd.read_csv("./Data analyst coding challenge/Trades.csv")
trades.info()
# ensure date time is formated correctly:
trades["TradeDateTime"]= pd.to_datetime(trades["TradeDateTime"], infer_datetime_format=True)

# trades.loc[trades["TradeDateTime"].astype("str").str.contains("09:00:00")]


# for index, row in trades.iterrows():
#     date = row["TradeDateTime"]:

# split date and time
trades["Date"] = [x.strftime("%Y-%m-%d") for x in trades["TradeDateTime"]]
trades["Time"] = [x.strftime("%H:%M:%S") for x in trades["TradeDateTime"]]

# establish open close: # 7:00 17:00 Assumption: the market closes at 5pm on the dot so take the minute before closing as close price
def open_close(t, open_time="07:00:00", close_time="16:59:00"):

    if str(t) == open_time:
        return True
    elif str(t) == close_time:
        return False
    else:
        return "-"

trades["is_open"]= [open_close(i) for i in trades["Time"]]
trades = trades.set_index("TradeDateTime")
# combine same products from different venues


def oc_creator(i):
    for
    return

def trade_pipeline(table):




    return