#########################################################################
# Name: kishotyo_dl.py
#
# Download "気象庁過去の気象データ検索" data as csvfile
#
# Usage: python3 kishotyo_dl.py <県名> <市> <年> <月> <日>
# ex: python3 kishotyo_dl.py 福島県 小名浜 2020 1 4
#    It is available to skip <月> <日>
#
# Author: Ryosuke Tomita
# Date: 2021/5/6
##########################################################################

#-----module-----
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import sys


class setUrl:
    def __init__(self,value):
        self.Url = value
        self.UrlParse = urlparse(self.Url)
        self.html = urlopen(self.Url)
        self.bsObj = BeautifulSoup(self.html,'lxml')
        return None

class Area(setUrl):
    def getList(self):
        self.areaList = []
        for areas in self.bsObj.find("map", {"name":"point"}).findAll("area"):
            areaName = areas.attrs['alt']
            areaHref = areas.attrs['href']
            self.areaList.append({areaName:areaHref})
        return self.areaList

    def renewUrl(self,value):
        self.areaKey = value
        self.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/select/"
        for i in range(0,len(self.areaList),1):
            if self.areaKey in self.areaList[i].keys():
                self.NewUrl = (self.frontUrl + self.areaList[i][self.areaKey])
        return self.NewUrl

class City(Area):
    pass

class Year(setUrl):
    def getList(self):
        self.yearList = []
        for year in self.bsObj.find("td", {"class":"nwtop"}).findAll("a"):
            yearValue = year.get_text()[0:4] #erase 年
            year_href = year.attrs['href']
            self.yearList.append({yearValue:year_href})
        return self.yearList

    def renewUrl(self,value):
        self.year = value
        self.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/"
        for i in range(0,len(self.yearList),1):
            if self.year in self.yearList[i].keys():
                self.NewUrl = (self.frontUrl + self.yearList[i][self.year])
        return self.NewUrl

class Month(setUrl):
    def renewUrl(self,value):
        self.month = int(value)
        monthList = np.arange(1,13,1)
        if self.month in monthList:
            self.NewUrl = (self.Url).replace("month=",("month=" + str(self.month)))
        else:
            print("SelectedMonth is not valid value")
        return self.NewUrl


class Day(setUrl):
    def getList(self):
        self.dayList = []
        for day in self.bsObj.findAll("a",{"href":re.compile(".*day=.+&")}):
            dayValue = day.get_text()[:-1] #erase 日
            day_href = day.attrs['href']
            self.dayList.append({dayValue:day_href})
        return self.dayList
    def renewUrl(self,value):
        self.day = value
        self.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/"
        for i in range(0,len(self.dayList),1):
            if self.day in self.dayList[i].keys():
                self.NewUrl = (self.frontUrl + self.dayList[i][self.day])
        return self.NewUrl

class Viewing(setUrl):
    def viewPageYear(self):
        self.columns = ["現地年平均気圧 (hPa)","海面年平均気圧 (hPa)","年降水量合計 (mm)","最大日降水量 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","日平均気温","日最高気温","日最低気温","年最高気温","年最低気温","年平均湿度 (%)","年最小湿度 (%)","年平均風速 (m/s)","年最大風速 (m/s)","年最大風速の風向","年最大瞬間風速 (m/s)","年最大瞬間風速風向","日照時間 (h)","全天日射量 (MJ/M**2)","降雪合計 (cm)","降雪の日合計の最大 (cm)","最深積雪","雲量","雪日数","霧日数","雷日数"]
        # get year from webpage
        self.years = []
        for year in self.bsObj.find("table",{"id":"tablefix1"}).findAll("a"):
            self.years.append(int(year.get_text()))
        # get data from webpage
        self.datas = []
        for data in self.bsObj.find("table",{"id":"tablefix1"}).findAll("td",{"class":re.compile('data.*')}):
            try:
                dataConv = float(data.get_text())
            except ValueError:
                dataConv = data.get_text()
            self.datas.append(dataConv)
        # create DataFrame
        self.datas = np.array(self.datas).reshape(len(self.years),len(self.columns)).tolist()
        self.df = pd.DataFrame(data=self.datas,index=self.years,columns=self.columns)
        return self.df
    def viewPageMonth(self):
        self.columns = ["現地月平均気圧 (hPa)","海面月平均気圧 (hPa)","月降水量合計 (mm)","最大1日間降水量 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","日平均気温","日最高気温","日最低気温","月最高気温","月最低気温","月平均湿度 (%)","月最小湿度 (%)","月平均風速 (m/s)","月最大風速 (m/s)","月最大風速の風向","月最大瞬間風速 (m/s)","月最大瞬間風速風向","日照時間 (h)","全天日射量 (MJ/m**2)","降雪合計 (cm)","1日の降雪合計の最大 (cm)","最深積雪 (cm)","雲量","雪日数","霧日数","雷日数"]

        # get Month from webpage
        self.months = []
        for month in self.bsObj.find("table",{"id":"tablefix1"}).findAll("a"):
            self.months.append(int(month.get_text()))
        # get data from webpage
        self.datas = []
        for data in self.bsObj.find("table",{"id":"tablefix1"}).findAll("td",{"class":"data_0_0"}):
            try:
                dataConv = float(data.get_text())
            except ValueError:
                dataConv = data.get_text()
            self.datas.append(dataConv)
        # create DataFrame
        self.datas = np.array(self.datas).reshape(len(self.months),len(self.columns)).tolist()
        self.df = pd.DataFrame(data=self.datas,index=self.months,columns=self.columns)
        return self.df

    def viewPageDay(self):
        self.columns = ["現地日平均気圧 (hPa)","海面日平均気圧 (hPa)","日降水量合計 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","日平均気温","日最高気温","日最低気温","日平均湿度 (%)","日最小湿度 (%)","日平均風速 (m/s)","日最大風速 (m/s)","日最大風速の風向","日最大瞬間風速 (m/s)","日最大瞬間風速風向","日照時間 (h)","降雪合計 (cm)","最深積雪","天気概況昼","天気概況夜"]
        # get Day from webpage
        self.days = []
        for day in self.bsObj.find("table",{"id":"tablefix1"}).findAll("a"):
            self.days.append(int(day.get_text()))
        # get data from webpage
        self.datas = []
        for data in self.bsObj.find("table",{"id":"tablefix1"}).findAll("td",{"class":"data_0_0"}):
            try:
                dataConv = float(data.get_text())
            except ValueError:
                dataConv = data.get_text()
            self.datas.append(dataConv)

        # create DataFrame
        self.datas = np.array(self.datas).reshape(len(self.days),len(self.columns)).tolist()
        self.df = pd.DataFrame(data=self.datas,index=self.days,columns=self.columns)
        return self.df

    def viewPageHour(self):
        self.hour = np.arange(1,25,1) # 1~24
        self.columns = ["現地気圧 (hPa)","海面気圧 (hPa)","降水量 (mm)","気温 (℃)","露天温度 (℃)","蒸気圧 (hPa)","湿度 (%)","風速 (m/s)","風向","日照時間 (h)","全天日射量 (MJ/m**2)","降雪 (cm)","積雪 (cm)","天気","雲量","視程 (km)"]
        self.datas = []
        for data in self.bsObj.find("table",{"id":"tablefix1"}).findAll("td",{"class":"data_0_0"}):
            try:
                dataConv = float(data.get_text())
            except ValueError:
                dataConv = data.get_text()
            self.datas.append(dataConv)

        # create DataFrame
        self.datas = np.array(self.datas).reshape(len(self.hour),len(self.columns)).tolist()
        self.df = pd.DataFrame(data=self.datas,index=self.hour,columns=self.columns)
        return self.df

#-----FUNCTION-----
def PrintArgs(dictionaries):
    keys=list(dictionaries.keys())
    values=list(dictionaries.values())
    for i in range (0,len(dictionaries),1):
        print(keys[i],'=',values[i])
    return None

def getViewPageUrl(prevUrl):
    if   args['SelectedYear'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/annually_s.php')
    elif args['SelectedYear'] != None and args['SelectedMonth'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/monthly_s1.php')
    elif args['SelectedMonth'] != None and args['SelectedDay'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/daily_s1.php')
    elif args['SelectedDay'] != None:
        viewPageUrl = prevUrl.replace('index.php','view/hourly_s1.php')
    return viewPageUrl


#-----MAIN-----
# get arguments
args = {}
args['SelectedArea'] = sys.argv[1]
args['SelectedCity'] = sys.argv[2]
try:
    args['SelectedYear'] = sys.argv[3]
except IndexError:
    args['SelectedYear'] = None
try:
    args['SelectedMonth'] = sys.argv[4]
except IndexError:
    args['SelectedMonth'] = None
try:
    args['SelectedDay'] = sys.argv[5]
except IndexError:
    args['SelectedDay'] = None

PrintArgs(args)
noneCounter = (list(args.values()).count(None)) #args empty numer

startPageUrl = "https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view="
outputName = (args['SelectedArea'] + args['SelectedCity'])
# area
areaI = Area(startPageUrl)
areaList = areaI.getList()
newUrl = areaI.renewUrl(args['SelectedArea'])

# city
cityI = City(newUrl)
cityList = cityI.getList()
newUrl = cityI.renewUrl(args['SelectedCity'])

# year
if noneCounter <= 2 :
    yearI = Year(newUrl)
    yearList = yearI.getList()
    newUrl = yearI.renewUrl(args['SelectedYear'])
else:
    pass
# month
if noneCounter <= 1 :
    monthI = Month(newUrl)
    newUrl = monthI.renewUrl(args['SelectedMonth'])
else:
    pass
# day
if noneCounter == 0:
    dayI = Day(newUrl)
    dayList = dayI.getList()
    newUrl = dayI.renewUrl(args['SelectedDay'])
else:
    pass

# get data from SelectedMonth page
viewPageUrl = getViewPageUrl(newUrl)
viewing = Viewing(viewPageUrl)
if   noneCounter == 3:
    df = viewing.viewPageYear()
    outputName += (".csv")
elif noneCounter == 2:
    df = viewing.viewPageMonth()
    outputName += (args['SelectedYear'] + ".csv")
elif noneCounter == 1:
    df = viewing.viewPageDay()
    outputName += (args['SelectedYear'] + "_" + args['SelectedMonth'] + ".csv")
elif noneCounter == 0:
    df = viewing.viewPageHour()
    outputName += (args['SelectedYear'] + "_" + args['SelectedMonth']+ "_" + args['SelectedDay'] + ".csv")
df.to_csv(outputName)
