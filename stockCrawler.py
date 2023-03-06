import requests
import pandas as pd
import numpy as np
import math
from datetime import date, timedelta
from dateutil import rrule
import datetime
# from datetime import datetime
import time
from fake_useragent import UserAgent
from enum import Enum
import os
import argparse


class QueryType(Enum):
    listed = 0
    OTC = 1
    TWII = 2


        
class Stock():
    def __init__(self, args):
        self.queryType = QueryType[args['queryType']]  # 設定要跑(加權，上市，興櫃)
        self.initOrFill = args['initOrFill'] # fill
        self.startDate = args['startDate'] #"2022-01-01"
        self.endDate = args['endDate'] #now
        self.choosenStock = args['choosenStock'] # ['1301', '2385', '2420', '3030', '9933']
        self.saveFileName = args['saveFileName'] # stock
        self.choosenStockDK = []
        
        user_agent = UserAgent()
        self.header = {
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'User-agent': user_agent.random,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Content-Length': '36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'JSESSIONID=A20E4F0C7B41C796E9ED7DCA35F46FAA; _ga=GA1.3.1665951062.1671879707; _gid=GA1.3.1608519753.1671879707; _gat=1',
            # 'Host': 'www.twse.com.tw',
            # 'Origin': 'https://www.twse.com.tw',
            # 'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin',
            # 'X-Requested-With': 'XMLHttpReques'
        }
        # asda = self.craw_one_day('20221223')
        # print(asda)

        if self.initOrFill == 'init':
            self.runToCrawler()
        else:
            self.getRestStock()
        
    
    def getRestStock(self):
        '''補齊沒有的股票用'''
        dirpath = os.getcwd()
        print("dirpath = ", dirpath, "\n")

        output_path = os.path.join(dirpath, str(self.saveFileName) + '.csv')
        print(output_path,"\n")
        readDf = pd.read_csv(str(self.saveFileName) + '.csv')
        startDateStr = readDf.iat[-1, 0] # 取得文件中最後一筆的日期
        # print(dateStr)
        startDateStr = Tools().transform_date(startDateStr) # 將民國轉西元
        startDate = date(*[int(x) for x in startDateStr.split('/')])
        startDate = startDate + datetime.timedelta(days=1)
        print('開始沒有的日期:', startDate)
        endDateStr = datetime.datetime.now().strftime("%Y-%m-%d") # 取得現在時間
        # now = '2022-12-27'
        print('更新到的日期:', endDateStr)
        endDate = date(*[int(x) for x in endDateStr.split('-')])
        print(endDate)
        for dt in rrule.rrule(rrule.DAILY, dtstart = startDate, until = endDate):
            print(dt)
            temp = self.craw_one_day(dt)
            print(temp)
            # 判斷如果是空的話，就不用處理(就是當天沒有開盤所以沒有資料)
            if temp.size != 0:
                tempDate = dt.strftime('%Y%m%d')
                tempDate = tempDate.replace(tempDate[0:4], str(int(tempDate[0:4]) - 1911)) # 西元轉民國
                # tempDate = f"{tempDate[:3]}/{tempDate[3:5]}/{tempDate[5:]}"
                tempDate = tempDate[:3] + '/' + tempDate[3:5] + '/' + tempDate[5:]
                temp = np.insert(temp, 0, tempDate) # 第一行'日期' + 股票價格
                print(temp,'\n--------------------------')
                print('temp', len(temp), 'readDfColumn', len(readDf.columns))
                if len(temp) != len(readDf.columns):
                    for i in range(len(readDf.columns) - len(temp)):
                        temp = np.append(temp, ' ')
                readDf.loc[len(readDf.index)] = temp
                readDf.to_csv(str(self.saveFileName) + '.csv', encoding='utf_8_sig', index=False)
                time.sleep(5)
           
            # readDf[dt] = self.craw_one_day(dt)
    
    def runToCrawler(self):
        '''初始建檔案用的，因為過多資料，不能一天一天撈，使用不同的API'''
        stocks = [2420, 3030, 9933]#[1301, 2385, 2420, 3030, 9933]

        if self.queryType == QueryType.TWII:
            df = self.craw_stock([], self.startDate, self.endDate)
            df.set_index("日期", inplace=True)
            readDf = pd.read_csv(str(self.saveFileName) + '.csv')
            df = df.drop(['開盤指數', '最高指數', '最低指數'], axis=1)
            readDf['加權指數'] = df['收盤指數'].to_numpy()
            readDf.to_csv(str(self.saveFileName) + '.csv', encoding='utf_8_sig', index=False)
        elif self.queryType == QueryType.listed:
            for index, stock in enumerate(self.choosenStock):
                df = self.craw_stock(stock, self.startDate, self.endDate)
                df.set_index("日期", inplace=True)
                # 如果是第一次跑，需要跑這個，因為需要第一行有日期
                if index == 0:
                    df = df.drop(['成交股數', '成交金額', '開盤價', '最高價', '最低價', '漲跌價差', '成交筆數'], axis=1)
                    df.to_csv(str(self.saveFileName) + '.csv', encoding='utf_8_sig')
                else:
                    readDf = pd.read_csv(str(self.saveFileName) + '.csv')
                    df = df.drop(['成交股數', '成交金額', '開盤價', '最高價',
                                '最低價', '漲跌價差', '成交筆數'], axis=1)
                    readDf[stock] = df['收盤價'].to_numpy()
                    readDf.to_csv(str(self.saveFileName) + '.csv', encoding='utf_8_sig', index=False)

    def craw_stock(self, stock_number, start_month, end_month):
        b_month = date(*[int(x) for x in start_month.split('-')])
        print(b_month)
        now = datetime.datetime.now().strftime("%Y-%m-%d")  # 取得現在時間
        print(now)
        if end_month == 'now':
            e_month = date(*[int(x) for x in now.split('-')])
        else:
            e_month = date(*[int(x) for x in end_month.split('-')])
        print(e_month)

        result = pd.DataFrame()
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=b_month, until=e_month):
            print(dt)
            if self.queryType == QueryType.TWII:
                result = pd.concat([result, self.craw_weighted_one_month(dt)], ignore_index=True)
            elif self.queryType == QueryType.listed:
                result = pd.concat([result, self.craw_one_month(stock_number, dt)], ignore_index=True)

            print(result)
            time.sleep(5)
        return result
    



    
    def craw_weighted_one_month(self, date):
        '''發行量加權股價指數歷史資料.'''
        url = (
            "https://www.twse.com.tw/zh/indicesReport/MI_5MINS_HIST?response=json&date=" +
            date.strftime('%Y%m%d')
        )
        self.header['Referer'] = 'https://www.twse.com.tw/zh/page/trading/indices/MI_5MINS_HIST.html'
        res = requests.post(url, headers = self.header)
        data = res.json()
        return pd.DataFrame(data['data'], columns=data['fields'])

    # 爬取每月股價的目標網站並包裝成函式


    def craw_one_month(self, stock_number, date):
        url = (
            "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" +
            date.strftime('%Y%m%d') +
            "&stockNo=" +
            str(stock_number)
        )
        self.header['Referer'] = 'https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html'
        res = requests.post(url, headers=self.header)
        data = res.json()
        return pd.DataFrame(data['data'], columns=data['fields'])

    def craw_one_day(self, date):
        url = "https://www.twse.com.tw/zh/exchangeReport/MI_INDEX?&date="+ date.strftime('%Y%m%d') +"&type=ALL"
        self.header['Referer'] = 'https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html'
        res = requests.post(url, headers = self.header)

        # print(res.status_code)
        # # print(res.json())
        resJson = res.json()
        if resJson['stat'] == 'OK':
            parseStockNumpy = self.parseStock(resJson)
            parseTWIINumpy = self.parseTWII(resJson)
            return np.concatenate((parseStockNumpy, parseTWIINumpy))
        else:
            return np.array([])
        

    def parseStock(self, resJson):
        data = resJson["data9"]
        # result = list(filter(chooseStock, data))

        df = pd.DataFrame(data, columns = resJson['fields9'])
        group = df.groupby('證券代號') # 資料做分組方便查找
        # tempDF = pd.DataFrame([], columns = resJson['fields9'])
        tempDF = pd.DataFrame()
        list_string = map(str, self.choosenStock)
        for stock in list_string:
            temp = group.get_group(stock) # 括弧內放入要取出的類別
            tempDF = pd.concat([tempDF, temp], axis = 0)
        numpyDF = tempDF['收盤價'].to_numpy()
        tempDF = tempDF['收盤價']
        tempDF.to_csv('asdsadsad.csv', encoding='big5')
        return numpyDF

    def parseTWII(self, resJson):
        data = resJson['data1']
        df = pd.DataFrame(data, columns = resJson['fields1'])
        group = df.groupby('指數')
        # tempDF = pd.DataFrame([], columns = resJson['fields9'])
        tempDF = pd.DataFrame()
        print("endGroup")
        temp = group.get_group('發行量加權股價指數')
        tempDF = pd.concat([tempDF, temp], axis = 0)
        numpyDF = tempDF['收盤指數'].to_numpy()
        print(numpyDF)
        return numpyDF

    def chooseStock(self, x):
        arr = np.array(self.choosenStock)
        if x[1] in arr:
            return x

class Tools():
    @staticmethod
    def transform_date(date):   #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d


def parser_loader():
    parser = argparse.ArgumentParser(description = 'Stock Crawler')

    parser.add_argument('--initOrFill', type = str, default = 'fill')
    parser.add_argument('--choosenStock', nargs='+', type=int, default=[2330])
    parser.add_argument('--startDate', type=str, default = '2023-01-01')
    parser.add_argument('--endDate', type=str, default = 'now')
    parser.add_argument('--saveFileName', type=str, default = 'testStock')
    parser.add_argument('--queryType', type=str, default = 'listed')
    return parser

if __name__ == "__main__":  
    parser = parser_loader()
    args = vars(parser.parse_args())
    print(args)

    Stock(args)
