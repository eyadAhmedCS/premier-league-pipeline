import json
import glob 
import pandas as pd
import os
from bs4 import BeautifulSoup
import io


def transform_seasons():

    # make to checks before start
    if not os.path.exists("data/raw/seasons/season_data.json"):
        print('The raw data file not exists :(')
        return
    
    if os.path.exists("data/processed/seasons.csv"):
        print('the season file have already transformed and saved')
        return
    
    # initialize list to enter all data from json file
    data_list=[]

    # read the data from json file and preper it to append to the data_list
    with open("data/raw/seasons/season_data.json",'r') as f:
        raw_data=f.read()
    seasons=json.loads(raw_data)['response'][0]['seasons']

    # add all seasons data to the data_list
    for season in seasons:

        year=season['year']
        start_date=season['start']
        end_date=season['end']
        current=season['current']

        data_list.append( (year,start_date,end_date,current) )

    # transform the list to dataframe then save it as csv file
    df=pd.DataFrame(data_list,columns=['year','start_date','end_date','current'])
    df.to_csv("data/processed/seasons.csv",index=False)
    print('Season transformation process have succeeded')
   
def transform_teams():

    # make to checks before start
    files= glob.glob("data/raw/teams/*.json")
    if len(files) == 0:
        print('The raw data files not exists :(')
        return
    
    if os.path.exists("data/processed/teams.csv"):
        print('the teams file have already transformed and saved')
        return
    
    # go to each file and extract data
    data_list=set()

    for file in files:

        # read the data from json file and preper it to append to the data_list
        with open(file,'r') as f:
            raw_data=f.read()
        teams=json.loads(raw_data)['response']

        # add all teams data to the data_list
        for team in teams:

            team_id= team['team']['id']
            name= team['team']['name']
            city= team['venue']['city']
            stadium=team['venue']['name']
            capacity=team['venue']['capacity']
            founded_year=team['team']['founded']

            record=(team_id,name,city,stadium,capacity,founded_year)

            if record in data_list:
                continue

            data_list.add(record)

    # transform the list to dataframe then save it as csv file
    df= pd.DataFrame(data_list,columns=['team_id','name','city','stadium','capacity','founded_year'])    
    df.to_csv("data/processed/teams.csv",index=False)
    print('teams transformation process have succeeded')

def transform_coachs():

    # make to checks before start
    files= glob.glob("data/raw/coachs_teams/*.html")
    if len(files) == 0:
        print('The raw data files not exists :(')
        return
    
    if os.path.exists("data/processed/coachs.csv"):
        print('the coachs file have already transformed and saved')
        return
    
    # reading the data by beutifulsoup and edit it to make it usable for pandas dataframe
    with open('data/raw/coachs_teams/coachs_teams.html','r',encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # replace the country place from alt to img, in html text to apper in the frame
    for img in soup.find_all('table')[1].find_all('img'):
        if img.get('alt'):
            img.replace_with(img['alt'])    

    # translate object to text then use io to pass it to the frame
    html_edited_text=str(soup)
    df=pd.read_html(io.StringIO(html_edited_text),flavor='lxml',match='From')[0]
    
    # filter unwanted symbols
    df['Name'] = df['Name'].str.replace(r'[‡§†]', '', regex=True)
    df['Name'] = df['Name'].str.strip()

    # add missing columns and rename some columns
    df=df[['Name','Nat.']]
    df['date_of_birth']=None
    df.rename(columns={'Name': 'name', 'Nat.': 'nationality'}, inplace=True)
    df.rename_axis('coach_id',inplace=True)
    df.drop_duplicates(inplace = True)


    df.to_csv('data/processed/coachs.csv')
    print('coachs transformation process have succeeded')

def transform_coachs_teams():

      # make to checks before start
    files= glob.glob("data/raw/coachs_teams/*.html")
    if len(files) == 0:
        print('The raw data files not exists :(')
        return
    
    if not os.path.exists("data/processed/coachs.csv"):
        print('The coachs data files not exists :(')
        return
    
    if not os.path.exists("data/processed/teams.csv"):
        print('The teams data files not exists :(')
        return
    
    if os.path.exists("data/processed/coachs_teams.csv"):
        print('the coachs_teams file have already transformed and saved')
        return

    # Initialize the important attributes
    page = 'data/raw/coachs_teams/coachs_teams.html'
    coach_path='data/processed/coachs.csv'
    team_path='data/processed/teams.csv'
    coachs_teams = pd.read_html(page,flavor='lxml',match='From')[0]
    coach_table=pd.read_csv(coach_path)
    team_table=pd.read_csv(team_path)   

    # make mapping for teams names before join
    team_mapping = {
    'Newcastle': 'Newcastle United',
    'Wolves': 'Wolverhampton Wanderers',
    'Leicester': 'Leicester City',
    'Tottenham': 'Tottenham Hotspur',
    'West Ham': 'West Ham United',
    'Brighton': 'Brighton & Hove Albion',
    'Leeds': 'Leeds United',
    'Sheffield Utd': 'Sheffield United',
    'Luton': 'Luton Town',
    'Ipswich': 'Ipswich Town'
}
    team_table['name']= team_table['name'].replace(team_mapping)
    
    # Delete spaces before join
    coachs_teams['Club']=coachs_teams['Club'].str.strip()
    
    # join 2 tables to add the team id and delete unwanted teams
    teams_join=pd.merge(coachs_teams,team_table,left_on='Club',right_on='name',how='inner')
    
    # delete ambigous symbols
    teams_join['Name'] = teams_join['Name'].str.replace(r'[‡§†]', '', regex=True)
    teams_join['Name']=teams_join['Name'].str.strip()

    # join 2 tables to add the coach id
    coach_join= pd.merge(teams_join,coach_table,left_on='Name',right_on='name',how='inner')
    
    

    # Delete unwanted symbols
    coach_join['From'] = coach_join['From'].str.split('[').str[0].str.strip()
    coach_join.replace('Present*',None,inplace=True)

    # set the type for date columns
    coach_join['From']= pd.to_datetime(coach_join['From'])
    coach_join['Until']=pd.to_datetime(coach_join['Until'])



    # filter the columns not in the 2022, 2023, 2024 premuier leugue seasons
    frame_result =coach_join[
        ( coach_join['From'] < pd.to_datetime('2025-06-01') ) 
                                &
          ( (coach_join['Until'].isna()) | (coach_join['Until'] >= pd.to_datetime('2022-08-05')))
]
    # Delete any coach that was in championship in that period
    frame_result= frame_result[
        ( frame_result['Years in League'].str.split('–').str[0] != '2025' ) |
        ( frame_result['From'] > pd.to_datetime('2025-01-01') )
        ]


    # Delete unwanted columns
    frame_result= frame_result[['coach_id','team_id','From','Until']]
    
    frame_result.rename(columns={'From': 'start_date', 'Until': 'end_date'}, inplace=True)
    frame_result.to_csv('data/processed/coachs_teams.csv',index=False)
    print('coachs_teams transformation process have succeeded')

def transform_standings():

    # make to checks before start
    files= glob.glob("data/raw/standings/*.json")
    if len(files) == 0:
        print('The raw data files not exists :(')
        return
    
    if os.path.exists("data/processed/standings.csv"):
        print('the standings file have already transformed and saved')
        return
    
    # go to each file and extract data
    data_list=set()

    for file in files:

        # read the data from json file and preper it to append to the data_list
        with open(file,'r') as f:
            raw_data=f.read()
        standings=json.loads(raw_data)['response'][0]['league']

        year= standings['season']
        season=standings['standings'][0]
        
        # add all standings data to the data_list
        for team in season:

            team_id= team['team']['id']
            matchweek= team['all']['played']
            rank= team['rank']
            points= team['points']
            wins= team['all']['win']
            draws= team['all']['draw']
            losses= team['all']['lose']
            goals_for= team['all']['goals']['for']
            goals_against= team['all']['goals']['against']
            goals_diff=  int(goals_for) - int(goals_against)

            record=(matchweek,team_id,year,rank,points,wins,draws,losses,goals_for,goals_against,goals_diff)

            if record in data_list:
                continue

            data_list.add(record)

    # transform the list to dataframe then save it as csv file
    df= pd.DataFrame(data_list,
        columns=['matchweek','team_id','season_id','rank','points','wins','draws','losses','goals_for','goals_against','goals_diff'])    
    df.to_csv("data/processed/standings.csv",index=False)
    print('standings transformation process have succeeded')

def transform_matches():

    # make to checks before start
    files= glob.glob("data/raw/fixtures/*.json")
    if len(files) == 0:
        print('The raw data files not exists :(')
        return
    
    if os.path.exists("data/processed/matches.csv"):
        print('the matches file have already transformed and saved')
        return
    
    # go to each file and extract data
    data_list=set()

    for file in files:

        # read the data from json file and preper it to append to the data_list
        with open(file,'r') as f:
            raw_data=f.read()

        json_data=json.loads(raw_data)
        fixtures=json_data['response']
        season_id=json_data['parameters']['season']
        
        # add all standings data to the data_list
        for match in fixtures:

            match_id= match['fixture']['id']
            match_date= match['fixture']['date']
            matchweek= int(match['league']['round'].split('- ')[1])
            referee= match['fixture']['referee']
            status= match['fixture']['status']['long']
            home_score_ht= match['score']['halftime']['home']
            away_score_ht= match['score']['halftime']['away']
            home_score_ft= match['score']['fulltime']['home']
            away_score_ft= match['score']['fulltime']['away']
            home_team_id=  match['teams']['home']['id']
            away_team_id= match['teams']['away']['id']
            check= match['teams']

            if check['home']['winner']== True:
                winner_team_id= home_team_id
            elif  check['away']['winner']== True:
                winner_team_id=away_team_id
            else:
                winner_team_id=None

            record=(match_id,match_date,matchweek,referee,status,home_score_ht,away_score_ht,home_score_ft,away_score_ft,home_team_id,away_team_id,season_id,winner_team_id)

            
            if record in data_list:
                continue

            data_list.add(record)

    # transform the list to dataframe then save it as csv file
    df= pd.DataFrame(data_list,
        columns=['match_id','match_date','matchweek','referee','status','home_score_ht','away_score_ht','home_score_ft','away_score_ft','home_team_id','away_team_id','season_id','winner_team_id'])    
    df.to_csv("data/processed/matches.csv",index=False)
    print('matches transformation process have succeeded')

def transform_matches_stats():

    # make to checks before start
    folder= glob.glob(f"data/raw/matches_stats/2*")

    for year in range(2022,2025):
        files= glob.glob(f"data/raw/matches_stats/{year}/*.json")
        if len(files) == 0:
            print(f'The {year} raw data files not exists :(')
            return
    
    if os.path.exists("data/processed/matches_stats.csv"):
        print('the matches_stats file have already transformed and saved')
        return
    
    # go to each file and extract data
    data_list=set()

    for files in folder:

        files= glob.glob(f'{files}/*.json')

        for file in files:

            # read the data from json file and preper it to append to the data_list
            with open(file,'r') as f:
                raw_data=f.read()

            json_data=json.loads(raw_data)
            matches_stats=json_data['response']
            match_id=json_data['parameters']['fixture']
            
            # add all standings data to the data_list
            for match in matches_stats:

                team_id = match['team']['id']
                stats = {s['type']: s['value'] for s in match['statistics']}
                possession =stats.get('Ball Possession')
                shots_total = stats.get('Total Shots')
                shots_on_target = stats.get('Shots on Goal')
                corners = stats.get('Corner Kicks')
                fouls = stats.get('Fouls')
                offsides = stats.get('Offsides')
                yellow_cards = stats.get('Yellow Cards')
                red_cards = stats.get('Red Cards')
                passes_total = stats.get('Total passes')
                passes_accuracy = stats.get('Passes %')
                expected_goals=stats.get('expected_goals')


                

                record=(match_id,team_id,possession,shots_total,shots_on_target,corners,fouls,offsides,yellow_cards,red_cards,passes_total,passes_accuracy,expected_goals)

                if record in data_list:
                    continue

                data_list.add(record)

    # transform the list to dataframe then save it as csv file
    df= pd.DataFrame(data_list,
        columns=['match_id','team_id','possession','shots_total','shots_on_target','corners','fouls','offsides','yellow_cards','red_cards','passes_total','passes_accuracy','expected_goals'])    
    df['red_cards'] = df['red_cards'].fillna(0)
    df['yellow_cards'] = df['yellow_cards'].fillna(0)
    df['offsides'] = df['offsides'].fillna(0)
    df['possession'] = df['possession'].str.replace('%', '').astype(float) / 100
    df['passes_accuracy'] = df['passes_accuracy'].str.replace('%', '').astype(float) / 100

    df.to_csv("data/processed/matches_stats.csv",index=False)
    print('matches stats transformation process have succeeded')



print('\nTransforming seasons process started...')
transform_seasons()
print('Transforming seasons process finished')

print('\nTransforming teams process started...')
transform_teams()
print('Transforming teams process finished')

print('\nTransforming coachs process started...')
transform_coachs()
print('Transforming coachs process finished')

print('\nTransforming coachs_teams process started...')
transform_coachs_teams()
print('Transforming coachs_teams process finished')

print('\nTransforming standings process started...')
transform_standings()
print('Transforming standings process finished')

print('\nTransforming matches process started...')
transform_matches()
print('Transforming matches process finished')

print('\nTransforming matches_stats process started...')
transform_matches_stats()
print('Transforming maches_stats process finished')
