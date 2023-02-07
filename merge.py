import pandas as pd
from datetime import datetime
# load csv and ensure date time column datatype is datetime object
merge = pd.read_csv("./Data analyst coding challenge/Merge.csv")
merge["Datetime"]= pd.to_datetime(merge["Datetime"], infer_datetime_format=True)
# fill nulls with 0's so they can be aggregated
merge = merge.fillna(0, axis=0)
# inspect unique resolution values
set(merge["Resolution"].values)
# change frequency to 2h and merge
two_hour = merge.groupby([pd.Grouper(key="Datetime", freq="2H", origin="07:00:00")]).mean().reset_index().set_index("Datetime")
# limit time range to 7:00 to 17:00 and forward fill the 1D resolution
final = two_hour.between_time("7:00", "17:00").ffill().reset_index()
