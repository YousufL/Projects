from NHLDraftModel_DYDY1 import EPScraperNHLDraftModel
from OHLDraftModel import EPScraperOHLDraftModel
from NHLdraftmodelprime import EPScraperNHLDraftModelPrime
from tqdm import tqdm
import pandas as pd
Draft_L = [252,264,264,286,286,234,241,
            246,258,272,293,289,291,
            292,291,230,213,211,211,211,
            210,211,211,211,210,
            211,211,217,217,217]
DataFrame = []

for i in tqdm(range(17,30)):
    df = EPScraperNHLDraftModel(1990+i,"nhl-entry-draft",Draft_L[i]).RunEverything()
    DataFrame.append(df)

final_data = pd.concat(DataFrame)

final_data.to_csv(r'C:\Users\Youfy\Desktop\findfagain22.csv', index = False)
