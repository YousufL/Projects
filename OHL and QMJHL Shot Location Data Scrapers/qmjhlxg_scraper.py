# -*- coding: utf-8 -*-
"""QMJHLxG Scraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-xdklon9hbA1yToA28mLB4gGpX0fhvZj
"""

import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.request import urlopen
from time import time
from datetime import datetime
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

!pip install -U selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def Get_Game_ID_URLS():

    wd = webdriver.Chrome('chromedriver',options=chrome_options)

    LINKS =[]

    wd.get('https://theqmjhl.ca/schedule')

    div = wd.find_elements_by_xpath('//*[@title="Game Centre"]')


    for i in range(0,572):
        LINKS.append(div[i].get_attribute('href'))
    
    return LINKS

Page_URLS = ['https://theqmjhl.ca/schedule/193','https://theqmjhl.ca/schedule/190','https://theqmjhl.ca/schedule/187',
             'https://theqmjhl.ca/schedule/184','https://theqmjhl.ca/schedule/181','https://theqmjhl.ca/schedule/178']

def Get_Game_ID_URLS(Page_URLS):
    wd1 = webdriver.Chrome('chromedriver',options=chrome_options)
    wd2 = webdriver.Chrome('chromedriver',options=chrome_options)
    wd3 = webdriver.Chrome('chromedriver',options=chrome_options)
    wd4 = webdriver.Chrome('chromedriver',options=chrome_options)
    wd5 = webdriver.Chrome('chromedriver',options=chrome_options)
    wd6 = webdriver.Chrome('chromedriver',options=chrome_options)

    LINKS =[]
    links = []
    links1 = []
    links2 = []
    links3 = []
    links4 = []
    links5 = []

    wd1.get(Page_URLS[0])
    wd2.get(Page_URLS[1])
    wd3.get(Page_URLS[2])
    wd4.get(Page_URLS[3])
    wd5.get(Page_URLS[4])
    wd6.get(Page_URLS[5])

    div = wd1.find_elements_by_xpath('//*[@title="Game Centre"]')
    div1 = wd2.find_elements_by_xpath('//*[@title="Game Centre"]')
    div2 = wd3.find_elements_by_xpath('//*[@title="Game Centre"]')
    div3 = wd4.find_elements_by_xpath('//*[@title="Game Centre"]')
    div4 = wd5.find_elements_by_xpath('//*[@title="Game Centre"]')
    div5 = wd6.find_elements_by_xpath('//*[@title="Game Centre"]')

    for i in range(0,572):
        links.append(div[i].get_attribute('href'))

    for i in range(0,len(div1)):
        links1.append(div1[i].get_attribute('href'))

    for i in range(0,len(div2)):
        links2.append(div2[i].get_attribute('href'))

    for i in range(0,len(div3)):
        links3.append(div3[i].get_attribute('href'))

    for i in range(0,len(div4)):
        links4.append(div4[i].get_attribute('href'))

    for i in range(0,len(div5)):
        links5.append(div5[i].get_attribute('href'))

    LINKS =  links+ links1 + links2 + links3 + links4 +links5
    #LINKS.append(links1)
    #LINKS.append(links2)
    #LINKS.append(links3)
    #LINKS.append(links4)
    print(len(links))
    print(len(links1))
    print(len(links2))
    print(len(links3))
    print(len(links4))
    print(len(links5))
    
    return LINKS

LINKS = Get_Game_ID_URLS(Page_URLS)

year_1 = pd.DataFrame(year_1)
year_1.columns = ['game_id']

year_2 = pd.DataFrame(year_2)
year_2.columns = ['game_id']

year_3 = pd.DataFrame(year_3)
year_3.columns = ['game_id']

year_4 = pd.DataFrame(year_4)
year_4.columns = ['game_id']

year_5 = pd.DataFrame(year_5)
year_5.columns = ['game_id']

year_6 = pd.DataFrame(year_6)
year_6.columns = ['game_id']

year_1['game_id'] = year_1['game_id'].map(lambda x: x.split('/')[4])
year_2['game_id'] = year_2['game_id'].map(lambda x: x.split('/')[4])
year_3['game_id'] = year_3['game_id'].map(lambda x: x.split('/')[4])
year_4['game_id'] = year_4['game_id'].map(lambda x: x.split('/')[4])
year_5['game_id'] = year_5['game_id'].map(lambda x: x.split('/')[4])
year_6['game_id'] = year_6['game_id'].map(lambda x: x.split('/')[4])

year_1['year'] = '2019-2020'
year_2['year'] = '2018-2019'
year_3['year'] = '2017-2018'
year_4['year'] = '2016-2017'
year_5['year'] = '2015-2016'
year_6['year'] = '2014-2015'

Years = pd.concat([year_1,year_2,year_3,year_4,year_5,year_6],axis=0)

from google.colab import files

Years.to_csv('year_game_id_QMJHL.csv')
files.download('year_game_id_QMJHL.csv')

def Construct_JSON_links(links):
    JSON_links = []



    start = 'https://cluster.leaguestat.com/feed/index.php?feed=gc&key=f322673b6bcae299&client_code=lhjmq&game_id='

    end = '&lang_code=en&fmt=json&tab=pxpverbose'

    game_ID = []

    for i in range(0,len(links)):
        game_ID.append(links[i].split('/')[4])

    for i in range(0,len(game_ID)):
        JSON_links.append(start +game_ID[i] + end)

    return JSON_links

jsons = Construct_JSON_links(LINKS)

len(jsons)

def construct_assist_dataframe(jsons):
    Goal_Scorer_First_Name = []
    Goal_Scorer_Last_Name = []
    Assist1_Scorer_ID = []
    #Assist1_Scorer_Last_Name = []
    Assist2_Scorer_ID = []
    #Assist2_Scorer_Last_Name = []
    power_play = []
    empty_net = []
    penalty_shot = []
    short_handed = []
    insurance_goal = []
    game_winning = []
    game_tieing = []
    Team_Name = []




    Assist_1_ID = []
    Assist_2_ID = []

    for i in tqdm(range(0,3634)):
        #do
        DATA = requests.get(jsons[i]).json()
        length = DATA["GC"]['Pxpverbose']


        for i in range(0,len(length)):
            if DATA["GC"]['Pxpverbose'][i]['event'] == 'shot':
                if (DATA["GC"]['Pxpverbose'][i]['shot_quality_description'] == 'Quality goal') | (DATA["GC"]['Pxpverbose'][i]['shot_quality_description'] == 'Non quality goal'):
                    #print(DATA["GC"]['Pxpverbose'][i+1])
                    try:
                        Team_Name.append(DATA["GC"]['Pxpverbose'][i+1]['goal_scorer']['team_code'])
                        Goal_Scorer_First_Name.append(DATA["GC"]['Pxpverbose'][i+1]['goal_scorer']['first_name'])
                        Goal_Scorer_Last_Name.append(DATA["GC"]['Pxpverbose'][i+1]['goal_scorer']['last_name'])
                        Assist1_Scorer_ID.append(DATA["GC"]['Pxpverbose'][i+1]['assist1_player_id'])
                        #Assist1_Scorer_Last_Name.append(DATA["GC"]['Pxpverbose'][i+1]['assist1_player']['last_name'])
                        Assist2_Scorer_ID.append(DATA["GC"]['Pxpverbose'][i+1]['assist2_player_id'])
                        #Assist2_Scorer_Last_Name.append(DATA["GC"]['Pxpverbose'][i+1]['assist2_player']['last_name'])
                        power_play.append(DATA["GC"]['Pxpverbose'][i+1]['power_play'])
                        empty_net.append(DATA["GC"]['Pxpverbose'][i+1]['empty_net'])
                        penalty_shot.append(DATA["GC"]['Pxpverbose'][i+1]['penalty_shot'])
                        short_handed.append(DATA["GC"]['Pxpverbose'][i+1]['short_handed'])
                        insurance_goal.append(DATA["GC"]['Pxpverbose'][i+1]['insurance_goal'])
                        game_winning.append(DATA["GC"]['Pxpverbose'][i+1]['game_winning'])
                        game_tieing.append(DATA["GC"]['Pxpverbose'][i+1]['game_tieing'])
                    except KeyError:
                        print('key')

    Team_Name = pd.DataFrame(Team_Name)
    Goal_Scorer_First_Name = pd.DataFrame(Goal_Scorer_First_Name)
    Goal_Scorer_Last_Name  = pd.DataFrame(Goal_Scorer_Last_Name)
    Assist1_Scorer_ID  = pd.DataFrame(Assist1_Scorer_ID)
    #Assist1_Scorer_Last_Name =  pd.DataFrame(Assist1_Scorer_Last_Name)
    Assist2_Scorer_ID = pd.DataFrame(Assist2_Scorer_ID)
    #Assist2_Scorer_Last_Name  = pd.DataFrame(Assist2_Scorer_Last_Name)
    power_play  = pd.DataFrame(power_play)
    empty_net = pd.DataFrame(empty_net)
    penalty_shot  = pd.DataFrame(penalty_shot)
    short_handed  = pd.DataFrame(short_handed)
    insurance_goal  = pd.DataFrame(insurance_goal)
    game_winning  = pd.DataFrame(game_winning)
    game_tieing  = pd.DataFrame(game_tieing)

    Special = pd.concat([Team_Name, Goal_Scorer_First_Name,Goal_Scorer_Last_Name,Assist1_Scorer_ID,Assist2_Scorer_ID,
                        power_play,empty_net,penalty_shot,short_handed,insurance_goal,game_winning,game_tieing],axis=1)

    Special.columns = ['Team_Name','Goal_Scorer_First_Name','Goal_Scorer_Last_Name','Assist1_Scorer_ID','Assist2_Scorer_ID',
                        'power_play','empty_net','penalty_shot','short_handed','insurance_goal','game_winning','game_tieing']


                                               
    return Special

from tqdm import tqdm
import time

DATA = construct_assist_dataframe(jsons)

from google.colab import files

DATA.to_csv('QMJHLASSISTS.csv')
files.download('QMJHLASSISTS.csv')

def Construct_Shot_DataFrame(jsons):
    
    from tqdm import tqdm
    import time

    event = []
    goalie_firstname = []
    goalie_lastname = []
    goalie_ID = []
    goalie_team = []
    goalie_teamID = []

    player_firstname = []
    player_lastname = []
    player_ID = [] 
    player_team = []
    player_teamID = []

    quality = []
    s_ = []
    shot_quality_description = []
    shot_type = []
    shot_type_description = []
    time__ = []
    time_formatted = []
    x_location = []
    y_location = []
    game_ID = []
    home = []
    period = []
    Goal_Type = []

    for i in tqdm(range(0,len(jsons))):
        #do
        DATA = requests.get(jsons[i]).json()
        length = DATA["GC"]['Pxpverbose']

        for i in range(0,len(length)):

            if DATA["GC"]['Pxpverbose'][i]['event'] == 'shot':
                
                period.append(DATA["GC"]['Pxpverbose'][i]['period_id'])
                home.append(DATA["GC"]['Pxpverbose'][i]['home'])
                game_ID.append(DATA["GC"]['Parameters']['game_id'])
                event.append(DATA["GC"]['Pxpverbose'][i]['event'])
                goalie_firstname.append(DATA["GC"]['Pxpverbose'][i]['goalie']['first_name'])
                goalie_lastname.append(DATA["GC"]['Pxpverbose'][i]['goalie']['last_name'])
                goalie_ID.append(DATA["GC"]['Pxpverbose'][i]['goalie_id'])
                goalie_team.append(DATA["GC"]['Pxpverbose'][i]['goalie']['team_code'])
                goalie_teamID.append(DATA["GC"]['Pxpverbose'][i]['goalie_team_id'])

                player_firstname.append(DATA["GC"]['Pxpverbose'][i]['player']['first_name'])
                player_lastname.append(DATA["GC"]['Pxpverbose'][i]['player']['last_name'])
                player_ID.append(DATA["GC"]['Pxpverbose'][i]['player']['player_id'])
                player_team.append(DATA["GC"]['Pxpverbose'][i]['player']['team_code'])
                player_teamID.append(DATA["GC"]['Pxpverbose'][i]['player']['team_id'])

                quality.append(DATA["GC"]['Pxpverbose'][i]['quality'])
                s_.append(DATA["GC"]['Pxpverbose'][i]['s'])
                shot_quality_description.append(DATA["GC"]['Pxpverbose'][i]['shot_quality_description'])
                shot_type.append(DATA["GC"]['Pxpverbose'][i]['shot_type'])
                shot_type_description.append(DATA["GC"]['Pxpverbose'][i]['shot_type_description'])
                time__.append(DATA["GC"]['Pxpverbose'][i]['time'])
                time_formatted.append(DATA["GC"]['Pxpverbose'][i]['time_formatted'])
                x_location.append(DATA["GC"]['Pxpverbose'][i]['x_location'])
                y_location.append(DATA["GC"]['Pxpverbose'][i]['y_location'])

                if (DATA["GC"]['Pxpverbose'][i]['shot_quality_description'] == 'Quality goal') or (DATA["GC"]['Pxpverbose'][i]['shot_quality_description'] == 'Non quality goal'):
                    try:
                        Goal_Type.append(DATA["GC"]['Pxpverbose'][i]['goal_type_name'])
                    except KeyError:
                        Goal_Type.append("ERROR")

                if (DATA["GC"]['Pxpverbose'][i]['shot_quality_description'] == 'Quality on net') or (DATA["GC"]['Pxpverbose'][i]['shot_quality_description'] == 'Non quality on net'):
                    Goal_Type.append("NULL")

            if DATA["GC"]['Pxpverbose'][i]['event'] == 'penalty':
                
                period.append(DATA["GC"]['Pxpverbose'][i]['period_id'])
                home.append(DATA["GC"]['Pxpverbose'][i]['home'])
                game_ID.append(DATA["GC"]['Parameters']['game_id'])
                event.append("Penalty")
                goalie_firstname.append("NA")
                goalie_lastname.append("NA")
                goalie_ID.append("NA")
                goalie_team.append("NA")
                goalie_teamID.append("NA")

                player_firstname.append("NA")
                player_lastname.append("NA")
                player_ID.append("NA")
                player_team.append(DATA["GC"]['Pxpverbose'][i]['player_served_info']['team_code'])
                player_teamID.append(DATA["GC"]['Pxpverbose'][i]['player_served_info']['team_id'])

                quality.append("NA")
                s_.append("NA")
                shot_quality_description.append(DATA["GC"]['Pxpverbose'][i]['penalty_class'])
                shot_type.append(DATA["GC"]['Pxpverbose'][i]['lang_penalty_description'])
                shot_type_description.append(DATA["GC"]['Pxpverbose'][i]['pp'])
                time__.append(DATA["GC"]['Pxpverbose'][i]['minutes_formatted'])
                time_formatted.append(DATA["GC"]['Pxpverbose'][i]['time_off_formatted'])
                x_location.append("NA")
                y_location.append("NA")
                Goal_Type.append("Penalty")

            if DATA["GC"]['Pxpverbose'][i]['event'] == 'faceoff':

                period.append(DATA["GC"]['Pxpverbose'][i]['period'])
                home.append("NA")
                game_ID.append(DATA["GC"]['Parameters']['game_id'])
                event.append("Faceoff")
                goalie_firstname.append("NA")
                goalie_lastname.append("NA")
                goalie_ID.append("NA")
                goalie_team.append("NA")
                goalie_teamID.append("NA")

                player_firstname.append("NA")
                player_lastname.append("NA")
                player_ID.append("NA")
                player_team.append("NA")
                player_teamID.append("NA")

                quality.append("NA")
                s_.append("NA")
                shot_quality_description.append("NA")
                shot_type.append("NA")
                shot_type_description.append("NA")
                time__.append(DATA["GC"]['Pxpverbose'][i]['time'])
                time_formatted.append(DATA["GC"]['Pxpverbose'][i]['time_formatted'])
                x_location.append("NA")
                y_location.append("NA")
                Goal_Type.append("NONE")




                
    event = pd.DataFrame(event)
    goalie_firstname = pd.DataFrame(goalie_firstname)
    goalie_lastname = pd.DataFrame(goalie_lastname)
    goalie_ID = pd.DataFrame(goalie_ID)
    goalie_team = pd.DataFrame(goalie_team)
    goalie_teamID = pd.DataFrame(goalie_teamID)

    player_firstname = pd.DataFrame(player_firstname)
    player_lastname = pd.DataFrame(player_lastname)
    player_ID = pd.DataFrame(player_ID)
    player_team = pd.DataFrame(player_team)
    player_teamID = pd.DataFrame(player_teamID)

    quality = pd.DataFrame(quality)
    s_ = pd.DataFrame(s_)
    shot_quality_description = pd.DataFrame(shot_quality_description)
    shot_type = pd.DataFrame(shot_type)
    shot_type_description = pd.DataFrame(shot_type_description)
    time__ = pd.DataFrame(time__)
    time_formatted = pd.DataFrame(time_formatted)
    x_location = pd.DataFrame(x_location)
    y_location = pd.DataFrame(y_location)
    game_ID = pd.DataFrame(game_ID)

    home = pd.DataFrame(home)
    period = pd.DataFrame(period)
    Goal_Type = pd.DataFrame(Goal_Type)


    Shots = pd.concat([event, goalie_firstname,goalie_lastname,goalie_ID,goalie_team,goalie_teamID,player_firstname,player_lastname,
                  player_ID,player_team,player_teamID,quality,s_,shot_quality_description,
                  shot_type,shot_type_description,time__,time_formatted,x_location,y_location,game_ID,home,period, Goal_Type],axis=1)
    

    Shots.columns = ['event', 'goalie_firstname','goalie_lastname','goalie_ID','goalie_team','goalie_teamID','player_firstname','player_lastname',
                  'player_ID','player_team','player_teamID','quality','s_','shot_quality_description','shot_type','shot_type_description','time',
                  'time_formatted','x_location','y_location','game_ID','home','period','Goal_Type']

    return Shots

SHOTS= Construct_Shot_DataFrame(Json_Links)

SHOTS['Goal_Type'] = SHOTS['Goal_Type'].replace('','EV')

SHOTS

from google.colab import files

SHOTS.to_csv('qmjhlshots2014-2015.csv')
files.download('qmjhlshots2014-2015.csv')

"""# HANDEDNESS DATA"""

import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.request import urlopen
from time import time
from datetime import datetime
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

!pip install -U selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

import pandas as pd
downloaded = drive.CreateFile({'id': '1d2pmTpmK5B_aEo8a5tNvwEh7jLdNPdjJ' }) 
downloaded.GetContentFile('QMJHL_SHOTS_2014_2020.csv') 
Data = pd.read_csv('QMJHL_SHOTS_2014_2020.csv', encoding='latin-1')

GOALIE_IDs = Data['goalie_ID'].unique()
GOALIE_IDs = GOALIE_IDs [GOALIE_IDs  != 0]
GOALIE_IDs = GOALIE_IDs[np.logical_not(np.isnan(GOALIE_IDs))]
GOALIE_IDs

PLAYER_IDs = Data['player_ID'].unique()
PLAYER_IDs = PLAYER_IDs [PLAYER_IDs  != 0]
PLAYER_IDs = PLAYER_IDs[np.logical_not(np.isnan(PLAYER_IDs))]

IDs = np.concatenate((PLAYER_IDs,GOALIE_IDs),axis=None)

IDs = int(IDs)

IDs

def Create_PlayerHand(IDs):
    Player_URL = []
    start = 'https://theqmjhl.ca/players/'
    for i in range(0,len(IDs)):
        Player_URL.append(start+str(int(IDs[i])))

    return Player_URL

URLs = Create_PlayerHand(IDs)

URLs

def Get_Handedness(URLs):
    Handedness = []

    for i in tqdm(range(1500,1602)):
        time.sleep(2)
        wd = webdriver.Chrome('chromedriver',options=chrome_options)
        wd.get(URLs[i])
        div = wd.find_elements_by_xpath('//*[@width=40]')
        try:
            Handedness.append(div[0].text)
        except IndexError:
            Handedness.append("Error")

    return Handedness

Handedness = Get_Handedness(URLs)

Handedness = pd.DataFrame(Handedness)

len(Handedness)

IDs = pd.DataFrame(IDs)

IDs = IDs[1500:1602]
IDs = IDs.reset_index()

Handedness_Data = pd.concat([IDs.iloc[:,1],Handedness],axis=1)
Handedness_Data.columns = ['IDs','Shoots']

Handedness_Data

Handedness

from google.colab import files

Handedness_Data.to_csv('Handedness_Data1500_1602.csv')
files.download('Handedness_Data1500_1602.csv')