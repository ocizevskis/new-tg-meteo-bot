import sqlite3
import os
import time
import requests
import json
if 'meteo.db' in os.listdir():
    os.remove('meteo.db')
    
    
connection_obj = sqlite3.connect('meteo.db')
cursor_obj = connection_obj.cursor()

water_levels = """CREATE TABLE data (
station TEXT PRIMARY KEY, 
river TEXT,
Lat REAL, 
Lon REAL, 
plot_url TEXT,
date TEXT,
level REAL 
);"""

cursor_obj.execute(water_levels)


water_levels = """CREATE TABLE user_rivers (
chatid INTEGER,
station TEXT,
threshold REAL,
is_notified INTEGER,
PRIMARY KEY(chatid,station)
);"""
cursor_obj.execute(water_levels)

station_ids = []
# for i in station_ids:
h = requests.get("https://videscentrs.lvgmc.lv/data/hymer_overview")
hymer_data = json.loads(h.text)

print(h.text)
for j in range(80):
    if hymer_data[j]["ts"][0]["name"] == "Ūdens līmenis":
        name = hymer_data[j]["name"].split(",")
        print(name)
        river,station = name[0],name[1][1:]
        value = hymer_data[j]["ts"][0]["value"]
        date = hymer_data[j]["ts"][0]["last_date"]
        lat = hymer_data[j]["lat"]
        lon = hymer_data[j]["lon"]
        plot = hymer_data[j]["plots"][0]["url"]
        i = (station,river,lat,lon,plot,date,value)
        sqlite_insert_with_param = f"""INSERT INTO data
                              VALUES (?,?,?,?,?,?,?);"""
        connection_obj.commit()
        cursor_obj.execute(sqlite_insert_with_param,i)
        connection_obj.commit()

        station_ids.append(i)

print(station_ids)
'''

    print(i,h.status_code)
    h.close()
    if h.status_code == 200:
        sqlite_insert_with_param = f"""INSERT INTO STATION_IDs
                              (Station_ID, name) 
                              VALUES ({i[0]}, '{i[1]}');"""
        cursor_obj.execute(sqlite_insert_with_param)
        print(cursor_obj.rowcount)
        connection_obj.commit()
'''

connection_obj.close()
