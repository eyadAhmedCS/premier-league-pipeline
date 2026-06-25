# 1. import the important libararies
import requests
import os
import glob 
import time
import re
import json
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

#  setup impotant tool for requests
api_key=os.getenv("API_KEY")
api_url=os.getenv("API_HOST")
html_url=os.getenv('HTML_URL')
html_headers= os.getenv('REQUEST_HEADERS')

headers = {
        "x-apisports-key": api_key
    }

# the season we will extract 22/23 , 23/24, 24/25
seasons=list(range(2022,2025))

def extract_seasons():
     # check if we have allready read the matches
    if os.path.exists("data/raw/seasons/season_data.json"):
        pass
    else:
        response=requests.get(f"{api_url}leagues",headers=headers,params={"id":39})

        if response.json()['errors']:
            print("Failed to fetch seasons")
            return
    
        with open('data/raw/seasons/season_data.json','w') as f:
            json.dump(response.json(), f, indent=4)

def extract_teams_accros_seasons():

    for season in seasons:
         # check if we have allready read the teams
        if os.path.exists(f"data/raw/teams/teams{season}_data.json"):
            continue

        response=requests.get(f"{api_url}teams",headers=headers,params={"league":39,"season":season})

        if response.json()['errors']:
            print("Failed to fetch teams")
            break

        with open(f'data/raw/teams/teams{season}_data.json','w') as f:
            json.dump(response.json(), f, indent=4)

        print('done')    
        time.sleep(6)
    
def extract_seasons_standing():

    for season in seasons:
         # check if we have allready read the standing
        if os.path.exists(f"data/raw/standings/standings{season}_data.json"):
            continue

        response=requests.get(f"{api_url}standings",headers=headers,params={"league":39,"season":season})

        if response.json()['errors']:
            print("Failed to fetch standings")
            break

        with open(f'data/raw/standings/standings{season}_data.json','w') as f:
            json.dump(response.json(), f, indent=4)

        print('done')    
        time.sleep(6)

    print("Ectract standings proccess have end")    

def extract_seasons_matches():
    
    for season in seasons:
        # check if we have allready read the matches
        if os.path.exists(f"data/raw/fixtures/fixtures{season}_data.json"):
            continue

        response=requests.get(f"{api_url}fixtures",headers=headers,params={"league":39,"season":season})

        if response.json()['errors']:
            print("Failed to fetch matches")
            break

        with open(f'data/raw/fixtures/fixtures{season}_data.json','w') as f:
            json.dump(response.json(), f, indent=4)

        print('done')    
        time.sleep(6) 

def extract_seasons_matches_stats():

    # read the data about last pointer information
    with open('data/raw/matches_stats/pointer.txt','r') as f:
            pointer_list=f.read().split(",")

    # go to each season and then find the matches stats
    for i,file in enumerate(glob.glob("data/raw/fixtures/*.json")):

        pointer=int(pointer_list[i])
        season=re.findall(r'fixtures(\d+)',file)[0]

        # check if the file have allready read
        if pointer>=380 :
            print(f"[-] File {i+1} (Season {season}): Already completed ({pointer}/380).")
            continue

        print(f"[+] Processing File {i+1} (Season {season}) starting from match pointer: {pointer}")
            
        # read the response of all matches to find IDs
        with open(file,'r') as f:
            json_string=f.read()
        jsondata=json.loads(json_string)['response']
        try:
            # make the requests for matches stats until no requests remaining or  we reach the end of the json file
            total_matches = len(jsondata)
            while pointer < total_matches:

                # take the id for current match and send request using the id
                match_id=jsondata[pointer]['fixture']['id']

                response=requests.get(f"{api_url}fixtures/statistics",headers=headers,params={"fixture":match_id})

                if response.json()['errors']:
                    print(response.json()['errors'])
                    break

                # write the match stats to file
                with open(f'data/raw/matches_stats/{season}/matches_stats{match_id}_data.json','w') as f:
                    json.dump(response.json(), f, indent=4)

                pointer=pointer+1
                print(f"-> Match {pointer}/380 saved.")

                # check the remaining requests
                remaining = int(response.headers.get('x-ratelimit-requests-remaining', 0))
                if remaining <= 5:
                    print(f"Only {remaining} requests left today. Stopping.")
                    break

                time.sleep(7)  

        except Exception as e:
            print(f"Error during processing: {e}")        
        finally:     
            # save the pointer location for the current file
            with open('data/raw/matches_stats/pointer.txt','w') as f:
                pointer_list[i]=str(pointer)
                f.write(','.join(pointer_list))
                    
def extract_Coachs():
    # read all teams accros seasons
    for file in glob.glob("data/raw/teams/*.json"):  

        # read the response of all teams in particular season
        with open(file,'r') as f:
            json_string=f.read()
        teams=json.loads(json_string)['response']
        for team in teams:

            team_id=team['team']['id']
            team_name=team['team']['name']
            # check if we have allreday read the team id
            if os.path.exists(f"data/raw/coachs/coach{team_id}.json"):
                continue 

            response=requests.get(f"{api_url}coachs",headers=headers,params={'team':team_id})

            if response.json()['errors']:
                print("Failed to fetch coachs")
                return

            print(f"{team_name} coach Added :)")

            with open(f'data/raw/coachs/coach{team_id}.json','w') as f:
                json.dump(response.json(),f,indent=4)

            time.sleep(7)        

def extract_coaches_page():

    if os.path.exists(f"data/raw/coachs_teams/coachs_teams.html"):
        print('the page have already saved')
        return
    
    page_headers = {
    "User-Agent": html_headers
    }
    
    response= requests.get(html_url,headers= page_headers)

    if response.status_code != 200:
        print("Failed to fetch page")
        return
    
    html_page= response.text
    

    with open('data/raw/coachs_teams/coachs_teams.html','w', encoding='utf-8') as f:
        f.write(html_page)






def run():

    # 3. make the requests for all seasons
    print("\nEctract seasons proccess have started")
    extract_seasons()
    print("Ectract seasons proccess have ended")

    # 4. make the requests for all teams acrros all seasons
    print("\nEctract teams proccess have started")
    extract_teams_accros_seasons()
    print("Ectract teams proccess have ended")

    # 5. make the requests for standings acrros all seasons
    print("\nEctract standings proccess have started")
    extract_seasons_standing()
    print("Ectract standings proccess have ended")

    # 6. make the requests for all matches acrros all seasons
    print("\nEctract matches proccess have started")
    extract_seasons_matches()
    print("Ectract matches proccess have ended")

    # 7. make request for matches stats
    print("\nExtract Matches stas have started")
    extract_seasons_matches_stats()
    print("Extract Matches stats have ended")

    # 8. make the request for all coachs
    print("\nEctract coachs proccess have started")
    extract_Coachs()
    print("Ectract coachs proccess have ended")

    print("\nEctract coachs page proccess have started")
    extract_coaches_page()
    print("Ectract coachs page proccess have ended")