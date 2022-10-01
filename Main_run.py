import trading
import account
import DB_main as db
import time
import numpy as np
from datetime import datetime
import pandas as pd
config = account.read_config()
bot_name = config["bot_name"]
pair = config['pair']
asset_name = config['asset_name']
qoute_currency = config["qoute_currency"]
user_id = 1  # รอแก้ให้รับค่าจาก config
bot_id  = 1  # รอแก้ให้รับค่าจาก config

# Grid Setting
up_zone = config["up_zone"]
low_zone = config["low_zone"]
grid_qty = config["grid_qty"]  # จำนวนเส้น gird
capital = config["capital"] #จำนวนการซื้อ 

my_grid_zone = trading.my_grid_zone_calculation(up_zone,low_zone,grid_qty)
step = my_grid_zone[0]-my_grid_zone[1] #หาระยะ gird 
my_grid_zone = np.flip(my_grid_zone)
# Order Type
post_only = True  # Maker or Taker (วางโพซิชั่นเป็น MAKER เท่านั้นหรือไม่ True = ใช่ // Defalut = True)
order_type = "limit" # limit, market

#เริ่มต้น bot 
Time = datetime.fromtimestamp(int(time.time()))
db.log(Time, 1, 'Bot Started')
exchange_markets = account.exchange.load_markets()
money_we_need = np.sum(capital*my_grid_zone)
print("money we need = ",money_we_need," dollar")             
print("Step-Grid distance = ",step)
#db.readindex_csv_id_buy("id01")
#account.exchange.cancelAllOrders()
#print(db.csv_check_empty())
#print(trading.create_buy_order(pair,1,0.422))
#account.exchange.cancel_all_orders()
order1 = '185861708523' #0.42 order
#print(trading.create_buy_order(pair,1,0.25))
#print(trading.create_buy_order(pair,1,0.25)['fee'])
#print('\n\n')
#print(trading.get_order(order1)['id'])
#print(trading.get_order(order1)['fee'])
#print(trading.get_order(order1)['filled'])
#print(trading.get_order(order1)['status'])
#print()
#print(account.exchange.fetchOrders()[-1])
#print(account.exchange.fetchOrders()[-1]['filled']) 'filled'
db_call = db.call_db()
#print(db_call)
#jk = str(int(db_call['id_buy'][0]))
#print(trading.get_order(jk))
#fee = fee[0]
#fee = fee['cost']*fee['fee']['rate']
init_round = 0
#print(db_call['status_buy'][0])
#print(pd.isna(db_call.loc[0,'status_sell']))
#gi = db_call.loc[db_call['zone']==4]
#gi_b = db.return_all_status(gi['status_buy'])
#gi_s = db.return_all_status(gi['status_sell'])




if db.csv_check_empty():
    print("Start Intizle")
    for gird in my_grid_zone:
        if gird < trading.get_price(pair):
            info_trade = trading.create_buy_order(pair, capital, gird)
            time.sleep(0.01)
            id_buy = info_trade['id']
            id_sell = None
            time_db = db.return_nowtime()
            time_stamp_buy = time_db[0]
            time_buy = time_db[1]
            time_stamp_sell = None
            time_sell = None
            pair = pair
            fee = 0.0002 * gird
            price = gird
            cost = gird + fee
            status_buy = trading.get_order(id_buy)['filled']
            status_sell = None
            zone = init_round
            Data1 = [id_buy,id_sell,time_stamp_buy,time_buy,time_stamp_sell,time_sell,pair,price,fee,cost,status_buy,status_sell,zone]
            db.update_tradelog(Data1)
            print(f"BuyZone({zone}):ID({id_buy}):{time_stamp_buy}:{time_buy} ,Pirce:{price},Status:{status_buy},Zone({zone})\n")
        else:
            id_buy = None
            id_sell = None
            time_db = db.return_nowtime()
            time_stamp_buy = None
            time_buy = None
            time_stamp_sell = None
            time_sell = None
            pair = pair
            fee = 0.0002 * gird
            price = gird
            cost = gird + fee
            status_buy = None
            status_sell = None
            zone = init_round
            Data1 = [id_buy,id_sell,time_stamp_buy,time_buy,time_stamp_sell,time_sell,pair,price,fee,cost,status_buy,status_sell,zone]
            db.update_tradelog(Data1)
            print(f"BuyZone({zone}):ID({id_buy}):{time_stamp_buy}:{time_buy} ,Pirce:{price},Status:{status_buy}\n")
        init_round+=1
    print("End intizle")
while True:
    try:
        gird_df = db.call_db()
        cash = trading.get_cash(qoute_currency)
        if cash < money_we_need:
            Time = datetime.today()
            Time = time.strftime("%m/%d/%Y, %H:%M:%S", Time)
            db.log(Time, 69, 'Cash Not Enough')
            break
        #buy and record 3 state nan 0 , 1 nan ยังไม่ได้ซื้อ 0 ส่งคำสั่งซื้อไปแล้ว 1 ซื้อสำเร็จ
        for dfg in range(len(gird_df)):
            if pd.isna(gird_df.loc[dfg,'id_buy']):
                price_g_old = gird_df.loc[dfg,'zone']
                price_g_old = my_grid_zone[price_g_old]
                if price_g_old < trading.get_price(pair):
                    info_trade = trading.create_buy_order(pair, capital, price_g_old)
                    time.sleep(0.01)
                    id_buy = info_trade['id']
                    time_db = db.return_nowtime()
                    time_stamp_buy = time_db[0]
                    time_buy = time_db[1]
                    gird_df.loc[dfg,'id_buy'] = id_buy
                    gird_df.loc[dfg,'timestamp_buy'] = time_stamp_buy 
                    gird_df.loc[dfg,'time_buy'] = time_buy
                    status_buy = gird_df.loc[dfg,'status_buy'] = 0.0
                    new_zone_init = gird_df.loc[dfg,'zone']
                    print(f"*****BuyZone({new_zone_init}) New ID({id_buy}):{time_stamp_buy}:{time_buy} ,Pirce:{price_g_old},Status:{status_buy}\n")
        gird_df.to_csv(db.get_file_path(),index=False)
        #check_buy and sell
        gird_df = db.call_db()
        for dfg in range(len(gird_df)):
            idB = gird_df.loc[dfg,'id_buy']
            if pd.isna(idB):
                continue
            price_sell = gird_df.loc[dfg,'zone']
            price_sell = my_grid_zone[price_sell]
            sta_b = trading.get_order(idB)['filled']
            sta_s_check = gird_df.loc[dfg,'status_sell']
            if pd.isna(sta_s_check) and sta_b == 1.0:
                info_trade = trading.create_sell_order(pair, capital,price_sell+step)
                id_sell = gird_df.loc[dfg,'id_sell'] = info_trade['id']
                time_db_s = db.return_nowtime()
                dayt=gird_df.loc[dfg,'timestamp_sell'] = time_db_s[0]
                tt = gird_df.loc[dfg,'time_sell'] = time_db_s[1]
                gird_df.loc[dfg,'status_sell'] = 0
                gird_df.loc[dfg,'status_buy'] = 1
                cb_s = gird_df.loc[dfg,'zone']
                print(f"Sell Zone({cb_s}) ID:{id_sell}: zone({price_sell}) : Time:{dayt}:{tt}")
                time.sleep(0.01)
        gird_df.to_csv(db.get_file_path(),index=False)
        
        #sell check
        gird_df = db.call_db()
        for dfg in range(len(gird_df)):
            idS = gird_df.loc[dfg,'id_sell']
            std_s = gird_df.loc[dfg,'status_sell']
            if pd.isna(idS) or std_s == 1.0:
                continue
            sta_iss = trading.get_order(idS)['filled']
            if sta_iss == 1.0:
                gird_df.loc[dfg,'status_sell'] = 1.0
                zone_sell = gird_df.loc[i,'zone']
                print(f"Sell Sucesce zone({zone_sell}:{my_grid_zone[zone_sell]})")
        gird_df.to_csv(db.get_file_path(),index=False)
        #buy check zone 
        gird_df = db.call_db()
        for i in range(len(my_grid_zone)):
            gi = gird_df.loc[gird_df['zone']==i]
            gi_b = db.return_all_status(gi['status_buy'])
            gi_s = db.return_all_status(gi['status_sell'])
            if gi_b and gi_s:
                gird = my_grid_zone[i]
                if gird < trading.get_price(pair):
                    info_trade = trading.create_buy_order(pair, capital, gird)
                    time.sleep(0.01)
                    id_buy = info_trade['id']
                    id_sell = None
                    time_db = db.return_nowtime()
                    time_stamp_buy = time_db[0]
                    time_buy = time_db[1]
                    time_stamp_sell = None
                    time_sell = None
                    pair = pair
                    fee = 0.0002 * gird
                    price = gird
                    cost = gird + fee
                    status_buy = trading.get_order(id_buy)['filled']
                    status_sell = None
                    zone = i
                    Data1 = [id_buy,id_sell,time_stamp_buy,time_buy,time_stamp_sell,time_sell,pair,price,fee,cost,status_buy,status_sell,zone]
                    db.update_tradelog(Data1)
                    print(f"BuyZone({zone}) Normal ID({id_buy}):{time_stamp_buy}:{time_buy} ,Pirce:{price},Status:{status_buy}\n")
                    

                    
    except Exception as e:
        print('Error : {}'.format(str(e)))
        Time = datetime.today()
        Time = Time.strftime("%m/%d/%Y, %H:%M:%S")
        # Check credential
        error_text = str(e)
        if 'permissions' in error_text or 'Not logged in' in error_text:
            print('Bot stopped due to credential error')
            Time = datetime.today()
            Time = Time.strftime("%m/%d/%Y, %H:%M:%S")
            code = 401
            db.log(Time, code, 'Bot stopped due to credential error')
            #log permission denied : 400
            break
        
        if 'No such market:' in error_text:
            print('Bot stopped due to pair error')
            Time = datetime.today()
            Time = Time.strftime("%m/%d/%Y, %H:%M:%S")
            code = 400
            db.log(Time, code, 'Bot stopped due to pair error')
            #log pair error 400
            break
        db.log(Time, 999, error_text)
