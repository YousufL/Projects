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

class EPScraperNHLDraftModel:

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
        hold2 = soup.find_all("td",class_="team")

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

        Player_Team = []
        for game in hold2:
            try:
                links_url = game.find('a', href=True)
                Player_Team.append(links_url.text)
            except:
                AttributeError

        Player_Names = Player_Names[5:self.draft_length+5]
        Player_URLs = Player_URLs[5:self.draft_length+5]


        self.Player_Names = Player_Names
        self.Player_URLs = Player_URLs
        self.Player_Team = Player_Team

        return Player_URLs, Player_Names, Player_Team

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

        self.Player_URLs, self.Player_Names, self.Player_Team = self.Collect_Player_URL_From_Draft()

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



            Test_Goalie = pd.DataFrame([Results.keys(), Player_Birthday, Player_Birthplace, Player_Position,
                  Player_Height]).transpose()
            Names = []
            Index = []

        for i in range(0,len(Test_Goalie)):
            if Test_Goalie[3][i] == 'G':
                Names.append(Test_Goalie[0][i])
                Index.append(i)

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

        #self.Results, self.Player_Birthday, self.Player_Birthplace, self.Player_Position, self.Player_Height = self.Get_Player_Stats()

        #self.Player_URLs, self.Player_Names = self.Collect_Player_URL_From_Draft()

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

    def Get_All_NHLYEARS(self,Results):
        NHL_ADJ_STATS = []

        for name, pos in zip(self.Player_Names,self.Player_Position):
            NHL_GP_95_96 = 0
            NHL_GP_96_97 = 0
            NHL_GP_97_98 = 0
            NHL_GP_98_99 = 0
            NHL_GP_99_00 = 0
            NHL_GP_00_01 = 0
            NHL_GP_01_02 = 0
            NHL_GP_02_03 = 0
            NHL_GP_03_04 = 0
            NHL_GP_04_05 = 0
            NHL_GP_05_06 = 0
            NHL_GP_06_07 = 0
            NHL_GP_07_08 = 0
            NHL_GP_08_09 = 0
            NHL_GP_09_10 = 0
            NHL_GP_10_11 = 0
            NHL_GP_11_12 = 0
            NHL_GP_12_13 = 0
            NHL_GP_13_14 = 0
            NHL_GP_14_15 = 0
            NHL_GP_15_16 = 0
            NHL_GP_16_17 = 0
            NHL_GP_17_18 = 0
            NHL_GP_18_19 = 0
            NHL_GP_19_20 = 0


            NHL_P_95_96 = 0
            NHL_P_96_97 = 0
            NHL_P_97_98 = 0
            NHL_P_98_99 = 0
            NHL_P_99_00 = 0
            NHL_P_00_01 = 0
            NHL_P_01_02 = 0
            NHL_P_02_03 = 0
            NHL_P_03_04 = 0
            NHL_P_04_05 = 0
            NHL_P_05_06 = 0
            NHL_P_06_07 = 0
            NHL_P_07_08 = 0
            NHL_P_08_09 = 0
            NHL_P_09_10 = 0
            NHL_P_10_11 = 0
            NHL_P_11_12 = 0
            NHL_P_12_13 = 0
            NHL_P_13_14 = 0
            NHL_P_14_15 = 0
            NHL_P_15_16 = 0
            NHL_P_16_17 = 0
            NHL_P_17_18 = 0
            NHL_P_18_19 = 0
            NHL_P_19_20 = 0

            Stats = Results[name]
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == ''):
                    continue

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 1996):
                        try:
                            NHL_GP_95_96  += int(Stats.loc[i,2])
                            NHL_P_95_96  +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 1997):
                        try:
                            NHL_GP_96_97  += int(Stats.loc[i,2])
                            NHL_P_96_97   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 1998):
                        try:
                            NHL_GP_97_98  += int(Stats.loc[i,2])
                            NHL_P_97_98   +=  int(Stats.loc[i,5])

                        except (TypeError, ValueError):
                            print("type error")


                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 1999):
                        try:
                            NHL_GP_98_99  += int(Stats.loc[i,2])
                            NHL_P_98_99   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2000):
                        try:
                            NHL_GP_99_00  += int(Stats.loc[i,2])
                            NHL_P_99_00   +=  int(Stats.loc[i,5])

                        except (TypeError, ValueError):
                            print("type error")


                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2001):
                        try:
                            NHL_GP_00_01  += int(Stats.loc[i,2])
                            NHL_P_00_01   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2002):
                        try:
                            NHL_GP_01_02  += int(Stats.loc[i,2])
                            NHL_P_01_02   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2003):
                        try:
                            NHL_GP_02_03  += int(Stats.loc[i,2])
                            NHL_P_02_03   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2004):
                        try:
                            NHL_GP_03_04  += int(Stats.loc[i,2])
                            NHL_P_03_04   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2005):
                        try:
                            NHL_GP_04_05  += int(Stats.loc[i,2])
                            NHL_P_04_05   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2006):
                        try:
                            NHL_GP_05_06  += int(Stats.loc[i,2])
                            NHL_P_05_06   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2007):
                        try:
                            NHL_GP_06_07  += int(Stats.loc[i,2])
                            NHL_P_06_07   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2008):
                        try:
                            NHL_GP_07_08  += int(Stats.loc[i,2])
                            NHL_P_07_08  +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2009):
                        try:
                            NHL_GP_08_09  += int(Stats.loc[i,2])
                            NHL_P_08_09   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2010):
                        try:
                            NHL_GP_09_10  += int(Stats.loc[i,2])
                            NHL_P_09_10   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2011):
                        try:
                            NHL_GP_10_11  += int(Stats.loc[i,2])
                            NHL_P_10_11   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")


                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2012):
                        try:
                            NHL_GP_11_12  += int(Stats.loc[i,2])
                            NHL_P_11_12   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")


                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2013):
                        try:
                            NHL_GP_12_13  += int(Stats.loc[i,2])
                            NHL_P_12_13   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2014):
                        try:
                            NHL_GP_13_14  += int(Stats.loc[i,2])
                            NHL_P_13_14   +=  int(Stats.loc[i,5])

                        except (TypeError, ValueError):
                            print("type error")


                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2015):
                        try:
                            NHL_GP_14_15 += int(Stats.loc[i,2])
                            NHL_P_14_15 +=  int(Stats.loc[i,5])

                        except (TypeError, ValueError):
                            print("type error")


                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2016):
                        try:
                            NHL_GP_15_16  += int(Stats.loc[i,2])
                            NHL_P_15_16  +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2017):
                        try:
                            NHL_GP_16_17  += int(Stats.loc[i,2])
                            NHL_P_16_17   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2018):
                        try:
                            NHL_GP_17_18  += int(Stats.loc[i,2])
                            NHL_P_17_18   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2019):
                        try:
                            NHL_GP_18_19  += int(Stats.loc[i,2])
                            NHL_P_18_19   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == 2020):
                        try:
                            NHL_GP_19_20  += int(Stats.loc[i,2])
                            NHL_P_19_20   +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")


            HOLD = np.zeros(50)
            HOLD =  np.array([NHL_GP_95_96,NHL_GP_96_97,NHL_GP_97_98,NHL_GP_98_99,NHL_GP_99_00,NHL_GP_00_01,
                        NHL_GP_01_02,NHL_GP_02_03,NHL_GP_03_04,NHL_GP_04_05,NHL_GP_05_06 ,NHL_GP_06_07,NHL_GP_07_08 ,
                        NHL_GP_08_09 ,NHL_GP_09_10 ,NHL_GP_10_11,NHL_GP_11_12,NHL_GP_12_13 ,NHL_GP_13_14 ,NHL_GP_14_15,
                        NHL_GP_15_16 ,NHL_GP_16_17 ,NHL_GP_17_18 ,NHL_GP_18_19,NHL_GP_19_20,NHL_P_95_96 ,NHL_P_96_97,
                        NHL_P_97_98 ,NHL_P_98_99,NHL_P_99_00 ,NHL_P_00_01 ,NHL_P_01_02 ,NHL_P_02_03 ,NHL_P_03_04 ,
                        NHL_P_04_05 ,NHL_P_05_06 ,NHL_P_06_07 ,NHL_P_07_08 ,NHL_P_08_09 ,NHL_P_09_10,NHL_P_10_11 ,
                        NHL_P_11_12,NHL_P_12_13 ,NHL_P_13_14,NHL_P_14_15,NHL_P_15_16,NHL_P_16_17,
                        NHL_P_17_18,NHL_P_18_19,NHL_P_19_20])

            NHL_ADJ_STATS.append(HOLD)



        return NHL_ADJ_STATS




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
            OHL_GP = 0
            OHL_G = 0
            OHL_A = 0
            OHL_P = 0
            WHL_GP = 0
            WHL_G = 0
            WHL_A = 0
            WHL_P = 0
            QMJHL_GP = 0
            QMJHL_G = 0
            QMJHL_A = 0
            QMJHL_P = 0
            NHL_GP = 0
            NHL_G = 0
            NHL_A = 0
            NHL_P = 0
            NHL_P_GP = 0
            NHL_P_G = 0
            NHL_P_A = 0
            NHL_P_P = 0
            NCAA_GP=0

            Stats = Results[name]
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]

                if (year == "-" or year == ''):
                    continue

                if (Stats[1][i] == "OHL"):
                    if (int(year.partition("-")[2]) == draft_year):
                        try:
                            OHL_GP += int(Stats.loc[i,2])
                            OHL_G  +=  int(Stats.loc[i,3])
                            OHL_A  +=  int(Stats.loc[i,4])
                            OHL_P  +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")

                if (Stats[1][i] == "QMJHL"):
                    if (int(year.partition("-")[2]) == draft_year):
                        try:
                            QMJHL_GP += int(Stats.loc[i,2])
                            QMJHL_G  +=  int(Stats.loc[i,3])
                            QMJHL_A  +=  int(Stats.loc[i,4])
                            QMJHL_P  +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")
                if (Stats[1][i] == "WHL"):
                    if (int(year.partition("-")[2]) == draft_year):
                        try:
                            WHL_GP += int(Stats.loc[i,2])
                            WHL_G  +=  int(Stats.loc[i,3])
                            WHL_A  +=  int(Stats.loc[i,4])
                            WHL_P  +=  int(Stats.loc[i,5])
                        except (TypeError, ValueError):
                            print("type error")


                if (Stats[1][i] == "NHL"):
                    try:
                        NHL_GP += int(Stats.loc[i,2])
                        NHL_G  +=  int(Stats.loc[i,3])
                        NHL_A  +=  int(Stats.loc[i,4])
                        NHL_P  +=  int(Stats.loc[i,5])
                    except (TypeError, ValueError):
                        print("type error")

                if (Stats[1][i] == "NHL"):
                    if (int(year.partition("-")[2]) == draft_year +3) | (int(year.partition("-")[2]) == draft_year +4) | (int(year.partition("-")[2]) == draft_year +5) | (int(year.partition("-")[2]) == draft_year +6) | (int(year.partition("-")[2]) == draft_year +7) | (int(year.partition("-")[2]) == draft_year +8) | (int(year.partition("-")[2]) == draft_year +9) | (int(year.partition("-")[2]) == draft_year +10):
                        try:
                            NHL_P_GP += int(Stats.loc[i,2])
                            NHL_P_G  +=  int(Stats.loc[i,3])
                            NHL_P_A  +=  int(Stats.loc[i,4])
                            NHL_P_P  +=  int(Stats.loc[i,5])
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

            HOLD = np.zeros(23)
            HOLD =  np.array([ WHC_17, WHC_18, DYWJC_20, NHL_GP, NHL_G, NHL_A, NHL_P,NHL_P_GP, NHL_P_G,NHL_P_A,NHL_P_P,
            OHL_GP,OHL_G,OHL_A,OHL_P,WHL_GP,WHL_G,WHL_A,WHL_P,QMJHL_GP,QMJHL_G,QMJHL_A,QMJHL_P])
            WHC_17=0
            WHC_18=0
            DYWJC_20 =0

            NHL_WC_Vars.append(HOLD)

        return NHL_WC_Vars


    def INV_Counter_1(self, Results, draft_year):
        Team_Goals = []
        counter=0
        Counter_1 = []

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]
                if (year == "-" or year == '' or Stats.loc[i,2] == ''):
                    continue

                if (int(year.partition("-")[2]) == (draft_year-1)):
                    try:
                        DY_GP__ = Stats.loc[i,2]
                        if int(DY_GP__) > max_holder:
                            counter = i
                            max_holder= int(DY_GP__)
                    except:
                        ValueError

            Counter_1.append(counter)

        return Counter_1


    def INV_Counter(self, Results, draft_year):
        Team_Goals = []
        counter=0
        Counter =[]

        for name, pos in zip(self.Player_Names,self.Player_Position):
            Stats = Results[name]
            max_holder=0
            for i, row in Stats[::-1].iterrows():
                year = Stats[0][i]
                if (year == "-" or year == '' or Stats.loc[i,2] == ''):
                    continue

                if (int(year.partition("-")[2]) == draft_year):
                    try:
                        DY_GP__ = Stats.loc[i,2]
                        if int(DY_GP__) > max_holder:
                            counter = i
                            max_holder= int(DY_GP__)
                    except:
                        ValueError

            Counter.append(counter)

        return Counter


    def Get_GINV(self, Results, counter):
        Team_G = []

        for name, count in tqdm(zip(self.Player_Names,counter)):
            try:

                Stats = Results[name]
                Team_Goals = Stats.iloc[count, 7]
                #print(Team_Goals)
                sleep(5)
                html = urlopen(Team_Goals)
                soup = BeautifulSoup(html,'html.parser')
                games = soup.find_all("table", class_ ="table table-striped table-sortable skater-stats highlight-stats")
                GOALS = []

            except:
                AttributeError, KeyError

            for result in games:
                GOALS.append(result.find_all("td" ,class_="g"))
                summ=0
                for j in range(1,len(GOALS[0])):
                    x = str(GOALS[0][j]).split(">")[0]
                    if x == '<td class="g"':
                        try:
                            r = str(GOALS[0][j]).split(">")[1]
                            z =int(str(r).split("<")[0].strip())
                            summ+= int(z)
                        except ValueError:
                            print('')
                #print(type(summ))
                #summ = int(summ)
                Team_G.append(summ)


        return Team_G

    def RunEverything(self):
        self.Results,self.Player_Birthday, self.Player_Birthplace, self.Player_Position, self.Player_Height = self.Get_Player_Stats()


        y = self.Get_Draft_Year_Data(self.Results,self.draft_year)
        x,e = self.Get_Draft_Year_1_Data(self.Results,self.draft_year)
        u = self.NHL_WC_Variables(self.Results, self.draft_year)
        bl = self.Get_All_NHLYEARS(self.Results)
        #lo = self.INV_Counter(self.Results,self.draft_year)
        #ly = self.INV_Counter_1(self.Results,self.draft_year)
        #r = self.Get_GINV(self.Results,lo)
        #z = self.Get_GINV(self.Results,ly)
        the= []

        for i in range(0,len(x)):
            ry = pd.DataFrame([self.Player_Names[i]])
            jkh = pd.DataFrame([self.Player_Team[i]])
            dz = pd.DataFrame([self.Player_Birthday[i]])
            gh = pd.DataFrame([self.Player_Height[i]])
            yy = pd.DataFrame([self.Player_Birthplace[i]])
            er = pd.DataFrame([bl[i]])
            #x_ = pd.DataFrame([x[i]])
            y_ = pd.DataFrame([y[i]])
            u_ = pd.DataFrame([u[i]])
            e__ = pd.DataFrame([e[i]])
            #r___ = pd.DataFrame([r[i]])
            #qq = pd.DataFrame([z[i]])
            ll = pd.concat([ry,jkh,dz,gh,yy,e__, y_,u_,er] ,axis=1)
            the.append(ll)

        column = ['NAME','Team', 'BIRTHDAY',"HEIGHT",'BIRTHPLACE', 'POS','DY_League', 'DY_GP', 'DY_G', 'DY_A', 'DY_P', 'DY_PIM',
         'WHC_17', 'WHC_18', 'DYWJC_20', 'NHL_GP', 'NHL_G', 'NHL_A', 'NHL_P','NHL_P_GP','NHL_P_G','NHL_P_A','NHL_P_P',
         'OHL_GP','OHL_G','OHL_A','OHL_P','WHL_GP','WHL_G','WHL_A','WHL_P','QMJHL_GP','QMJHL_G',
         'QMJHL_A','QMJHL_P','NHL_GP_95_96','NHL_GP_96_97','NHL_GP_97_98','NHL_GP_98_99','NHL_GP_99_00','NHL_GP_00_01',
                     'NHL_GP_01_02','NHL_GP_02_03','NHL_GP_03_04','NHL_GP_04_05','NHL_GP_05_06' ,'NHL_GP_06_07','NHL_GP_07_08' ,
                     'NHL_GP_08_09' ,'NHL_GP_09_10' ,'NHL_GP_10_11','NHL_GP_11_12','NHL_GP_12_13' ,'NHL_GP_13_14' ,'NHL_GP_14_15',
                     'NHL_GP_15_16' ,'NHL_GP_16_17' ,'NHL_GP_17_18' ,'NHL_GP_18_19','NHL_GP_19_20','NHL_P_95_96' ,'NHL_P_96_97',
                     'NHL_P_97_98' ,'NHL_P_98_99','NHL_P_99_00' ,'NHL_P_00_01' ,'NHL_P_01_02' ,'NHL_P_02_03' ,'NHL_P_03_04' ,
                     'NHL_P_04_05' ,'NHL_P_05_06' ,'NHL_P_06_07' ,'NHL_P_07_08' ,'NHL_P_08_09' ,'NHL_P_09_10','NHL_P_10_11' ,
                     'NHL_P_11_12','NHL_P_12_13','NHL_P_13_14','NHL_P_14_15','NHL_P_15_16','NHL_P_16_17',
                     'NHL_P_17_18','NHL_P_18_19','NHL_P_19_20']
        df =pd.DataFrame(np.concatenate(the), columns = column)

        return df
