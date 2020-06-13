

def Clean(df):
    #@title
    #Drop NA's
    df = df.dropna()

    #Remove Non-UFC Fights
    df = df[~df.Event.str.contains("EliteXC")]
    df = df[~df.Event.str.contains("Strikeforce")]
    df = df[~df.Event.str.contains("PRIDE")]
    df = df[~df.Event.str.contains("Bellator")]
    df = df[~df.Birth_Year.str.contains("-")]
    df = df[~df.Event.str.contains("DEEP")]
    df = df[~df.Event.str.contains("DREAM")]
    df = df[~df.Event.str.contains("Dynamite")]
    df = df[~df.Event.str.contains("Meca")]
    df = df[~df.Event.str.contains("MFA")]


    df = df[df.Round != 6]
    df = df[df.Time != '0']
    df = df[df.Time != '1']
    df = df[df.Time != '2']
    df = df[df.Time != '4']

    df = df[df.Method != 'CNC']
    df = df[df.Method != 'Overturned']
    df = df[df.Method != 'DQ']
    df = df[df.Method != 'Other']
    df = df[df.Method != '']

    df = df[df.Result != 'nc']
    df = df[df.Result != 'nan']
    df = df[df.Result != 'next']

    df['Result'][df.Result == 'loss'] = -1
    df['Result'][df.Result == 'win'] = 1
    df['Result'][df.Result == 'draw'] = 0

    df['Method'][df.Method == 'S-DEC'] = 'Decision'
    df['Method'][df.Method == 'U-DEC'] = 'Decision'
    df['Method'][df.Method == 'M-DEC'] = 'Decision'
    df['Method'][df.Method == 'Decision'] = 'Decision'


    #Reset Index
    df = df.reset_index()

    #Get total seconds in round of finish or decision
    total = []
    for i in range(0,len(df)):
        try:
            total.append(int(df['Time'][i].split(':')[0])*60 + int(df['Time'][i].split(':')[1]))
        except ValueError:
            total.append("NA")

    total=pd.DataFrame(total)
    total.columns = ['total']

    df = pd.concat([df,total],axis=1)

    #Get Total seconds of Fight
    total_seconds = []
    for i in range(0,len(df)):
        if int(df['Round'][i]) == 1:
            try:
                total_seconds.append(df['total'][i])
            except TypeError:
                print('the')

        if int(df['Round'][i]) == 2:
            try:
                total_seconds.append(df['total'][i]+300)
            except TypeError:
                print('the')

        if int(df['Round'][i]) == 3:
            try:
                total_seconds.append(df['total'][i]+600)
            except TypeError:
                print('the')

        if int(df['Round'][i]) == 4:
            try:
                total_seconds.append(df['total'][i]+900)
            except TypeError:
                print('the')

        if int(df['Round'][i]) == 5:
            try:
                total_seconds.append(df['total'][i] + 1200)
            except TypeError:
                print('the')

    #Append seconds to dataframe
    total_seconds=pd.DataFrame(total_seconds)
    total_seconds.columns = ['total_seconds']
    df = pd.concat([df,total_seconds],axis=1)

    #Sort by Date
    df['Date'] = pd.to_datetime(df.Date)
    df = df.sort_values(['Name','Date'], ascending=[False,True])

    #Get Minutes
    df['Minutes'] = df['total_seconds']/60

    #Get Proper Stats
    df['SSL'] = df['Sig_Str_For'].map(lambda x: int(x.split(" ")[0]))
    df['TDL']  = df['TD_For'].map(lambda x: int(x.split(" ")[0]))
    df['HSL']  = df['Head_For'].map(lambda x: int(x.split(" ")[0]))
    df['BSL']  = df['Body_For'].map(lambda x: int(x.split(" ")[0]))
    df['LSL']  = df['Leg_For'].map(lambda x: int(x.split(" ")[0]))
    df['DSL']  = df['Distance_For'].map(lambda x: int(x.split(" ")[0]))
    df['CSL']  = df['Clinch_For'].map(lambda x: int(x.split(" ")[0]))
    df['GSL']  = df['Ground_For'].map(lambda x: int(x.split(" ")[0]))
    df['SS_Att'] = df['Sig_Str_For'].map(lambda x: int(x.split(" ")[2]))
    df['TD_Att']  = df['TD_For'].map(lambda x: int(x.split(" ")[2]))
    df['HS_Att']  = df['Head_For'].map(lambda x: int(x.split(" ")[2]))
    df['BS_Att']  = df['Body_For'].map(lambda x: int(x.split(" ")[2]))
    df['LS_Att']  = df['Leg_For'].map(lambda x: int(x.split(" ")[2]))
    df['DS_Att']  = df['Distance_For'].map(lambda x: int(x.split(" ")[2]))
    df['CS_Att']  = df['Clinch_For'].map(lambda x: int(x.split(" ")[2]))
    df['GS_Att']  = df['Ground_For'].map(lambda x: int(x.split(" ")[2]))
    df['SSL_Against'] = df['Sig_Str_Against'].map(lambda x: int(x.split(" ")[0]))
    df['TDL_Against']  = df['TD_Against'].map(lambda x: int(x.split(" ")[0]))
    df['HSL_Against']  = df['Head_Against'].map(lambda x: int(x.split(" ")[0]))
    df['BSL_Against']  = df['Body_Against'].map(lambda x: int(x.split(" ")[0]))
    df['LSL_Against']  = df['Leg_Against'].map(lambda x: int(x.split(" ")[0]))
    df['DSL_Against']  = df['Distance_Against'].map(lambda x: int(x.split(" ")[0]))
    df['CSL_Against']  = df['Clinch_Against'].map(lambda x: int(x.split(" ")[0]))
    df['GSL_Against']  = df['Ground_Against'].map(lambda x: int(x.split(" ")[0]))
    df['SSL_Att_Against'] = df['Sig_Str_Against'].map(lambda x: int(x.split(" ")[2]))
    df['TDL_Att_Against']  = df['TD_Against'].map(lambda x: int(x.split(" ")[2]))
    df['HSL_Att_Against']  = df['Head_Against'].map(lambda x: int(x.split(" ")[2]))
    df['BSL_Att_Against']  = df['Body_Against'].map(lambda x: int(x.split(" ")[2]))
    df['LSL_Att_Against']  = df['Leg_Against'].map(lambda x: int(x.split(" ")[2]))
    df['DSL_Att_Against']  = df['Distance_Against'].map(lambda x: int(x.split(" ")[2]))
    df['CSL_Att_Against']  = df['Clinch_Against'].map(lambda x: int(x.split(" ")[2]))
    df['GSL_AttAgainst']  = df['Ground_Against'].map(lambda x: int(x.split(" ")[2]))

    #Drop unwanted columns
    df = df.drop(columns = ['Sig_Str_For','TD_For','Head_For','Body_For','Leg_For','Distance_For','Clinch_For',
                                'Ground_For','Sig_Str_Against','TD_Against','Head_Against','Body_Against','Leg_Against',
                            'Distance_Against','Clinch_Against','Ground_Against','Sig_Str_For_per','TD_For_per','Sig_Str_Against_per','TD_Against_per'])

    #Calculate Rate Stats
    df['SSL'] = df['SSL']/df['Minutes']
    df['TDL']  = df['TDL']/df['Minutes']
    df['HSL']  = df['HSL']/df['Minutes']
    df['BSL']  =df['BSL'] /df['Minutes']
    df['LSL']  = df['LSL'] /df['Minutes']
    df['DSL']  = df['DSL'] /df['Minutes']
    df['CSL']  = df['CSL'] /df['Minutes']
    df['GSL']  = df['GSL'] /df['Minutes']
    df['SS_Att'] = df['SS_Att'] /df['Minutes']
    df['TD_Att']  = df['TD_Att'] /df['Minutes']
    df['HS_Att']  = df['HS_Att'] /df['Minutes']
    df['BS_Att']  = df['BS_Att'] /df['Minutes']
    df['LS_Att']  = df['LS_Att']  /df['Minutes']
    df['DS_Att']  = df['DS_Att'] /df['Minutes']
    df['CS_Att']  = df['CS_Att']/df['Minutes']
    df['GS_Att']  = df['GS_Att']  /df['Minutes']
    df['SSL_Against'] = df['SSL_Against']/df['Minutes']
    df['TDL_Against']  = df['TDL_Against'] /df['Minutes']
    df['HSL_Against']  = df['HSL_Against']  /df['Minutes']
    df['BSL_Against']  = df['BSL_Against'] /df['Minutes']
    df['LSL_Against']  = df['LSL_Against']/df['Minutes']
    df['DSL_Against']  = df['DSL_Against'] /df['Minutes']
    df['CSL_Against']  = df['CSL_Against'] /df['Minutes']
    df['GSL_Against']  = df['GSL_Against'] /df['Minutes']
    df['SSL_Att_Against'] = df['SSL_Att_Against']/df['Minutes']
    df['TDL_Att_Against']  = df['TDL_Att_Against'] /df['Minutes']
    df['HSL_Att_Against']  = df['HSL_Att_Against']/df['Minutes']
    df['BSL_Att_Against']  = df['BSL_Att_Against'] /df['Minutes']
    df['LSL_Att_Against']  = df['LSL_Att_Against'] /df['Minutes']
    df['DSL_Att_Against']  = df['DSL_Att_Against']  /df['Minutes']
    df['CSL_Att_Against']  = df['CSL_Att_Against']/df['Minutes']
    df['GSL_AttAgainst']  = df['GSL_AttAgainst'] /df['Minutes']

    #Get accuracies
    df['Sig_Str_Acc'] = df['SSL']/df['SS_Att']
    df['Sig_Str_Acc'].fillna(0, inplace=True)
    df['Sig_Str_Defense'] = df['SSL_Against']/df['SSL_Att_Against']
    df['Sig_Str_Defense'].fillna(0, inplace=True)
    df['Head_Str_Acc'] = df['HSL']/df['HS_Att']
    df['Head_Str_Acc'].fillna(0, inplace=True)
    df['Head_Str_Def'] = df['HSL_Against']/df['HSL_Att_Against']
    df['Head_Str_Def'].fillna(0, inplace=True)
    df['Clinch_Str_Acc'] = df['CSL']/df['CS_Att']
    df['Clinch_Str_Acc'].fillna(0, inplace=True)
    df['Clinch_Str_Def'] = df['CSL_Against']/df['CSL_Att_Against']
    df['Clinch_Str_Def'].fillna(0, inplace=True)
    df['Body_Str_Acc'] = df['BSL']/df['BS_Att']
    df['Body_Str_Acc'].fillna(0, inplace=True)
    df['Body_Str_Def'] = df['BSL_Against']/df['BSL_Att_Against']
    df['Body_Str_Def'].fillna(0, inplace=True)
    df['Leg_Str_Acc'] = df['LSL']/df['LS_Att']
    df['Leg_Str_Acc'].fillna(0, inplace=True)
    df['Leg_Str_Def'] = df['LSL_Against']/df['LSL_Att_Against']
    df['Leg_Str_Def'].fillna(0, inplace=True)
    df['Ground_Str_Acc'] = df['GSL']/df['GS_Att']
    df['Ground_Str_Acc'].fillna(0, inplace=True)
    df['Ground_Str_Def'] = df['GSL_Against']/df['GSL_AttAgainst']
    df['Ground_Str_Def'].fillna(0, inplace=True)
    df['DS_Acc'] = df['DSL']/df['DS_Att']
    df['DS_Acc'].fillna(0, inplace=True)
    df['DS_Def'] = df['DSL_Against']/df['DSL_Att_Against']
    df['DS_Def'].fillna(0, inplace=True)
    df['TD_Acc'] = df['TDL']/df['TD_Att']
    df["TD_Acc"].fillna(0, inplace=True)
    df['TD_Def'] = df['TDL_Against']/df['TDL_Att_Against']
    df["TD_Def"].fillna(0, inplace=True)

    df['Fight_Year'] =  df['Date'].map(lambda x: str(x).split('-')[0])
    df['Age_Fight'] = df['Fight_Year'].astype(int) - df['Birth_Year'].astype(int)

    df['Win_Count'] = np.where(( df['Result']==1),1,0)
    df['Loss_Count'] = np.where(( df['Result']==-1),1,0)

    #Win counts by win type
    df['Win_Decision_Count'] = np.where( (df['Result']== 1) & (df['Method'] == "Decision") , 1, 0)
    df['Win_KO_Count'] = np.where( (df['Result']== 1) & (df['Method'] == "KO/TKO") , 1, 0)
    df['Win_Sub_Count'] = np.where( (df['Result']== 1) & (df['Method'] == "SUB") , 1, 0)


    #loss counts by loss type
    df['Loss_Decision_Count'] = np.where( (df['Result']== -1) & (df['Method'] == "Decision") , 1, 0)
    df['Loss_KO_Count'] = np.where( (df['Result']== -1) & (df['Method'] == "KO/TKO") , 1, 0)
    df['Loss_Sub_Count'] = np.where( (df['Result']== -1) & (df['Method'] == "SUB") , 1, 0)

    #COunt win finishes and losses
    df['Finish_Win_Count'] = np.where( (df['Win_KO_Count']== 1) & (df['Win_Sub_Count'] == 1) , 1, 0)
    df['Finish_Loss_Count'] = np.where( (df['Loss_KO_Count']== 1) & (df['Loss_Sub_Count'] == 1) , 1, 0)

    #Sort by date to correctly count
    df = df.sort_values(by='Date', ascending=True)

    #Total wins/losses
    df['Total_Wins'] = df.groupby('Name')['Win_Count'].transform(lambda x: x.expanding().sum().shift(1))
    df['Total_Losses'] = df.groupby('Name')['Loss_Count'].transform(lambda x: x.expanding().sum().shift(1))

    #KO wins/KO losses
    df['KO_Wins'] = df.groupby('Name')['Win_KO_Count'].transform(lambda x: x.expanding().sum().shift(1))
    df['KO_Losses'] = df.groupby('Name')['Loss_KO_Count'].transform(lambda x: x.expanding().sum().shift(1))

    #Sub wins/losses
    df['Sub_Wins'] = df.groupby('Name')['Win_Sub_Count'].transform(lambda x: x.expanding().sum().shift(1))
    df['Sub_Losses'] = df.groupby('Name')['Loss_Sub_Count'].transform(lambda x: x.expanding().sum().shift(1))

    #Decision wins/losses
    df['Decision_Wins'] = df.groupby('Name')['Win_Decision_Count'].transform(lambda x: x.expanding().sum().shift(1))
    df['Decision_Losses'] = df.groupby('Name')['Loss_Decision_Count'].transform(lambda x: x.expanding().sum().shift(1))

    #Calculate percentages
    df['Total_Fights'] = df['Total_Wins'] + df['Total_Losses']
    df["Win%"] = df['Total_Wins']/(df['Total_Wins'] + df['Total_Losses'])
    df['Win%'].fillna(0, inplace=True)

    df["KO Win %"] = df['KO_Wins']/df['Total_Wins']
    df['KO Win %'].fillna(0, inplace=True)

    df["KO Loss %"]= df['KO_Losses']/df['Total_Losses']
    df["KO Loss %"].fillna(0, inplace=True)

    df["Sub Win %"]= df['Sub_Wins']/df['Total_Wins']
    df["Sub Win %"].fillna(0, inplace=True)

    df["Sub Loss %"]= df['Sub_Losses']/df['Total_Losses']
    df["Sub Loss %"].fillna(0, inplace=True)

    df["Decision Win %"]= df['Decision_Wins']/df['Total_Wins']
    df["Decision Win %"].fillna(0, inplace=True)

    df["Decision Loss %"]= df['Decision_Losses']/df['Total_Losses']
    df["Decision Loss %"].fillna(0, inplace=True)

    df['Win_Streak'] = df.groupby('Name')['Win_Count'].apply(lambda x: x * (x.groupby((x != x.shift()).cumsum()).cumcount()+ 1)).shift(1)
    df['Loss_Streak'] = df.groupby('Name')['Loss_Count'].apply(lambda x: x * (x.groupby((x != x.shift()).cumsum()).cumcount()+ 1)).shift(1)

    df['hold_opp']  = df['Opponent'] + df['Date'].astype(str)
    df['hold_Name'] =  df['Name'] + df['Date'].astype(str)

    y=2
    df = df.sort_values(['Name','Date'], ascending=[True,True])
    df['Sig_Str_Acc_Moving']  = df.groupby('Name')['Sig_Str_Acc'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Sig_Str_Def_Moving']  = df.groupby('Name')['Sig_Str_Defense'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Head_Str_Acc_Moving']  = df.groupby('Name')['Head_Str_Acc'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Head_Str_Def_Moving']  = df.groupby('Name')['Head_Str_Def'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Clinch_Str_Acc_Moving']  = df.groupby('Name')['Clinch_Str_Acc'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Clinch_Str_Def_Moving']  = df.groupby('Name')['Clinch_Str_Def'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Body_Str_Acc_Moving']  = df.groupby('Name')['Body_Str_Acc'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Body_Str_Def_Moving']  = df.groupby('Name')['Body_Str_Def'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Leg_Str_Acc_Moving']  = df.groupby('Name')['Leg_Str_Acc'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Leg_Str_Def_Moving']  = df.groupby('Name')['Leg_Str_Def'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Ground_Str_Acc_Moving']  = df.groupby('Name')['Ground_Str_Acc'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Ground_Str_Def_Moving']  = df.groupby('Name')['Ground_Str_Def'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['DS_Str_Acc_Moving']  = df.groupby('Name')['DS_Acc'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['DS_Str_Def_Moving']  = df.groupby('Name')['DS_Def'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['SSL_Moving']  = df.groupby('Name')['SSL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['TDL_Moving'] = df.groupby('Name')['TDL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['HSL_Moving'] = df.groupby('Name')['HSL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['BSL_Moving'] = df.groupby('Name')['BSL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['LSL_Moving'] = df.groupby('Name')['LSL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['DSL_Moving'] = df.groupby('Name')['DSL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['CSL_Moving'] = df.groupby('Name')['CSL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['GSL_Moving'] = df.groupby('Name')['GSL'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['SSL_Against_Moving']  = df.groupby('Name')['SSL_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['TDL_Against_Moving'] = df.groupby('Name')['TDL_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['HSL_Against_Moving'] = df.groupby('Name')['HSL_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['BSL_Against_Moving'] = df.groupby('Name')['BSL_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['LSL_Against_Moving'] = df.groupby('Name')['LSL_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['DSL_Against_Moving'] = df.groupby('Name')['DSL_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['CSL_Against_Moving'] = df.groupby('Name')['CSL_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Minutes_Moving'] = df.groupby('Name')['Minutes'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Sub_Att_For_Moving'] = df.groupby('Name')['Sub_Att_For'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Pass_For_Moving'] = df.groupby('Name')['Pass_For'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Rev_For_Moving'] = df.groupby('Name')['Rev_For'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Sub_Att_Against_Moving'] = df.groupby('Name')['Sub_Att_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Pass_Against_Moving'] = df.groupby('Name')['Pass_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))
    df['Rev_Against_Moving'] = df.groupby('Name')['Rev_Against'].transform(lambda x: x.rolling(y, 1).mean().shift(1))


    return df






def MakeStats(df):
    Name_2 = []

    Total_Wins_2 = []
    Total_Losses_2= []
    Total_KO_2= []
    Total_KO_Losses_2= []
    Total_SUB_2= []
    Total_SUB_Losses_2= []
    Total_Fights_2= []
    Win_perc_2= []
    KO_Win_perc_2= []
    KO_Loss_perc_2= []
    Sub_Win_perc_2= []
    Sub_loss_perc_2= []
    Decision_Win_perc_2 = []
    Decision_Loss_perc_2 = []
    Win_Streak_2= []
    Loss_Streak_2= []

    Age_2 = []
    SSA_2 = []
    SSD_2 = []
    HSA_2 = []
    HSD_2 = []
    CSA_2 = []
    CSD_2 = []
    BSA_2 = []
    BSD_2 = []
    LSA_2 = []
    LSD_2 = []
    GSA_2 = []
    GSD_2 = []
    DSA_2 = []
    DSD_2 = []
    SSL_2 = []
    TDL_2 = []
    HSL_2 = []
    BSL_2 = []
    LSL_2 = []
    DSL_2 = []
    CSL_2 = []
    GSL_2 = []
    SSLA_2 = []
    TDLA_2 = []
    HSLA_2 = []
    BSLA_2 = []
    LSLA_2 = []
    DSLA_2 = []
    CSLA_2 = []
    MM_2 = []
    SUB_2 = []
    PASS_2 = []
    REV_2 = []
    SUBA_2 = []
    PASSA_2 = []
    REVA_2 = []




    for i in tqdm(range(1,len(df))):
        for j in range(1,len(df)):
            if (sorted(df['hold_opp'][i]) == sorted(df['hold_Name'][j])):
                print(df['Name'][j])

                Date.append(df['Date'][i])
                Event.append(df['Event'][i])
                Result_1.append(df['Result'][i])
                Result_2.append(df['Result'][i])


                Name_1.append(df['Name'][i])


                Total_Wins_1.append(df['Total_Wins'][i])
                Total_Losses_1.append(df['Total_Losses'][i])
                Total_KO_1.append(df['KO_Wins'][i])
                Total_KO_Losses_1.append(df['KO_Losses'][i])
                Total_SUB_1.append(df['Sub_Wins'][i])
                Total_SUB_Losses_1.append(df['Sub_Losses'][i])
                Total_Fights_1.append(df['Total_Fights'][i])
                Win_perc_1.append(df['Win%'][i])
                KO_Win_perc_1.append(df['KO Win %'][i])
                KO_Loss_perc_1.append(df['KO Loss %'][i])
                Sub_Win_perc_1.append(df['Sub Win %'][i])
                Sub_loss_perc_1.append(df['Sub Loss %'][i])
                Decision_Win_perc_1.append(df['Decision Win %'][i])
                Decision_Loss_perc_1.append(df['Decision Loss %'][i])
                Win_Streak_1.append(df['Win_Streak'][i])
                Loss_Streak_1.append(df['Loss_Streak'][i])


                Age_1.append(df['Age_Fight'][i])
                SSA_1.append(df['Sig_Str_Acc_Moving'][i])
                SSD_1.append(df['Sig_Str_Def_Moving'][i])
                HSA_1.append(df['Head_Str_Acc_Moving'][i])
                HSD_1.append(df['Head_Str_Def_Moving'][i])
                CSA_1.append(df['Clinch_Str_Acc_Moving'][i])
                CSD_1.append(df['Clinch_Str_Def_Moving'][i])
                BSA_1.append(df['Body_Str_Acc_Moving'][i])
                BSD_1.append(df['Body_Str_Def_Moving'][i])
                LSA_1.append(df['Leg_Str_Acc_Moving'][i])
                LSD_1.append(df['Leg_Str_Def_Moving'][i])
                GSA_1.append(df['Ground_Str_Acc_Moving'][i])
                GSD_1.append(df['Ground_Str_Def_Moving'][i])
                DSA_1.append(df['DS_Str_Acc_Moving'][i])
                DSD_1.append(df['DS_Str_Def_Moving'][i])
                SSL_1.append(df['SSL_Moving'][i])
                TDL_1.append(df['TDL_Moving'][i])
                HSL_1.append(df['HSL_Moving'][i])
                BSL_1.append(df['BSL_Moving'][i])
                LSL_1.append(df['LSL_Moving'][i])
                DSL_1.append(df['DSL_Moving'][i])
                CSL_1.append(df['CSL_Moving'][i])
                GSL_1.append(df['GSL_Moving'][i])
                SSLA_1.append(df['SSL_Against_Moving'][i])
                TDLA_1.append(df['TDL_Against_Moving'][i])
                HSLA_1.append(df['HSL_Against_Moving'][i])
                BSLA_1.append(df['BSL_Against_Moving'][i])
                LSLA_1.append(df['LSL_Against_Moving'][i])
                DSLA_1.append(df['DSL_Against_Moving'][i])
                CSLA_1.append(df['CSL_Against_Moving'][i])
                MM_1.append(df['Minutes_Moving'][i])
                SUB_1.append(df['Sub_Att_For_Moving'][i])
                PASS_1.append(df['Pass_For_Moving'][i])
                REV_1.append(df['Rev_For_Moving'][i])
                SUBA_1.append(df['Sub_Att_Against_Moving'][i])
                PASSA_1.append(df['Pass_Against_Moving'][i])
                REVA_1.append(df['Rev_Against_Moving'][i])



                Name_2.append(df['Name'][j])

                Total_Wins_2.append(df['Total_Wins'][j])
                Total_Losses_2.append(df['Total_Losses'][j])
                Total_KO_2.append(df['KO_Wins'][j])
                Total_KO_Losses_2.append(df['KO_Losses'][j])
                Total_SUB_2.append(df['Sub_Wins'][j])
                Total_SUB_Losses_2.append(df['Sub_Losses'][j])
                Total_Fights_2.append(df['Total_Fights'][j])
                Win_perc_2.append(df['Win%'][j])
                KO_Win_perc_2.append(df['KO Win %'][j])
                KO_Loss_perc_2.append(df['KO Loss %'][j])
                Sub_Win_perc_2.append(df['Sub Win %'][j])
                Sub_loss_perc_2.append(df['Sub Loss %'][j])
                Decision_Win_perc_2.append(df['Decision Win %'][j])
                Decision_Loss_perc_2.append(df['Decision Loss %'][j])
                Win_Streak_2.append(df['Win_Streak'][j])
                Loss_Streak_2.append(df['Loss_Streak'][j])

                Age_2.append(df['Age_Fight'][j])
                SSA_2.append(df['Sig_Str_Acc_Moving'][j])
                SSD_2.append(df['Sig_Str_Def_Moving'][j])
                HSA_2.append(df['Head_Str_Acc_Moving'][j])
                HSD_2.append(df['Head_Str_Def_Moving'][j])
                CSA_2.append(df['Clinch_Str_Acc_Moving'][j])
                CSD_2.append(df['Clinch_Str_Def_Moving'][j])
                BSA_2.append(df['Body_Str_Acc_Moving'][j])
                BSD_2.append(df['Body_Str_Def_Moving'][j])
                LSA_2.append(df['Leg_Str_Acc_Moving'][j])
                LSD_2.append(df['Leg_Str_Def_Moving'][j])
                GSA_2.append(df['Ground_Str_Acc_Moving'][j])
                GSD_2.append(df['Ground_Str_Def_Moving'][j])
                DSA_2.append(df['DS_Str_Acc_Moving'][j])
                DSD_2.append(df['DS_Str_Def_Moving'][j])
                SSL_2.append(df['SSL_Moving'][j])
                TDL_2.append(df['TDL_Moving'][j])
                HSL_2.append(df['HSL_Moving'][j])
                BSL_2.append(df['BSL_Moving'][j])
                LSL_2.append(df['LSL_Moving'][j])
                DSL_2.append(df['DSL_Moving'][j])
                CSL_2.append(df['CSL_Moving'][j])
                GSL_2.append(df['GSL_Moving'][j])
                SSLA_2.append(df['SSL_Against_Moving'][j])
                TDLA_2.append(df['TDL_Against_Moving'][j])
                HSLA_2.append(df['HSL_Against_Moving'][j])
                BSLA_2.append(df['BSL_Against_Moving'][j])
                LSLA_2.append(df['LSL_Against_Moving'][j])
                DSLA_2.append(df['DSL_Against_Moving'][j])
                CSLA_2.append(df['CSL_Against_Moving'][j])
                MM_2.append(df['Minutes_Moving'][j])
                SUB_2.append(df['Sub_Att_For_Moving'][j])
                PASS_2.append(df['Pass_For_Moving'][j])
                REV_2.append(df['Rev_For_Moving'][j])
                SUBA_2.append(df['Sub_Att_Against_Moving'][j])
                PASSA_2.append(df['Pass_Against_Moving'][j])
                REVA_2.append(df['Rev_Against_Moving'][j])


    Date = pd.DataFrame(Date)
    Event =pd.DataFrame(Event)
    Result_1 = pd.DataFrame(Result_1)
    Result_2 = pd.DataFrame(Result_2)

    Name_1 = pd.DataFrame(Name_1)

    Total_Wins_1 = pd.DataFrame(Total_Wins_1)
    Total_Losses_1=pd.DataFrame(Total_Losses_1)
    Total_KO_1= pd.DataFrame(Total_KO_1)
    Total_KO_Losses_1= pd.DataFrame(Total_KO_Losses_1)
    Total_SUB_1= pd.DataFrame(Total_SUB_1)
    Total_SUB_Losses_1= pd.DataFrame(Total_SUB_Losses_1)
    Total_Fights_1= pd.DataFrame(Total_Fights_1)
    Win_perc_1= pd.DataFrame(Win_perc_1)
    KO_Win_perc_1= pd.DataFrame(KO_Win_perc_1)
    KO_Loss_perc_1= pd.DataFrame(KO_Loss_perc_1)
    Sub_Win_perc_1= pd.DataFrame(Sub_Win_perc_1)
    Sub_loss_perc_1= pd.DataFrame(Sub_loss_perc_1)
    Decision_Win_perc_1 = pd.DataFrame(Decision_Win_perc_1)
    Decision_Loss_perc_1 = pd.DataFrame(Decision_Loss_perc_1)
    Win_Streak_1= pd.DataFrame(Win_Streak_1)
    Loss_Streak_1= pd.DataFrame(Loss_Streak_1)

    Age_1 =  pd.DataFrame(Age_1)
    SSA_1 =  pd.DataFrame(SSA_1)
    SSD_1 =  pd.DataFrame(SSD_1)
    HSA_1 =  pd.DataFrame(HSA_1)
    HSD_1 =  pd.DataFrame(HSD_1)
    CSA_1 =  pd.DataFrame(CSA_1)
    CSD_1 =  pd.DataFrame(CSD_1)
    BSA_1 =  pd.DataFrame(BSA_1)
    BSD_1 =  pd.DataFrame(BSD_1)
    LSA_1 =  pd.DataFrame(LSA_1)
    LSD_1 =  pd.DataFrame(LSD_1)
    GSA_1 =  pd.DataFrame(GSA_1)
    GSD_1 =  pd.DataFrame(GSD_1)
    DSA_1 =  pd.DataFrame(DSA_1)
    DSD_1 =  pd.DataFrame(DSD_1)
    SSL_1 =  pd.DataFrame(SSL_1)
    TDL_1 =  pd.DataFrame(TDL_1)
    HSL_1 =  pd.DataFrame(HSL_1)
    BSL_1 =  pd.DataFrame(BSL_1)
    LSL_1 =  pd.DataFrame(LSL_1)
    DSL_1 =  pd.DataFrame(DSL_1)
    CSL_1 =  pd.DataFrame(CSL_1)
    GSL_1 =  pd.DataFrame(GSL_1)
    SSLA_1 =  pd.DataFrame(SSLA_1)
    TDLA_1 =  pd.DataFrame(TDLA_1)
    HSLA_1 =  pd.DataFrame(HSLA_1)
    BSLA_1 =  pd.DataFrame(BSLA_1)
    LSLA_1 =  pd.DataFrame(LSLA_1)
    DSLA_1 =  pd.DataFrame(DSLA_1)
    CSLA_1 =  pd.DataFrame(CSLA_1)
    MM_1 =  pd.DataFrame(MM_1)
    SUB_1 =  pd.DataFrame(SUB_1)
    PASS_1 =  pd.DataFrame(PASS_1)
    REV_1 =  pd.DataFrame(REV_1)
    SUBA_1 =  pd.DataFrame(SUBA_1)
    PASSA_1 =  pd.DataFrame(PASSA_1)
    REVA_1 =  pd.DataFrame(REVA_1)



    Name_2 = pd.DataFrame(Name_2)

    Total_Wins_2 = pd.DataFrame(Total_Wins_2)
    Total_Losses_2=pd.DataFrame(Total_Losses_2)
    Total_KO_2= pd.DataFrame(Total_KO_2)
    Total_KO_Losses_2= pd.DataFrame(Total_KO_Losses_2)
    Total_SUB_2= pd.DataFrame(Total_SUB_2)
    Total_SUB_Losses_2= pd.DataFrame(Total_SUB_Losses_2)
    Total_Fights_2= pd.DataFrame(Total_Fights_2)
    Win_perc_2= pd.DataFrame(Win_perc_2)
    KO_Win_perc_2= pd.DataFrame(KO_Win_perc_2)
    KO_Loss_perc_2= pd.DataFrame(KO_Loss_perc_2)
    Sub_Win_perc_2= pd.DataFrame(Sub_Win_perc_2)
    Sub_loss_perc_2= pd.DataFrame(Sub_loss_perc_2)
    Decision_Win_perc_2 = pd.DataFrame(Decision_Win_perc_2)
    Decision_Loss_perc_2 = pd.DataFrame(Decision_Loss_perc_2)
    Win_Streak_2= pd.DataFrame(Win_Streak_2)
    Loss_Streak_2= pd.DataFrame(Loss_Streak_2)

    Age_2 =  pd.DataFrame(Age_2)
    SSA_2 =  pd.DataFrame(SSA_2)
    SSD_2 =  pd.DataFrame(SSD_2)
    HSA_2 =  pd.DataFrame(HSA_2)
    HSD_2 =  pd.DataFrame(HSD_2)
    CSA_2 =  pd.DataFrame(CSA_2)
    CSD_2 =  pd.DataFrame(CSD_2)
    BSA_2 =  pd.DataFrame(BSA_2)
    BSD_2 =  pd.DataFrame(BSD_2)
    LSA_2 =  pd.DataFrame(LSA_2)
    LSD_2 =  pd.DataFrame(LSD_2)
    GSA_2 =  pd.DataFrame(GSA_2)
    GSD_2 =  pd.DataFrame(GSD_2)
    DSA_2 =  pd.DataFrame(DSA_2)
    DSD_2 =  pd.DataFrame(DSD_2)
    SSL_2 =  pd.DataFrame(SSL_2)
    TDL_2 =  pd.DataFrame(TDL_2)
    HSL_2 =  pd.DataFrame(HSL_2)
    BSL_2 =  pd.DataFrame(BSL_2)
    LSL_2 =  pd.DataFrame(LSL_2)
    DSL_2 =  pd.DataFrame(DSL_2)
    CSL_2 =  pd.DataFrame(CSL_2)
    GSL_2 =  pd.DataFrame(GSL_2)
    SSLA_2 =  pd.DataFrame(SSLA_2)
    TDLA_2 =  pd.DataFrame(TDLA_2)
    HSLA_2 =  pd.DataFrame(HSLA_2)
    BSLA_2 =  pd.DataFrame(BSLA_2)
    LSLA_2 =  pd.DataFrame(LSLA_2)
    DSLA_2 =  pd.DataFrame(DSLA_2)
    CSLA_2 =  pd.DataFrame(CSLA_2)
    MM_2  = pd.DataFrame(MM_2)
    SUB_2 =  pd.DataFrame(SUB_2)
    PASS_2 =  pd.DataFrame(PASS_2)
    REV_2 =  pd.DataFrame(REV_2)
    SUBA_2 =  pd.DataFrame(SUBA_2)
    PASSA_2 =  pd.DataFrame(PASSA_2)
    REVA_2 =  pd.DataFrame(REVA_2)





    Stats_Against = pd.concat([Date,Event,Result_1,Result_2,Name_1,Age_1,Total_Wins_1,Total_Losses_1,Total_KO_1,Total_KO_Losses_1,Total_SUB_1,Total_SUB_Losses_1,Total_Fights_1,Win_perc_1,KO_Win_perc_1,
                               KO_Loss_perc_1,Sub_Win_perc_1,Sub_loss_perc_1,Decision_Win_perc_1,Decision_Loss_perc_1,Win_Streak_1,Loss_Streak_1,SSA_1,SSD_1,HSA_1,HSD_1,
                               CSA_1,CSD_1,BSA_1,BSD_1,LSA_1,LSD_1,GSA_1,GSD_1,DSA_1,DSD_1,SSL_1,TDL_1,HSL_1,BSL_1,LSL_1,DSL_1,CSL_1,GSL_1,SSLA_1,TDLA_1,HSLA_1,BSLA_1,
                               LSLA_1,DSLA_1,CSLA_1,MM_1,SUB_1,PASS_1,REV_1,SUBA_1,PASSA_1,REVA_1,
                               Name_2,Age_2,Total_Wins_2,Total_Losses_2,Total_KO_2,Total_KO_Losses_2,Total_SUB_2,Total_SUB_Losses_2,Total_Fights_2,Win_perc_2,KO_Win_perc_2,
                               KO_Loss_perc_2,Sub_Win_perc_2,Sub_loss_perc_2,Decision_Win_perc_2,Decision_Loss_perc_2,Win_Streak_2,Loss_Streak_2,SSA_2,SSD_2,HSA_2,HSD_2,
                               CSA_2,CSD_2,BSA_2,BSD_2,LSA_2,LSD_2,GSA_2,GSD_2,DSA_2,DSD_2,SSL_2,TDL_2,HSL_2,BSL_2,LSL_2,DSL_2,CSL_2,GSL_2,SSLA_2,TDLA_2,HSLA_2,BSLA_2,
                               LSLA_2,DSLA_2,CSLA_2,MM_2,SUB_2,PASS_2,REV_2,SUBA_2,PASSA_2,REVA_2],axis=1)

    Stats_Against.columns = ['Date','Event','Result_1','Result_2','Name_1','Age_1','Total_Wins_1','Total_Losses_1','Total_KO_1','Total_KO_Losses_1','Total_SUB_1','Total_SUB_Losses_1','Total_Fights_1','Win_perc_1','KO_Win_perc_1',
                               'KO_Loss_perc_1','Sub_Win_perc_1','Sub_loss_perc_1','Decision_Win_perc_1','Decision_Loss_perc_1','Win_Streak_1','Loss_Streak_1','SSA_1','SSD_1','HSA_1','HSD_1',
                               'CSA_1','CSD_1','BSA_1','BSD_1','LSA_1','LSD_1','GSA_1','GSD_1','DSA_1','DSD_1','SSL_1','TDL_1','HSL_1','BSL_1','LSL_1','DSL_1','CSL_1','GSL_1','SSLA_1','TDLA_1','HSLA_1','BSLA_1',
                               'LSLA_1','DSLA_1','CSLA_1','MM_1','SUB_1','PASS_1','REV_1','SUBA_1','PASSA_1','REVA_1',
                               'Name_2','Age_2','Total_Wins_2','Total_Losses_2','Total_KO_2','Total_KO_Losses_2','Total_SUB_2','Total_SUB_Losses_2','Total_Fights_2','Win_perc_2','KO_Win_perc_2',
                               'KO_Loss_perc_2','Sub_Win_perc_2','Sub_loss_perc_2','Decision_Win_perc_2','Decision_Loss_perc_2','Win_Streak_2','Loss_Streak_2','SSA_2','SSD_2','HSA_2','HSD_2',
                               'CSA_2','CSD_2','BSA_2','BSD_2','LSA_2','LSD_2','GSA_2','GSD_2','DSA_2','DSD_2','SSL_2','TDL_2','HSL_2','BSL_2','LSL_2','DSL_2','CSL_2','GSL_2','SSLA_2','TDLA_2','HSLA_2','BSLA_2',
                               'LSLA_2','DSLA_2','CSLA_2','MM_2','SUB_2','PASS_2','REV_2','SUBA_2','PASSA_2','REVA_2']

    return Stats_Against





def get_x_y(Stats_Against):
    k = []
    for i in range(0,len(Stats_Against)):
        if Stats_Against['Name_1'][i] == Stats_Against['Name_2'][i]:
            k.append(i)

    Stats_Against = Stats_Against.drop(k)

    Stats_Against['sorted_row'] = [sorted([a,b]) for a,b,c in zip(Stats_Against.Name_1, Stats_Against.Name_2,Stats_Against.Date)]
    Stats_Against['sorted_row'] = Stats_Against['sorted_row'].astype(str)
    Stats_Against = Stats_Against.drop_duplicates(subset=['sorted_row'],keep='first')

    Stats_Against = Stats_Against.dropna()
    #Stats_Against = pd.concat([Stats_Against, pd.get_dummies(Stats_Against['Weight_Class'])], axis=1)

    #Reset index
    Stats_Against = Stats_Against.reset_index()

    #Get binary variabel for fight result
    Fight_Result = []

    for i in range(0,len(Stats_Against)):
        if Stats_Against['Result_1'][i] == 1:
            Fight_Result.append(0)
        else:
            Fight_Result.append(1)

    Fight_Result = pd.DataFrame(Fight_Result)
    Fight_Result.columns = ['Fight_Result']
    Stats_Against = pd.concat([Stats_Against,Fight_Result],axis=1)

    Stats_Against['Delta_Total_Wins'] = Stats_Against['Total_Wins_1'] - Stats_Against['Total_Wins_2']
    Stats_Against['Delta_Total_Losses'] = Stats_Against['Total_Losses_1'] - Stats_Against['Total_Losses_2']
    Stats_Against['Delta_Total_KO'] = Stats_Against['Total_KO_1'] - Stats_Against['Total_KO_2']
    Stats_Against['Delta_Total_KO_Losses'] = Stats_Against['Total_KO_Losses_1'] - Stats_Against['Total_KO_Losses_2']
    Stats_Against['Delta_Total_SUB'] = Stats_Against['Total_SUB_1'] - Stats_Against['Total_SUB_2']
    Stats_Against['Delta_Total_SUB_Losses'] = Stats_Against['Total_SUB_Losses_1'] - Stats_Against['Total_SUB_Losses_2']

    Stats_Against['Delta_Total_Fights'] = Stats_Against['Total_Fights_1'] - Stats_Against['Total_Fights_2']
    Stats_Against['Delta_Win_perc'] = Stats_Against['Win_perc_1'] - Stats_Against['Win_perc_2']
    Stats_Against['Delta_KO_Win_perc'] = Stats_Against['KO_Win_perc_1'] - Stats_Against['KO_Win_perc_2']
    Stats_Against['Delta_KO_Loss_perc'] = Stats_Against['KO_Loss_perc_1'] - Stats_Against['KO_Loss_perc_2']
    Stats_Against['Delta_Sub_Win_perc'] = Stats_Against['Sub_Win_perc_1'] - Stats_Against['Sub_Win_perc_2']
    Stats_Against['Delta_Sub_Loss_perc'] = Stats_Against['Sub_loss_perc_1'] - Stats_Against['Sub_loss_perc_2']

    Stats_Against['Delta_Decision_Win_perc'] = Stats_Against['Decision_Win_perc_1'] - Stats_Against['Decision_Win_perc_2']
    Stats_Against['Delta_Decision_Loss_perc'] = Stats_Against['Decision_Loss_perc_1'] - Stats_Against['Decision_Loss_perc_2']
    Stats_Against['Delta_Win_Streak'] = Stats_Against['Win_Streak_1'] - Stats_Against['Win_Streak_2']
    Stats_Against['Delta_Loss_Streak'] = Stats_Against['Loss_Streak_1'] - Stats_Against['Loss_Streak_2']

    Stats_Against['Delta_Age'] = Stats_Against['Age_1'] - Stats_Against['Age_2']
    Stats_Against['Delta_SSA'] = Stats_Against['SSA_1'] - Stats_Against['SSA_2']
    Stats_Against['Delta_SSD'] = Stats_Against['SSD_1'] - Stats_Against['SSD_2']
    Stats_Against['Delta_HSA'] = Stats_Against['HSA_1'] - Stats_Against['HSA_2']
    Stats_Against['Delta_HSD'] = Stats_Against['HSD_1'] - Stats_Against['HSD_2']
    Stats_Against['Delta_CSA'] = Stats_Against['CSA_1'] - Stats_Against['CSA_2']
    Stats_Against['Delta_CSD'] = Stats_Against['CSD_1'] - Stats_Against['CSD_2']
    Stats_Against['Delta_BSA'] = Stats_Against['BSA_1'] - Stats_Against['BSA_2']
    Stats_Against['Delta_BSD'] = Stats_Against['BSD_1'] - Stats_Against['BSD_2']
    Stats_Against['Delta_LSA'] = Stats_Against['LSA_1'] - Stats_Against['LSA_2']

    Stats_Against['Delta_LSD'] = Stats_Against['LSD_1'] - Stats_Against['LSD_2']
    Stats_Against['Delta_GSA'] = Stats_Against['GSA_1'] - Stats_Against['GSA_2']
    Stats_Against['Delta_GSD'] = Stats_Against['GSD_1'] - Stats_Against['GSD_2']
    Stats_Against['Delta_DSA'] = Stats_Against['DSA_1'] - Stats_Against['DSA_2']
    Stats_Against['Delta_DSD'] = Stats_Against['DSD_1'] - Stats_Against['DSD_2']
    Stats_Against['Delta_SSL'] = Stats_Against['SSL_1'] - Stats_Against['SSL_2']
    Stats_Against['Delta_TDL'] = Stats_Against['TDL_1'] - Stats_Against['TDL_2']
    Stats_Against['Delta_HSL'] = Stats_Against['HSL_1'] - Stats_Against['HSL_2']
    Stats_Against['Delta_BSL'] = Stats_Against['BSL_1'] - Stats_Against['BSL_2']
    Stats_Against['Delta_LSL'] = Stats_Against['LSL_1'] - Stats_Against['LSL_2']

    Stats_Against['Delta_DSL'] = Stats_Against['DSL_1'] - Stats_Against['DSL_2']
    Stats_Against['Delta_CSL'] = Stats_Against['CSL_1'] - Stats_Against['CSL_2']
    Stats_Against['Delta_GSL'] = Stats_Against['GSL_1'] - Stats_Against['GSL_2']
    Stats_Against['Delta_SSLA'] = Stats_Against['SSLA_1'] - Stats_Against['SSLA_2']
    Stats_Against['Delta_TDLA'] = Stats_Against['TDLA_1'] - Stats_Against['TDLA_2']
    Stats_Against['Delta_HSLA'] = Stats_Against['HSLA_1'] - Stats_Against['HSLA_2']
    Stats_Against['Delta_BSLA'] = Stats_Against['BSLA_1'] - Stats_Against['BSLA_2']
    Stats_Against['Delta_LSLA'] = Stats_Against['LSLA_1'] - Stats_Against['LSLA_2']
    Stats_Against['Delta_DSLA'] = Stats_Against['DSLA_1'] - Stats_Against['DSLA_2']
    Stats_Against['Delta_CSLA'] = Stats_Against['CSLA_1'] - Stats_Against['CSLA_2']
    Stats_Against['Delta_MM'] = Stats_Against['MM_1'] - Stats_Against['MM_2']
    Stats_Against['Delta_SUB'] = Stats_Against['SUB_1'] - Stats_Against['SUB_2']
    Stats_Against['Delta_PASS'] = Stats_Against['PASS_1'] - Stats_Against['PASS_2']
    Stats_Against['Delta_REV'] = Stats_Against['REV_1'] - Stats_Against['REV_2']
    Stats_Against['Delta_SUBA'] = Stats_Against['SUBA_1'] - Stats_Against['SUBA_2']
    Stats_Against['Delta_PASSA'] = Stats_Against['PASSA_1'] - Stats_Against['PASSA_2']
    Stats_Against['Delta_REVA'] = Stats_Against['REVA_1'] - Stats_Against['REVA_2']


    X = Stats_Against.iloc[:,115::]
    y = Stats_Against.iloc[:,114]
    X = pd.DataFrame(X)
    y = pd.DataFrame(y)
    Data = pd.concat([y,X],axis=1)
    Data = Data.dropna()

    y = Data.iloc[:,0]
    X = Data.iloc[:,1::]
    return X,y
