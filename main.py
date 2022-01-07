import pandas
from datetime import datetime
from pytz import timezone
import numpy as np


def getdate(row):
    """change timezone UTC to Europe/Berlin"""
    return datetime.strptime(row, '%Y-%m-%d %H:%M').astimezone(timezone('UTC')).astimezone(timezone('Europe/Sofia')).date()

def gettime(row):
    return datetime.strptime(row, '%Y-%m-%d %H:%M').astimezone(timezone('UTC')).astimezone(timezone('Europe/Sofia')).time()

def getshift(row):
    return df[row]


def getkwh(row):
    """Wh to kWh"""
    return round(row / 1000, 2)

def convert_datetime_timezone(dt):
    tz1 = timezone("UTC")
    tz2 = timezone("Europe/Sofia")

    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime('%Y-%m-%d %H:%M')

    return dt


#url = 'http://192.168.100.203/emeter/0/em_data.csv'                        # get csv
url = 'em_data (30).csv'
print("Downloading data ...")
df = pandas.read_csv(url)                                                   # read csv
df = df.sort_values(by=['Date/time UTC'])                                   # sort data by fist column
#df['Date/time UTC'] = df['Date/time UTC'].apply(convert_datetime_timezone) #convert to local time
df['date'] = df['Date/time UTC'].apply(getdate)        
grouped_by_date = df.groupby(df['date'])                                    # group by date
#print(grouped_by_date.sum()['Active energy Wh'].apply(getkwh))              # get sums and print

# new part
df['time'] = df['Date/time UTC'].apply(gettime)                             # get local time
df['night shift'] = df['time'].apply(lambda x: 1
 if (x > datetime.strptime('21:59','%H:%M').time() or x < datetime.strptime('06:00','%H:%M').time()) else 0)   #works

df['Night energy'] = df['Active energy Wh'] * df['night shift']
df['Day energy'] = df['Active energy Wh'] -  df['Night energy']
grouped_by_date = df.groupby(df['date'])                                    # group by date
#print(grouped_by_date.sum()['Night energy'].apply(getkwh))              # get sums and print
#print(grouped_by_date.sum()['Day energy'].apply(getkwh))              # get sums and print
print(grouped_by_date.sum().apply(getkwh))
df.to_csv('output.csv')

