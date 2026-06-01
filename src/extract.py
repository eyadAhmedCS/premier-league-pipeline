# 1. import the important libararies
import requests
import pandas as pd
import json
import os
import sqlite3
import time
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# 2. setup impotant tool for requests
api_key=os.getenv("API_KEY")
api_url=os.getenv("API_HOST")

headers = {
    "x-apisports-key": api_key
}

conn = sqlite3.connect('D:/Api_project/premier-league-pipeline/data/raw/premier_league.db')


# 3. make the requests for all seasons

# the request for pL seasons dataas id =39 for PL
response=requests.get(f"{api_url}leagues",headers=headers,params={"id":39})
data=response.json()['response'][0]['seasons']
dictt={
       'year':[],
       'start_date':[],
       'end_date':[],
       'current':[]
       }

# add the seasons data to dictionary
for season in data:
    dictt['year'].append(season["year"])
    dictt['start_date'].append(season["start"])
    dictt['end_date'].append(season["end"])
    dictt['current'].append(season["current"])

# save the season data
df=pd.DataFrame(dictt)  
df.rename_axis('season_id', inplace=True)
df.to_sql('Seasons',conn,if_exists='replace',index=True)




    



# for season in seasons:



# 4. save the data to raw file