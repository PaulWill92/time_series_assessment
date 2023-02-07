import pandas as pd
from datetime import datetime
import time
import datapane as dp
import altair as alt
# data source = consumption.csv

# Load data
consumption = pd.read_csv("./Data analyst coding challenge/Consumption.csv")
time.sleep(1)
print(consumption)
# this throws an error because date formats in the rows are different
print("Attempting to convert date column into datetype object")
try:
    consumption["Date"]= pd.to_datetime(consumption["Date"], infer_datetime_format=True)
except:
    print("WARNING: there are some different date formats in the rows, so can't infer date format")
 # inspect for missing values:
print("--- examining missing values:---")
time.sleep(.5)
print(f"There are: \n {consumption.isna().sum()} \n values missing values across the consumption dataframe rows")
 # No values are missing across dataframe rows

# check for dupes:
# across duplicates
time.sleep(.5)
consumption.duplicated().sum() # there are zero across duplicates
# date duplicates:
consumption["Date"].duplicated().sum() 


# check why the duplicates occur with consumption value
consumption.loc[consumption["Date"].duplicated()]
consumption.loc[consumption["Date"]=="2020125"] # The values within the day 1 to 29 are quite low in differences how to handle the duplicates


# consumption dupes:
consumption["Consumption"].duplicated().sum() # 177 days are the same consumption 
consumption.loc[consumption["Consumption"].duplicated()] # check the duplicate values
consumption.loc[consumption["Consumption"].astype("str").str.contains("245.43")] # validate why they are


# findings:
# 2 types of date formats: dd/mm/yyyy and yyyymmdd
# Dates with the dd/mm/yyyy format tend to usually be part of the 177 consumption duplicates
# Dates with the yyyymmdd are all part of the 18 date duplicates and don't vary too greatly with 50-100 units of consumption variance


# Handling the format inconsistencies:
# seperate date into list
dates = consumption["Date"].tolist()

def date_conversion(date_input, conversion_pattern=None):
    """
    A function that converts a string with so far only 2 defined formats into a datetime object.

    Args:
        date_input (str): a date string

    Returns:
        date_time_object : date object of converted string given the 2 types of formats.

    """
    if conversion_pattern == None:
        format1 = "%d/%m/%Y" # equivalent to dd/mm/yyyy
        format2 = "%Y%m%d" # equivalent to yyyymmdd

        try:
            date_obj = datetime.strptime(date_input, format1)
        except:
            date_obj = datetime.strptime(date_input, format2)

        
    else:
        date_obj = datetime.strptime(date_input, conversion_pattern)

    return date_obj


# test function: 
converted_dates = [date_conversion(d) for d in dates]

years = [d.year for d in converted_dates]

unique_years = list(set(years))
len(unique_years) # the function worked and there are 7 unique years that can be assigned a value
# add conversion to dataframe:

consumption["Date"] = [date_conversion(i) for i in consumption["Date"]]
consumption["Year"] = [i.strftime("%Y") for i in consumption["Date"]]
consumption["Month"] = [i.strftime("%m") for i in consumption["Date"]]
consumption["index"] = [i.strftime("%m-%d") for i in consumption["Date"]]
consumption.set_index("index", inplace=True)

cleaned_consumption_df = consumption.drop("Date", axis=1)[["Year", "Consumption", "Month"]]
# Dealing with duplicates:
len(cleaned_consumption_df)
len(cleaned_consumption_df.loc[cleaned_consumption_df.duplicated()])
cleaned_consumption_df.loc[cleaned_consumption_df.duplicated()]


# mapping month to season based on UK:
def season_mapping(month):
    season_dict = { "Winter": ["12","01","02"],
                    "Spring": ["03", "04", "05"],
                    "Summer": ["06", "07", "08"],
                    "Autumn": ["09", "10", "11"]

    }
    for k,v in season_dict.items():
        if month in v:
            return k
# applying map to dataframe
cleaned_consumption_df["Season"]= [season_mapping(month) for month in cleaned_consumption_df["Month"]]

# aggregate by year and season
season = cleaned_consumption_df.groupby(["Year","Season"]).agg(Consumption=("Consumption", "mean")).reset_index()
season_filtered = season.loc[season["Year"].astype("int") <= 2020].copy()
average_2021_2022 = season.loc[season["Year"].astype("int") > 2020].copy().groupby("Year").mean().reset_index().replace({"2021": "2021 Average", "2022":"2022 Average"})

line = alt.Chart(season_filtered).mark_line(point=True).encode(
    alt.X("Year:T"),
    alt.Y("Consumption:Q"),
    alt.Color("Season"),
    alt.OpacityValue(0.7),
    tooltip= [alt.Tooltip("Season"),
              alt.Tooltip("Year:T"),
              alt.Tooltip("Consumption")
             ]
).interactive().properties()

avg_line = alt.Chart(average_2021_2022).mark_rule(color="black", strokeDash=[2,2]).encode(
    alt.Y("Consumption:Q"),
    alt.SizeValue(2),
    alt.Color("Year"),


)

line + avg_line

graph = line+avg_line



# Energy consumption seems to go up based on how cold the season is. The Years 2017 and 2018 most likely had the coldest winters as their consumption units peaked.

# simple app:
app = dp.App( dp.Text("## Energy Consumption Analysis Across 5 Years"),
              dp.Plot(graph, caption="Units of Energy Consumption Per Year"),
              dp.DataTable(cleaned_consumption_df, caption="Consumption Dataset"),
              dp.Text("### Analysis: \nEnergy consumption seems to go up based on how cold the season is that means winter and autumn, are generally the colder of the seasons, thus more energy is consumed than the other seasons. The Years 2017 and 2018 most likely had the coldest winters as their consumption units peaked."))
app.save(path="./consumption.html", open=True)

