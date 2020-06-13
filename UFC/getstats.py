
from tqdm import tqdm
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
def Get_AllUFC_Fighters():

    fighter_links = []
    Page_URL = []
    First_name = []
    Last_name = []
    First_Lower = []
    Last_Lower = []
    UFC_Names = []
    Reach = []
    Weight = []
    Stance = []
    Height = []
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    start = 'http://ufcstats.com/statistics/fighters?char='
    end = '&page=all'
    for i in range(0,len(alphabet)):
        Page_URL.append(start + alphabet[i] + end)

    for i in tqdm(range(0,len(Page_URL))):
        #time.sleep(1)
        html = urlopen(Page_URL[i])
        soup = BeautifulSoup(html,'html')
        div = soup.find_all("a", class_ = 'b-link b-link_style_black')
        div2 = soup.find_all("td", class_ = 'b-statistics__table-col')
        for i in range(0,len(div),3):
            First_name.append(div[i].text)
        for i in range(1,len(div),3):
            Last_name.append(div[i].text)
        for i in range(0,len(div),3):
            fighter_links.append(div[i].get('href'))

        for i in range(4,len(div2),11):
            Weight.append(div2[i].text.strip())
        for i in range(5,len(div2),11):
            Reach.append(div2[i].text.strip())
        for i in range(3,len(div2),11):
            Height.append(div2[i].text.strip())
        for i in range(6,len(div2),11):
            Stance.append(div2[i].text.strip())



    #for i in range(0,len(First_name)):
      #  First_Lower.append(First_name[i].lower())
        #Last_Lower.append(Last_name[i].lower())


    for i in range(0,len(Last_name)):
        UFC_Names.append(First_name[i] + ' ' + Last_name[i])

    return UFC_Names , Weight, Reach, Height, Stance, fighter_links
