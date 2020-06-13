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

class EPScraperNHLDraftModelPrime:

    def __init__(self, draft_year, draft_type, draft_length):

        self.draft_length = draft_length
        self.draft_type = draft_type
        self.draft_year = draft_year
        print("Elite Prospect scraper for Draft year and Draft year -1 variables")

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
        try:
            League_Hold = games.find_all("td", class_='league')
            Games_Played_Hold = games.find_all("td", class_='regular gp')
            Goals_Hold = games.find_all("td", class_='regular g')
            Assists_Hold = games.find_all("td", class_='regular a')
            Points_Hold = games.find_all("td", class_='regular tp')
            PIM_Hold = games.find_all("td", class_='regular pim')
            Team_Hold = games.find_all("td", class_='team')
        except AttributeError:
            print('')

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

            sleep(8)
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

        self.Player_Position = Player_Position
        #self.DICT_MAP = DICT_MAP
        self.Player_Birthday = Player_Birthday
        self.Player_Height = Player_Height


        return  DICT_MAP, Player_Birthday, Player_Birthplace, Player_Position, Player_Height


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


    def Get_Draft_Year_Data__1(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__1NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__1NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 1):
                        try:
                            Draft_Year__1NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+1):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__1NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__2(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__2NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__2NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 2):
                        try:
                            Draft_Year__2NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+2):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__2NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__3(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__3NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__3NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 3):
                        try:
                            Draft_Year__3NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+3):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__3NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__4(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__4NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__4NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 4):
                        try:
                            Draft_Year__4NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+4):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__4NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__5(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__5NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__5NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 5):
                        try:
                            Draft_Year__5NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+5):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__5NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__6(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__6NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__6NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 6):
                        try:
                            Draft_Year__6NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+6):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__6NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__7(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__7NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__7NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):
                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 7):
                        try:
                            Draft_Year__7NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+7):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__7NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__8(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__8NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__8NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):
                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year + 8):
                        try:
                            Draft_Year__8NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+8):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__8NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__9(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__9NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__9NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):
                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year +9):
                        try:
                            Draft_Year__9NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+9):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__9NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data = Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_Data__10(self, Results, draft_year):

        DY_League = []
        DY_GP = 0
        DY_GP__ = []
        DY_G = 0
        DY_A =[]
        DY_P=[]
        DY_PIM = []
        counter=0
        Draft_Year_Data = []
        Draft_Year__10NHLGP = 0

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Draft_Year__10NHLGP = 0

            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == "" or Stats.loc[i,2] == '-' ):

                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year +10):
                        try:
                            Draft_Year__10NHLGP += int(Stats.loc[i,2])

                        except (TypeError, ValueError):
                            print("type error")

                if (int(year.partition("-")[2]) == draft_year+10):
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


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_League, DY_GP, DY_G, DY_A, DY_P, DY_PIM,Draft_Year__10NHLGP])
            Draft_Year_Data.append(HOLD)

            self.Draft_Year_Data =Draft_Year_Data

        return Draft_Year_Data

    def Get_Draft_Year_1_Data(self, Results, draft_year):

        DY_1_League = []
        DY_1_GP__ = []
        DY_1_GP = []
        DY_1_G=[]
        DY_1_A =[]
        DY_1_P=[]
        DY_1_PIM = []
        Draft_Year_1_Data = []
        hold = []
        holder= []
        counter=0
        for name, pos in zip(self.Player_Names,self.Player_Position):

            Stats = Results[name]
            max_holder=0
            max_holder2=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]
                if (year == "-" or year == '' or Stats.loc[i,2] == '-' ):
                    continue

                if (int(year.partition("-")[2]) == draft_year -1):
                    holder = Stats.loc[i,2]
                    DY_1_GP__ = Stats.loc[i,2]
                    if int(DY_1_GP__) > max_holder2:
                        counter2 = i
                        max_holder2 = int(DY_1_GP__)
                        DY_1_League = Stats.loc[counter2,1]
                        DY_1_GP = Stats.loc[counter2,2]
                        DY_1_G =  Stats.loc[counter2,3]
                        DY_1_A =  Stats.loc[counter2,4]
                        DY_1_P =  Stats.loc[counter2,5]
                        DY_1_PIM = Stats.loc[counter2,6]


                HOLD = np.zeros(7)
                HOLD =  np.array([DY_1_League, DY_1_GP, DY_1_G, DY_1_A, DY_1_P, DY_1_PIM])
            Draft_Year_1_Data.append(HOLD)

            self.Draft_Year_1_Data = Draft_Year_1_Data

        return Draft_Year_1_Data, self.Player_Position


    def NHL_WC_Variables(self, Results, draft_year):

        NHL_GP = 0
        NHL_G = 0
        NHL_A = 0
        NHL_P = 0
        WHC_17 = 0
        WHC_18 = 0
        DYWJC_20 = 0
        year = []
        Stats = []
        Training = []
        NHL_WC_Vars = []


        for name, pos in zip(self.Player_Names,self.Player_Position):
            NHL_GP = 0
            NHL_G = 0
            NHL_A = 0
            NHL_P = 0
            NCAA_GP=0

            Stats = Results[name]
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == ''):
                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year +3) | (int(year.partition("-")[2]) == draft_year +4) | (int(year.partition("-")[2]) == draft_year +5) | (int(year.partition("-")[2]) == draft_year +6) | (int(year.partition("-")[2]) == draft_year +7) | (int(year.partition("-")[2]) == draft_year +8) | (int(year.partition("-")[2]) == draft_year +9) | (int(year.partition("-")[2]) == draft_year +10):
                        try:
                            NHL_GP += int(Stats.loc[i,2])
                            NHL_G  +=  int(Stats.loc[i,3])
                            NHL_A  +=  int(Stats.loc[i,4])
                            NHL_P  +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")


            #if (Stats[1][i] == "NCAA"):
                #try:
                    #NCAA_GP += int(Stats.loc[i,2])
                #except (TypeError, ValueError):
                    #print("type error")

                if (Stats[1][i] == "WHC-17"):
                    WHC_17 =1

                if (Stats[1][i] == "WJC-18"):
                    WHC_18 = 1

                if (int(year.partition("-")[2]) == draft_year):
                    if (Stats[1][i] == "WJC-20"):
                        DYWJC_20 = 1

            HOLD = np.zeros(7)
            HOLD =  np.array([ WHC_17, WHC_18, DYWJC_20, NHL_GP, NHL_G, NHL_A, NHL_P])

            WHC_17=0
            WHC_18=0
            DYWJC_20 =0

            NHL_WC_Vars.append(HOLD)

        return NHL_WC_Vars

    def RunEverything(self):
        self.Results,self.Player_Birthday, self.Player_Birthplace, self.Player_Position, self.Player_Height =  self.Get_Player_Stats()
        #Test_Goalie = pd.DataFrame([self.Results.keys(), self.Player_Birthday, self.Player_Birthplace, self.Player_Position, self.Player_Height]).transpose()
        #Names = []
        #Index = []
        #for i in range(0,len(Test_Goalie)):
        #    if Test_Goalie[3][i] == 'G':
        #        Names.append(Test_Goalie[0][i])
        #        Index.append(i)
        #for k in Names:
        #    del self.Results[k]
        #n = 0
        #for l in Index:
        #    del self.Player_Names[l-n]
        #    del self.Player_Birthday[l-n]
        #    del self.Player_Birthplace[l-n]
        #    del self.Player_Position[l-n]
        #    del self.Player_Height[l-n]
        #    n += 1

        x,e = self.Get_Draft_Year_1_Data(self.Results,self.draft_year)
        y = self.Get_Draft_Year_Data(self.Results,self.draft_year)
        u = self.NHL_WC_Variables(self.Results, self.draft_year)
        a = self.Get_Draft_Year_Data__1(self.Results,self.draft_year)
        b = self.Get_Draft_Year_Data__2(self.Results,self.draft_year)
        c = self.Get_Draft_Year_Data__3(self.Results,self.draft_year)
        d = self.Get_Draft_Year_Data__4(self.Results,self.draft_year)
        f = self.Get_Draft_Year_Data__5(self.Results,self.draft_year)
        g = self.Get_Draft_Year_Data__6(self.Results,self.draft_year)
        h = self.Get_Draft_Year_Data__7(self.Results,self.draft_year)
        uu = self.Get_Draft_Year_Data__8(self.Results,self.draft_year)
        j = self.Get_Draft_Year_Data__9(self.Results,self.draft_year)
        k = self.Get_Draft_Year_Data__10(self.Results,self.draft_year)
        the= []
        for i in range(0,len(x)):
            ry = pd.DataFrame([self.Player_Names[i]])
            dz = pd.DataFrame([self.Player_Birthday[i]])
            gh = pd.DataFrame([self.Player_Height[i]])
            bnn = pd.DataFrame([self.Player_Birthplace[i]])
            x_ = pd.DataFrame([x[i]])
            y_ = pd.DataFrame([y[i]])
            a_ = pd.DataFrame([a[i]])
            b_ = pd.DataFrame([b[i]])
            c_ = pd.DataFrame([c[i]])
            d_ = pd.DataFrame([d[i]])
            f_ = pd.DataFrame([f[i]])
            g_ = pd.DataFrame([g[i]])
            h_ = pd.DataFrame([h[i]])
            uu_ = pd.DataFrame([uu[i]])
            j_ = pd.DataFrame([j[i]])
            k_ = pd.DataFrame([k[i]])
            u_ = pd.DataFrame([u[i]])
            e__ = pd.DataFrame([e[i]])
            ll = pd.concat([ry,dz,gh,bnn,e__,x_ ,y_,a_,b_,c_,d_,f_,g_,h_,uu_,j_,k_,u_] ,axis=1)
            the.append(ll)

        column = ['NAME', 'BIRTHDAY',"BIRTHPLACE","HEIGHT", 'POS',
                  'DY_1_League', 'DY_1_GP', 'DY_1_G','DY_1_A', 'DY_1_P', 'DY_1_PIM',
                  'DY_League', 'DY_GP', 'DY_G', 'DY_A', 'DY_P', 'DY_PIM',
                  'DY1_League', 'DY1_GP', 'DY1_G', 'DY1_A', 'DY1_P', 'DY1_PIM','Draft_Year__1NHLGP',
                  'DY2_League', 'DY2_GP', 'DY2_G', 'DY2_A', 'DY2_P', 'DY2_PIM','Draft_Year__2NHLGP',
                  'DY3_League', 'DY3_GP', 'DY3_G', 'DY3_A', 'DY3_P', 'DY3_PIM','Draft_Year__3NHLGP',
                  'DY4_League', 'DY4_GP', 'DY4_G', 'DY4_A', 'DY4_P', 'DY4_PIM','Draft_Year__4NHLGP',
                  'DY5_League', 'DY5_GP', 'DY5_G', 'DY5_A', 'DY5_P', 'DY5_PIM','Draft_Year__5NHLGP',
                  'DY6_League', 'DY6_GP', 'DY6_G', 'DY6_A', 'DY6_P', 'DY6_PIM','Draft_Year__6NHLGP',
                  'DY7_League', 'DY7_GP', 'DY7_G', 'DY7_A', 'DY7_P', 'DY7_PIM','Draft_Year__7NHLGP',
                  'DY8_League', 'DY8_GP', 'DY8_G', 'DY8_A', 'DY8_P', 'DY8_PIM','Draft_Year__8NHLGP',
                  'DY9_League', 'DY9_GP', 'DY9_G', 'DY9_A', 'DY9_P', 'DY9_PIM','Draft_Year__9NHLGP',
                  'DY10_League', 'DY10_GP', 'DY10_G', 'DY10_A', 'DY10_P', 'DY10_PIM','Draft_Year__10NHLGP',
                  'WHC_17', 'WHC_18', 'DYWJC_20', 'NHL_GP', 'NHL_G', 'NHL_A', 'NHL_P']
        df =pd.DataFrame(np.concatenate(the), columns = column)

        #k = []
        #for i in range(0,len(df)-1):
        #    if (df['DY_1_GP'][i] == df['DY_1_GP'][i+1]) and (df['DY_1_G'][i] == df['DY_1_G'][i+1]) and (df['DY_1_A'][i] == df['DY_1_A'][i+1]) and (df['DY_1_P'][i] == df['DY_1_P'][i+1]) and (df['DY_1_PIM'][i] == df['DY_1_PIM'][i+1]) and (df['DY_1_League'][i] == df['DY_1_League'][i+1]):
        #        print('the')
        #        k.append(i+1)
        #n = 0
        #for i in k:
        #    df = df.drop([i-n])
        #    n += 1

        return df
