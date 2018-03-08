import json
import requests
import numpy as np
import pandas as pd
# bitFlyerにアクセスするのに使う
import pybitflyer
#Zaifにアクセスするのに使う
from zaifapi.impl import ZaifPublicApi
# 時間の管理に使う
import time
from datetime import datetime
#データのプロットに使う
import matplotlib
import matplotlib.pyplot as plt

bitflyerapi = pybitflyer.API()
zaifapi = ZaifPublicApi()

bitflyer_raws = []
zaif_raws = []
quoinex_raws = []
coincheck_raws = []
timestamp = []
start = time.time()
t = 3

#1分おきにt分間データを収集
while True:
    # 毎分00秒に稼働
    if datetime.now().strftime('%S') [0:2]== '00':
        # データの取得
        bitflyer_tick = bitflyerapi.ticker(product_code="BTC_JPY")
        print("{}".format(json.dumps(bitflyer_tick,indent=4)))
        zaif_last_price = zaifapi.last_price('btc_jpy')
        print("{}".format(json.dumps(zaif_last_price, indent=4)))
        Quoinex_Markets_BTCJPY = requests.get('https://api.quoine.com/products/code/CASH//BTCJPY')
        quoinex_tick = json.loads(Quoinex_Markets_BTCJPY.text)
        print("{}".format(json.dumps(quoinex_tick, indent=4)))
        #データの更新
        bitflyer_raws = np.append(bitflyer_raws, bitflyer_tick['ltp'])
        zaif_raws = np.append(zaif_raws, zaif_last_price['last_price'])
        quoinex_raws = np.append(quoinex_raws, quoinex_tick['last_traded_price'])
        timestamp = np.append(timestamp, datetime.now())
        # 次の00秒まで休憩
        time.sleep(57)
        #経過時間の計測
        elapsed_time = time.time() - start
        if elapsed_time > 60*t:#t分後にデータを処理してbreak
            #pandasを使って処理
            df = pd.DataFrame({'bitflyer':bitflyer_raws,'zaif':zaif_raws,'quoinex':quoinex_raws}, index = timestamp)
            print(df)
            #csv形式で保存
            df.to_csv("result.csv")
            break
