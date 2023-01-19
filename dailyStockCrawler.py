import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import math
from datetime import date,timedelta
from urllib.request import urlopen
from dateutil import rrule
import matplotlib.pyplot as plt
import datetime
import json
import time
from fake_useragent import UserAgent

def chooseStock(x):
    choosenStock = ["台積電", "聯發科"]
    arr = np.array(choosenStock)
    if x[1] in arr:
        return x
    
# def craw_stock():

url = "https://www.twse.com.tw/zh/exchangeReport/MI_INDEX?&date=20221222&type=ALL"
user_agent = UserAgent()
print('user-agent: ', user_agent.random)
global header 
header= {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'User-agent': user_agent.random,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=A20E4F0C7B41C796E9ED7DCA35F46FAA; _ga=GA1.3.1665951062.1671879707; _gid=GA1.3.1608519753.1671879707; _gat=1',
    'Host': 'www.twse.com.tw',
    'Origin': 'https://www.twse.com.tw',
    'Referer': 'https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html',
    # 'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpReques'
}


now = datetime.datetime.now().strftime("%Y-%m-%d")         # 取得現在時間
e_month = date(*[int(x) for x in now.split('-')])
print(e_month)

# res = requests.post(url, headers = header)

# print(res.status_code)
# # print(res.json())
# resJson = res.json()
# data = resJson["data9"]
# result = list(filter(chooseStock, data))

# df = pd.DataFrame(result)

# print(df)