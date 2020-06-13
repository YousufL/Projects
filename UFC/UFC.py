import json
import ssl
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.request import urlopen
from time import time
from datetime import datetime
import numpy as np
from tqdm import tqdm
import time
import re

def Get_All_Stats(fighter_links,UFC_Names,Weight,Reach,Stance,Height):


    FIGHTER_STATS = []

    for j in tqdm(range(0,len(fighter_links))):
        #time.sleep(2)
        print(UFC_Names[j])
        html = urlopen(fighter_links[j])
        soup = BeautifulSoup(html, 'html')

        div = soup.find_all('p', class_ = 'b-fight-details__table-text')
        div2 =  soup.find_all('a', class_ = 'b-link b-link_style_black')
        div3 = soup.find_all("li", class_='b-list__box-list-item b-list__box-list-item_type_block')
        div4 =  soup.find_all('i', class_ = 'b-flag__text')
        div5 = soup.find_all('p', class_ = 'b-fight-details__table-text')




        Name = []
        Weight_ = []
        Reach_ = []
        Stance_ = []
        Height_ = []


        fight_details = []
        Date = []
        Method = []
        Round = []
        Time = []
        Event = []
        Opponent = []
        Result = []
        Birth_Year = []

        KD_For = []
        KD_Against = []

        Sig_Str_For = []
        Sig_Str_Against = []
        Sig_Str_For_per = []
        Sig_Str_Against_per = []

        Total_Str_For = []
        Total_Str_Against = []

        TD_For = []
        TD_Against = []

        TD_For_per = []
        TD_Against_per = []

        Sub_Att_For = []
        Sub_Att_Against = []

        Pass_For = []
        Pass_Against = []

        Rev_For = []
        Rev_Against = []


        Head_For = []
        Head_Against = []

        Body_For = []
        Body_Against = []

        Leg_For = []
        Leg_Against = []

        Distance_For = []
        Distance_Against = []

        Clinch_For = []
        Clinch_Against = []

        Ground_For = []
        Ground_Against = []


        for i in range(0,len(div4)):
            Result.append(div4[i].text.strip())
        try:
            if Result[0] == 'next':
                Result=[]
                for i in range(1,len(div4)):
                    Result.append(div4[i].text.strip())
                for i in range(0,len(Result)):
                    Name.append(UFC_Names[j])
                    Weight_.append(Weight[j])
                    Stance_.append(Stance[j])
                    Reach_.append(Reach[j])
                    Height_.append(Height[j])

                for i in range(18,len(div),17):
                    Date.append(div[i].text.strip())

                for i in range(19,len(div),17):
                    Method.append(div[i].text.strip())

                for i in range(21,len(div),17):
                    Round.append(div[i].text.strip())

                for i in range(22,len(div),17):
                    Time.append(div[i].text.strip())

                for i in range(17,len(div),17):
                    Event.append(div[i].text.strip())

                for i in range(1,len(div2),3):
                    Opponent.append(div2[i].text.strip())

                for i in range(6,len(div5),17):
                    fight_details.append(div5[i].find('a',href=True).get('href'))

                for i in range(0,len(Opponent)):
                    try:
                        Birth_Year.append(div3[4].text.strip().split(' ')[22])
                    except IndexError:
                        Birth_Year.append('-')
            else:
                for i in range(0,len(Result)):
                    Name.append(UFC_Names[j])
                    Weight_.append(Weight[j])
                    Stance_.append(Stance[j])
                    Reach_.append(Reach[j])
                    Height_.append(Height[j])

                for i in range(12,len(div),17):
                    Date.append(div[i].text.strip())

                for i in range(13,len(div),17):
                    Method.append(div[i].text.strip())

                for i in range(15,len(div),17):
                    Round.append(div[i].text.strip())

                for i in range(16,len(div),17):
                    Time.append(div[i].text.strip())

                for i in range(11,len(div),17):
                    Event.append(div[i].text.strip())

                for i in range(1,len(div2),3):
                    Opponent.append(div2[i].text.strip())

                for i in range(0,len(Opponent)):
                    try:
                        Birth_Year.append(div3[4].text.strip().split(' ')[22])
                    except IndexError:
                        Birth_Year.append('-')

                for i in range(0,len(div5),17):
                    fight_details.append(div5[i].find('a',href=True).get('href'))
        except IndexError:
            print('tge')

        for i in range(0,len(fight_details)):
            #print(Round[i])
            #print(fight_details[i])
            html = urlopen(fight_details[i])
            soup = BeautifulSoup(html, 'html')
            x  =soup.find_all('p',class_='b-fight-details__table-text')

            #if x[0].text.strip() == UFC_Names[j]:

            try:
                if x[0].text.strip() == UFC_Names[j]:

                    KD_For.append(x[2].text.strip())
                    KD_Against.append(x[3].text.strip())
                    Sig_Str_For.append(x[4].text.strip())
                    Sig_Str_Against.append(x[5].text.strip())
                    Sig_Str_For_per.append(x[6].text.strip())
                    Sig_Str_Against_per.append(x[7].text.strip())

                    Total_Str_For.append(x[8].text.strip())
                    Total_Str_Against.append(x[9].text.strip())

                    TD_For.append(x[10].text.strip())
                    TD_Against.append(x[11].text.strip())

                    TD_For_per.append(x[12].text.strip())
                    TD_Against_per.append(x[13].text.strip())

                    Sub_Att_For.append(x[14].text.strip())
                    Sub_Att_Against.append(x[15].text.strip())

                    Pass_For.append(x[16].text.strip())
                    Pass_Against.append(x[17].text.strip())

                    Rev_For.append(x[18].text.strip())
                    Rev_Against.append(x[19].text.strip())

                    Head_For.append(x[20+20*int(Round[i])+6].text.strip())
                    Head_Against.append(x[20+20*int(Round[i])+7].text.strip())

                    Body_For.append(x[20+20*int(Round[i])+8].text.strip())
                    Body_Against.append(x[20+20*int(Round[i])+9].text.strip())

                    Leg_For.append(x[20+20*int(Round[i])+10].text.strip())
                    Leg_Against.append(x[20+20*int(Round[i])+11].text.strip())

                    Distance_For.append(x[20+20*int(Round[i])+12].text.strip())
                    Distance_Against.append(x[20+20*int(Round[i])+13].text.strip())
                    #print(20+20*int(Round[i])+15)
                    Clinch_For.append(x[20+20*int(Round[i])+14].text.strip())
                    Clinch_Against.append(x[20+20*int(Round[i])+15].text.strip())

                    Ground_For.append(x[20+20*int(Round[i])+16].text.strip())
                    Ground_Against.append(x[20+20*int(Round[i])+17].text.strip())

                else:
                    KD_For.append(x[3].text.strip())
                    KD_Against.append(x[2].text.strip())
                    Sig_Str_For.append(x[5].text.strip())
                    Sig_Str_Against.append(x[4].text.strip())
                    Sig_Str_For_per.append(x[7].text.strip())
                    Sig_Str_Against_per.append(x[6].text.strip())

                    Total_Str_For.append(x[9].text.strip())
                    Total_Str_Against.append(x[8].text.strip())

                    TD_For.append(x[11].text.strip())
                    TD_Against.append(x[10].text.strip())

                    TD_For_per.append(x[13].text.strip())
                    TD_Against_per.append(x[12].text.strip())

                    Sub_Att_For.append(x[15].text.strip())
                    Sub_Att_Against.append(x[14].text.strip())

                    Pass_For.append(x[17].text.strip())
                    Pass_Against.append(x[16].text.strip())

                    Rev_For.append(x[19].text.strip())
                    Rev_Against.append(x[18].text.strip())

                    Head_For.append(x[20+20*int(Round[i])+7].text.strip())
                    Head_Against.append(x[20+20*int(Round[i])+6].text.strip())

                    Body_For.append(x[20+20*int(Round[i])+9].text.strip())
                    Body_Against.append(x[20+20*int(Round[i])+8].text.strip())

                    Leg_For.append(x[20+20*int(Round[i])+11].text.strip())
                    Leg_Against.append(x[20+20*int(Round[i])+10].text.strip())

                    Distance_For.append(x[20+20*int(Round[i])+13].text.strip())
                    Distance_Against.append(x[20+20*int(Round[i])+12].text.strip())
                    #print(20+20*int(Round[i])+15)
                    Clinch_For.append(x[20+20*int(Round[i])+15].text.strip())
                    Clinch_Against.append(x[20+20*int(Round[i])+14].text.strip())

                    Ground_For.append(x[20+20*int(Round[i])+17].text.strip())
                    Ground_Against.append(x[20+20*int(Round[i])+16].text.strip())

            except IndexError:
                #print('no')
                KD_For.append("NA")
                KD_Against.append("NA")
                Sig_Str_For.append("NA")
                Sig_Str_Against.append("NA")
                Sig_Str_For_per.append("NA")
                Sig_Str_Against_per.append("NA")

                Total_Str_For.append("NA")
                Total_Str_Against.append("NA")

                TD_For.append("NA")
                TD_Against.append("NA")

                TD_For_per.append("NA")
                TD_Against_per.append("NA")

                Sub_Att_For.append("NA")
                Sub_Att_Against.append("NA")

                Pass_For.append("NA")
                Pass_Against.append("NA")

                Rev_For.append("NA")
                Rev_Against.append("NA")

                Head_For.append("NA")
                Head_Against.append("NA")

                Body_For.append("NA")
                Body_Against.append("NA")

                Leg_For.append("NA")
                Leg_Against.append("NA")

                Distance_For.append("NA")
                Distance_Against.append("NA")
                #print(20+20*int(Round[i])+15)
                Clinch_For.append("NA")
                Clinch_Against.append("NA")

                Ground_For.append("NA")
                Ground_Against.append("NA")


        Name = pd.DataFrame(Name)
        Weight_ = pd.DataFrame(Weight_)
        Reach_ = pd.DataFrame(Reach_)
        Stance_ = pd.DataFrame(Stance_)
        Height_ = pd.DataFrame(Height_)



        #print(Head_For)
        Result = pd.DataFrame(Result)
        Date = pd.DataFrame(Date)
        Method = pd.DataFrame(Method)
        Round = pd.DataFrame(Round)
        Time = pd.DataFrame(Time)
        Event = pd.DataFrame(Event)
        Opponent = pd.DataFrame(Opponent)
        Birth_Year = pd.DataFrame(Birth_Year)


        Sig_Str_For = pd.DataFrame(Sig_Str_For)
        Sig_Str_Against= pd.DataFrame(Sig_Str_Against)
        Sig_Str_For_per= pd.DataFrame(Sig_Str_For_per)
        Sig_Str_Against_per= pd.DataFrame(Sig_Str_Against_per)



        TD_For = pd.DataFrame(TD_For)
        TD_Against =pd.DataFrame(TD_Against)

        TD_For_per = pd.DataFrame(TD_For_per)
        TD_Against_per = pd.DataFrame(TD_Against_per)

        Sub_Att_For = pd.DataFrame(Sub_Att_For)
        Sub_Att_Against = pd.DataFrame(Sub_Att_Against)

        Pass_For = pd.DataFrame(Pass_For)
        Pass_Against = pd.DataFrame(Pass_Against)

        Rev_For = pd.DataFrame(Rev_For)
        Rev_Against = pd.DataFrame(Rev_Against)


        Head_For = pd.DataFrame(Head_For)
        Head_Against = pd.DataFrame(Head_Against)

        Body_For = pd.DataFrame(Body_For)
        Body_Against = pd.DataFrame(Body_Against)

        Leg_For = pd.DataFrame(Leg_For)
        Leg_Against = pd.DataFrame(Leg_Against)
        #print(Leg_Against)

        Distance_For = pd.DataFrame(Distance_For)
        Distance_Against = pd.DataFrame(Distance_Against)

        Clinch_For = pd.DataFrame(Clinch_For)
        Clinch_Against = pd.DataFrame(Clinch_Against)

        Ground_For = pd.DataFrame(Ground_For)
        Ground_Against = pd.DataFrame(Ground_Against)


        Static_Stats = pd.concat([Name, Weight_,Reach_,Stance_,Height_,Birth_Year,Date,Result,Method,Round,Time,Event,Opponent,Sig_Str_For,Sig_Str_For_per,TD_For,TD_For_per,Sub_Att_For,Pass_For,
                                Rev_For,Head_For,Body_For, Leg_For, Distance_For, Clinch_For, Ground_For,Sig_Str_Against,Sig_Str_Against_per,TD_Against, TD_Against_per,
                                Sub_Att_Against, Pass_Against, Rev_Against,Head_Against,Body_Against,Leg_Against,Distance_Against,Clinch_Against,Ground_Against],axis=1)

        try:
            Static_Stats.columns = ['Name', 'Weight_','Reach_','Stance_','Height_','Birth_Year','Date','Result','Method','Round','Time','Event','Opponent','Sig_Str_For','Sig_Str_For_per','TD_For','TD_For_per','Sub_Att_For','Pass_For',
                                'Rev_For','Head_For','Body_For', 'Leg_For', 'Distance_For', 'Clinch_For', 'Ground_For','Sig_Str_Against','Sig_Str_Against_per','TD_Against', 'TD_Against_per',
                                'Sub_Att_Against', 'Pass_Against', 'Rev_Against','Head_Against','Body_Against','Leg_Against','Distance_Against','Clinch_Against','Ground_Against']
        except ValueError:
            print('fw')


        FIGHTER_STATS.append(Static_Stats)
    df = pd.concat(FIGHTER_STATS)


    return df
