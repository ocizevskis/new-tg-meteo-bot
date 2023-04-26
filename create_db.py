import sqlite3
import update
import os



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
connection_obj.commit()
connection_obj.close()


update.create_data_table()