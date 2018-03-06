"""
参考URL
https://qiita.com/shionhonda/items/bd2a7aaf143eff4972c4
http://kappazu.com/2017/11/24/%E4%BB%AE%E6%83%B3%E9%80%9A%E8%B2%A8%E8%87%AA%E5%8B%95%E5%A3%B2%E8%B2%B7%E5%85%A5%E9%96%80%E3%80%80python%E3%81%A7quoinex-api%E3%81%A6%E3%81%99%E3%81%A8%E2%91%A0/
https://qiita.com/wakaba130/items/5f54aed913156dc4438f
https://qiita.com/Akira-Taniguchi/items/e52930c881adc6ecfe07
"""
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

#bitflyer
# bfapi = pybitflyer.API()
# bfticker = bfapi.ticker(product_code="BTC_JPY")
# print("{}".format(json.dumps(bfticker,indent=4)))

#zaif
zaif = ZaifPublicApi()
print(zaif.last_price('btc_jpy'))

# #coincheck

#quoinex
# GET /products/code/:code/:currency_pair_code
# Markets_BTCJPY = requests.get('https://api.quoine.com/products/code/CASH//BTCJPY')

# sirtmp = json.loads(Markets_BTCJPY.text)
# print("{}".format(json.dumps(sirtmp,indent=4)))

raws = []
timestamp = []
start = time.time()
t = 3

#1分おきにt分間データを収集
while True:
    # 毎分00秒に稼働
    if datetime.now().strftime('%S') [0:2]== '00':
        # データの更新
        last_price = zaif.last_price('btc_jpy')
        print("{}".format(json.dumps(last_price, indent=4)))
        raws = np.append(raws, last_price['last_price'])
        timestamp = np.append(timestamp, datetime.now())
        # 次の00秒まで休憩
        time.sleep(57)
        elapsed_time = time.time() - start
        if elapsed_time > 60*t:#t分後にデータを処理してbreak
            print(raws)
            print(timestamp)
            result = zip(timestamp,raws)
            f = open('result_zaif.txt', 'w')
            for x in result:
                f.write(str(x) + "\n")
            f.close()
            #pandasを使って処理
            df = pd.DataFrame({'raws':raws}, index = timestamp)
            print(df)
            #csv形式で保存
            df.to_csv("result_zaif.csv")
            break
