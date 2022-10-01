
import account
import pandas as pd
from datetime import datetime
import pytz
import csv
import os
import json
import time
import sys

exchange = account.exchange
bot_name = account.bot_name 

tradelog_file = "\tradinglog_{}.csv".format(bot_name)

trading_call_back = 5

def check_db(tradelog_file):
    try:
        tradinglog = pd.read_csv(tradelog_file)
        print('DataBase Exist Loading DataBase....')
    except:
        tradinglog = pd.DataFrame(columns=['id_buy','id_sell', 'timestamp_buy', 'time_buy','timestamp_sell', 'time_sell','pair', 'price','fee','cost','status_buy','status_sell','zone'])
        tradinglog.to_csv(tradelog_file, index=False)
        print("Database Created")
        
    return tradinglog


def update_tradelog(row_input):
    with open(tradelog_file, "a+", newline='') as fp:
                wr = csv.writer(fp, dialect='excel')
                wr.writerow(row_input)
    Time = datetime.fromtimestamp(int(time.time()))
    print('Recording Trade ID : {}'.format(Time))

# Database Setup
print("------------------------------")
print('Checking Database file.....')
tradinglog = check_db(tradelog_file)

print("------------------------------")

def search_zone_notyet(df,zone):    
    for i in range(len(df)):
        if df['zone'][i] == zone:
            return False
        else:
            return True

def get_file_path():
    return tradelog_file 

def readindex_csv_id_buy(id_target):
    global tradelog_file
    file = tradelog_file
    csv_file = pd.read_csv(file)
    return csv_file[csv_file['id_buy']== id_target]
    #if current rows 2nd value is equal to input, print that row
def readindex_csv_id_sell(id_target):
    global tradelog_file
    file = tradelog_file
    csv_file = pd.read_csv(file)
    return csv_file[csv_file['id_sell']== id_target]
    #if current rows 2nd value is equal to input, print that row
def update_status_buy_zero(df,index):
    df.loc[index,'status_buy'] = 0.0
def update_status_sell_zero(df,index):
    df.loc[index,'status_sell'] = 0.0


def csv_check_empty(): 
    global tradelog_file
    file = tradelog_file
    csv_file = pd.read_csv(file)
    try:
        x = csv_file.iloc[-1]
        return False
    except:
        return True

def zone_check(price):
    global tradelog_file
    file = tradelog_file
    csv_file = pd.read_csv(file)

def return_nowtime():
    now = datetime.today()
    return [now.strftime("%d/%m/%Y"),now.strftime("%H:%M:%S")]


        
def update_tradelog_id_sell(price):
    dfg = pd.read_csv(tradelog_file)
    for i in range(len(dfg)):
        if dfg.loc[i,'price'] == price and dfg['status_buy'][i] == 1.0 : # and status
            return True
        else:
            return False
    dfg.to_csv(tradelog_file,index=False)

def update_tradelog_id_buy(price):
    dfg = pd.read_csv(tradelog_file)
    for i in range(len(dfg)):
        if dfg.loc[i,'price'] == price and dfg['status_buy'][i] == 1.0 : # and status
            return True
        else:
            return False
    dfg.to_csv(tradelog_file,index=False)
    
def update_status_buy(df,index):
    df.loc[index,'status_buy'] = 1.0

def update_status_sell(df,index):
    df.loc[index,'status_sell'] = 1.0

def search_price_notyet(df,price):    
    for i in range(len(df)):
        if df['price'][i] == price:
            return False
        else:
            return True

def call_db():
    return pd.read_csv(tradelog_file)

def log(Time, code, message):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    with open(dir_path + '/log.txt', 'a') as txt_file:
        data = "{} | {} | {} \n".format(Time, code, message)
        txt_file.write(data)

def return_all_status(all_status):
    for i in range(len(all_status)):
        if pd.isna(all_status.iloc[i]) or all_status.iloc[i] == 0:
            return False
        
    return True