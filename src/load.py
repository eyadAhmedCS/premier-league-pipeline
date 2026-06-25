import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


conn = sqlite3.connect(os.getenv("DB_Loacation"))
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = cursor.fetchall()

if not tables:
    with open('database/schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()

def load_Seasons_data():
   try:
      df = pd.read_csv('data/processed/seasons.csv')
      table_name='Seasons'
      df.to_sql(table_name ,conn , if_exists='append', index=False)
   except Exception as e:
      print('an error have ocuurd in seasons loading', e)

def load_Teams_data():
   try:
      df = pd.read_csv('data/processed/teams.csv')
      table_name='Teams'
      df.to_sql(table_name ,conn , if_exists='append', index=False)
   except Exception as e:
      print('an error have ocuurd in teams loading', e)

def load_Matches_data():
   try:
      df = pd.read_csv('data/processed/matches.csv')
      table_name='Matches'
      df.to_sql(table_name ,conn , if_exists='append', index=False)
   except Exception as e:
      print('an error have ocuurd in matches loading', e)

def load_Standings_data():
   try:
      df = pd.read_csv('data/processed/standings.csv')
      table_name='Standings'
      df.to_sql(table_name ,conn , if_exists='append', index=False)
   except Exception as e:
      print('an error have ocuurd in standings loading', e)

def load_Match_Stats_data():
   try:
      df = pd.read_csv('data/processed/matches_stats.csv')
      table_name='Team_Match_Stats'
      df.to_sql(table_name ,conn , if_exists='append', index=False)
   except Exception as e:
      print('an error have ocuurd in team_match_stats loading', e)

def load_Coach_data():
   try:
      df = pd.read_csv('data/processed/coachs.csv')
      table_name='Coach'
      df.to_sql(table_name ,conn , if_exists='append', index=False)
   except Exception as e:
      print('an error have ocuurd in coachs loading', e)

def load_Coachs_teams_data():
   try:
      df = pd.read_csv('data/processed/coachs_teams.csv')
      table_name='Coachs_teams'
      df.to_sql(table_name ,conn , if_exists='append', index=False)
   except Exception as e:
      print('an error have ocuurd in coachs_teams loading', e)


def run():

   print('\nLoading seasons process started...')
   load_Seasons_data()
   print('Loading seasons process finished')

   print('\nLoading teams process started...')
   load_Teams_data()
   print('Loading teams process finished')

   print('\nLoading coachs process started...')
   load_Coach_data()
   print('Loading coachs process finished')

   print('\nLoading coachs_teams process started...')
   load_Coachs_teams_data()
   print('Loading coachs_teams process finished')

   print('\nLoading standings process started...')
   load_Standings_data()
   print('Loading standings process finished')

   print('\nLoading matches process started...')
   load_Matches_data()
   print('Loading matches process finished')

   print('\nLoading matches_stats process started...')
   load_Match_Stats_data()
   print('Loading maches_stats process finished')

   conn.close()   