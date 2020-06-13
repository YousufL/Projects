import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.request import urlopen
from time import time
from datetime import datetime
import pandas as pd
import numpy as np

from time import sleep
import time
from tqdm import tqdm

class EPScraperOHLDraftModel:

    def __init__(self, draft_year, draft_type, draft_length):

        self.draft_length = draft_length
        self.draft_type = draft_type
        self.draft_year = draft_year
        print("Elite Prospect scraper for OHL Draft year data")

    def Collect_Player_URL_From_Draft(self):

        start = 'https://www.eliteprospects.com/draft/'

        #Create URL
        url = start + self.draft_type + "/" + str(self.draft_year)

        #Get HTML and Soup
        html = urlopen(url)
        soup = BeautifulSoup(html,'html.parser')

        #Clean up HTML to get players
        hold = soup.find_all("td", class_="player")

        Player_Names = []
        for game in hold:
            try:
                links_name = game.find('a', href=True)
                Player_Names.append(links_name.text)
            except:
                AttributeError

        Player_URLs = []
        for game in hold:
            try:
                links_url = game.find('a', href=True)
                Player_URLs.append(links_url.get('href'))
            except:
                AttributeError

        Player_Names = Player_Names[5:self.draft_length+5]
        Player_URLs = Player_URLs[5:self.draft_length+5]

        self.Player_Names = Player_Names
        self.Player_URLs = Player_URLs

        return Player_URLs, Player_Names

    def Create_Data_Frame(self, games):

        Season = []
        Player_Results =[]
        Get_Link = []
        League = []
        Games_Played = []
        Assists = []
        Goals = []
        Points = []
        PIM = []
        Player_Results =[]
        Team_URL=[]
        League_Hold = games.find_all("td", class_='league')
        Games_Played_Hold = games.find_all("td", class_='regular gp')
        Goals_Hold = games.find_all("td", class_='regular g')
        Assists_Hold = games.find_all("td", class_='regular a')
        Points_Hold = games.find_all("td", class_='regular tp')
        PIM_Hold = games.find_all("td", class_='regular pim')
        Team_Hold = games.find_all("td", class_='team')

        for game in Team_Hold:
            try:
                links = game.find('a', href=True)
                Team_URL.append(links.get('href'))
            except AttributeError:
                Team_URL.append(0)

        for links in League_Hold:
            try:
                links_hold = links.find('a', href=True)
                Get_Link_Hold = links_hold.get('href')
                Get_Link.append(Get_Link_Hold)
            except AttributeError:
                Get_Link.append(0)


        for text in Get_Link:
            try:
                left_text = text.partition("/")[2]
                left_text = left_text.partition("/")[2]
                left_text = left_text.partition("/")[2]
                left_text = left_text.partition("/")[2]
                left_text = left_text.partition("/")[2]
                Season.append(left_text.partition("/")[2])
            except AttributeError:
                Season.append(0)


        for league in League_Hold:
            try:
                league.text.strip()
                cols =league.find_all('td')
                cols=[x.text.strip() for x in cols]
                League.append(league.text.strip())
            except AttributeError:
                League.append(0)


        for league in Games_Played_Hold:
            try:
                league.text.strip()
                cols=league.find_all('td')
                cols=[x.text.strip() for x in cols]
                Games_Played.append(league.text.strip())
            except AttributeError:
                Games_Played.append(0)

        for league in Goals_Hold:
            try:
                league.text.strip()
                cols=league.find_all('td')
                cols=[x.text.strip() for x in cols]
                Goals.append(league.text.strip())
            except AttributeError:
                Goals.append(0)


        for league in Assists_Hold:
            try:
                league.text.strip()
                cols=league.find_all('td')
                cols=[x.text.strip() for x in cols]
                Assists.append(league.text.strip())
            except AttributeError:
                Assists.append(0)
                print('error')

        for league in Points_Hold:
            try:
                league.text.strip()
                cols=league.find_all('td')
                cols=[x.text.strip() for x in cols]
                Points.append(league.text.strip())
            except AttributeError:
                Points.append(0)
                print('error')

        for league in PIM_Hold:
            try:
                league.text.strip()
                cols=league.find_all('td')
                cols=[x.text.strip() for x in cols]
                PIM.append(league.text.strip())
            except AttributeError:
                PIM.append(0)


        Player_Results = pd.DataFrame([Season, League, Games_Played, Goals, Assists, Points, PIM, Team_URL])
        Player_Results = pd.DataFrame(Player_Results.transpose())

        return Player_Results

    def Get_Player_Stats(self):
        DICT_MAP = {}
        Player_Birthday = []
        Player_Birthplace = []
        Player_Position = []
        Player_Height = []
        Team_URL=[]

        self.Player_URLs, self.Player_Names = self.Collect_Player_URL_From_Draft()

        for url, name in tqdm(zip(self.Player_URLs,self.Player_Names)):
            print(name)

            sleep(5)
            html = urlopen(url)
            soup = BeautifulSoup(html,'html.parser')

            attributes = soup.find_all("div", class_="col-xs-8 fac-lbl-dark")
            Player_Birthday.append(attributes[0].text.strip())
            Player_Birthplace.append(attributes[3].text.strip())
            Player_Position.append(attributes[5].text.strip())
            Player_Height.append(attributes[6].text.strip())

            games = soup.find(id='league-stats')
            self.games = games
            Results = self.Create_Data_Frame(self.games)
            DICT_MAP[name] = Results



            Test_Goalie = pd.DataFrame([Results.keys(), Player_Birthday, Player_Birthplace, Player_Position,
                  Player_Height]).transpose()
            Names = []
            Index = []

        for i in range(0,len(Test_Goalie)):
            if Test_Goalie[3][i] == 'G':
                Names.append(Test_Goalie[0][i])
                Index.append(i)

        for k in Names:
            del Results[k]

        n = 0
        for i in Index:
            del Player_Names[i-n]
            del Player_Birthday[i-n]
            del Player_Birthplace[i-n]
            del Player_Position[i-n]
            del Player_Height[i-n]
            n += 1

        self.Player_Position = Player_Position
        #self.DICT_MAP = DICT_MAP
        self.Player_Birthday = Player_Birthday
        self.Player_Height = Player_Height


        return  DICT_MAP


    def Get_Draft_Year_Data(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []

        for name, pos in zip(self.Player_Names,self.Player_Position):

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue
                if (int(year.partition("-")[2]) == draft_year):
                    DY_GP__ = Stats.loc[i,2]
                    if int(DY_GP__) > max_holder:
                        counter = i
                        max_holder= int(DY_GP__)

                        DY_League = Stats.loc[counter,1]

                        DY_GP = Stats.loc[counter,2]
                        DY_G =  Stats.loc[counter,3]
                        DY_A =  Stats.loc[counter,4]
                        DY_P =  Stats.loc[counter,5]
                        DY_PIM = Stats.loc[counter,6]


                HOLD = np.zeros(6)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def NHL_WC_Variables(self, Results, draft_year):
        NCAA_GP=0
        NHL_GP = 0
        NHL_G = 0
        NHL_A = 0
        NHL_P = 0
        NHL_WC_Vars = []

        for name, pos in zip(self.Player_Names,self.Player_Position):

            Stats = Results[name]
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == ''):
                    continue

                if (Stats[1][i] == "OHL"):
                    try:
                        NHL_GP += int(Stats.loc[i,2])
                        NHL_G  +=  int(Stats.loc[i,3])
                        NHL_A  +=  int(Stats.loc[i,4])
                        NHL_P  +=  int(Stats.loc[i,5])
                    except (TypeError, ValueError):
                        print("type error")

                if (Stats[1][i] == "NCAA"):
                    try:
                        NCAA_GP += int(Stats.loc[i,2])
                    except (TypeError, ValueError):
                        print("type error")

            HOLD = np.zeros(5)
            HOLD = np.array([NCAA_GP,NHL_GP,NHL_G,NHL_A,NHL_P])

            NHL_WC_Vars.append(HOLD)

        return NHL_WC_Vars

    def RunEverything(self):
        self.Results = self.Get_Player_Stats()
        y = self.Get_Draft_Year_Data(self.Results,self.draft_year)
        u = self.NHL_WC_Variables(self.Results, self.draft_year)
        the= []

        for i in range(0,len(y)):
            ry = pd.DataFrame([self.Player_Names[i]])
            dz = pd.DataFrame([self.Player_Birthday[i]])
            gh = pd.DataFrame([self.Player_Height[i]])
            y_ = pd.DataFrame([y[i]])
            u_ = pd.DataFrame([u[i]])
            ll = pd.concat([ry,dz,gh,y_,u_] ,axis=1)
            the.append(ll)

        column = ['NAME', 'BIRTHDAY',"HEIGHT",'DY_League', 'DY_GP', 'DY_G', 'DY_A', 'DY_P', 'DY_PIM','NCAA_GP', 'OHL_GP', 'OHL_G', 'OHL_A', 'OHL_P']
        df =pd.DataFrame(np.concatenate(the), columns = column)

        k = []
        for i in range(0,len(df)-1):
            if (df['DY_GP'][i] == df['DY_GP'][i+1]) and (df['DY_G'][i] == df['DY_G'][i+1]) and (df['DY_A'][i] == df['DY_A'][i+1]) and (df['DY_P'][i] == df['DY_P'][i+1]) and (df['DY_PIM'][i] == df['DY_PIM'][i+1]) and (df['DY_League'][i] == df['DY_League'][i+1]):
                print('the')
                k.append(i+1)

        n = 0
        for i in k:
            print(i)
            df = df.drop([i-n])
            n += 1


        return df
