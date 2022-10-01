import json
import ccxt
import os

# ดึงไฟล์ json จาก path
dir_path = os.path.dirname(os.path.realpath(__file__))

def read_config():
    global dir_path
    with open(dir_path + '/config.json') as json_file:
        return json.load(json_file)

config = read_config()

# API and Secret setting
api_key = config["api_key"]
api_secret = config["api_secret"]

bot_name = config["bot_name"]
pair = config["pair"]

import ccxt
print('CCXT Version:', ccxt.__version__)
exchange = ccxt.ftx({
    'apiKey': api_key,
    'secret': api_secret,
})
markets = exchange.load_markets()

