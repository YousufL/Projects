from UFC import Get_All_Stats
from getstats import Get_AllUFC_Fighters


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


UFC_Names, Weight, Reach, Height, Stance, fighter_links = Get_AllUFC_Fighters()


DATA  = Get_All_Stats(fighter_links,UFC_Names,Weight,Reach,Stance,Height)

DATA.to_csv(r'C:\Users\Youfy\Desktop\Data.csv', index = False)
