import gspread
import httplib2
import datetime as dt
import numpy as np
import os
import pandas as pd

from config import *
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

# Read key into a variable
f = file(pk12, 'rb')
key = f.read()
f.close()

# Define scope and create credentials object
scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(svc_email, key, scope)

http = httplib2.Http()
http = credentials.authorize(http)

# Build drive and authorize gspread
d = build('drive', 'v2', http=http)
gs = gspread.authorize(credentials)

# Open worksheet and get all values
wks = gs.open('Flight Itineraries').sheet1
all = wks.get_all_values()

# Today's date in type string
t = dt.datetime.strftime(dt.date.today(), '%m/%d/%Y')


# Alternative using Pandas library
all_flights = pd.DataFrame(all[1:], columns=all[0])

flights_today = []
flights_tomorrow = []

# Go through the Departure Date column and extract flights that are leaving today or tomorrow.
for i,x in all_flights.D_Date.iteritems():
    if pd.to_datetime(x) == pd.to_datetime(t):
        flights_today.append(i)
    elif int(((pd.to_datetime(x) - pd.to_datetime(t)).total_seconds())/86400) == 1:
        flights_tomorrow.append(i)
    else:
        pass

# Grab the items in the today's flights' rows and push them out. Also record action in log.
if len(flights_today) != 0:
    for i in flights_today:
        x = all_flights.iloc[i]
        name, dep_city, dep_time, dep_flight, arr_city, arr_time = x['Person'], x['D_City'], x['D_Time'], x['D_Flight'], x['A_City'], x['A_Time']
        message = name +' is flying from '+dep_city+' at '+dep_time+' today on '+dep_flight+' and arriving at '+arr_time+' in '+ arr_city+'."'
        os.system(msg_dhruv+message)
	os.system(msg_ritika+message)
	os.system(msg_papa+message)
	os.system(msg_mamma+message)
	os.system(msg_mehul+message)
	os.system(msg_paavani+message)
    file = open('/home/dkar/dev/gpush/gpush.log', 'a')
    file.write('\n'+t+': '+str(len(flights_today))+ ' flight(s) today')
else:
    file = open('/home/dkar/dev/gpush/gpush.log', 'a')
    file.write('\n'+t+': No flights today')
    file.close()
