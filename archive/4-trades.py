import pandas as pd
from datetime import datetime

# to do:
# create open, high, low & close prices (OHLC)
# Create total volume for each product and contract over a time interval.


trades = pd.read_csv("./Data analyst coding challenge/Trades.csv")
trades.info()
# ensure date time is formated correctly:
trades["TradeDateTime"]= pd.to_datetime(trades["TradeDateTime"], infer_datetime_format=True)
# combine VenueB & VenueA
trades = trades.replace({"Emission - Venue B": "Emission", "Emission - Venue A": "Emission"})
# trades.loc[trades["TradeDateTime"].astype("str").str.contains("09:00:00")]


# for index, row in trades.iterrows():
#     date = row["TradeDateTime"]:

# Preprocessing: 
## split date and time
trades["Date"] = [x.strftime("%Y-%m-%d") for x in trades["TradeDateTime"]]
trades["Time"] = [x.strftime("%H:%M:%S") for x in trades["TradeDateTime"]]
trades = trades.set_index("TradeDateTime").between_time("7:00", "17:00") # for OHLC data this range is all we care about
trades_agg = trades.groupby(["Product", "TradeDateTime", "Time", "Contract"]).mean().reset_index()
# add hour and minute preprocessing cols for future function
trades_agg["Hour"] = [int(x.strftime("%H")) for x in trades_agg["TradeDateTime"]]
trades_agg["Minute"] = [int(x.strftime("%M")) for x in trades_agg["TradeDateTime"]]
# sorting the index by time so that when product is filtered out I can have a distinct is_open column to allow me to calculate HL
trades_agg = trades_agg.set_index("TradeDateTime").sort_index().reset_index()
# preprocessing is good (is open for each category will look like this: Open, -, - ,- ,-, ..., Close) and the Max and min between these numbers will be the HL
# establish open close: # 7:00 17:00 Assumption: the market closes at 5pm on the dot so take the minute before closing as close price

check_open = (7,0)
mappings_dict = {}
working_days = 4
unique_products = len(trades_agg["Product"].unique().tolist())
counter = 0
holder = []
for i, (H,M) in enumerate(zip(trades_agg["Hour"], trades_agg["Minute"])):
    counter = check_open[-1]
    if len(holder) < unique_products:
        if (H,M) == check_open:
            holder.append(i)
            counter +=1
    elif len(holder) < unique_products:
        pass
