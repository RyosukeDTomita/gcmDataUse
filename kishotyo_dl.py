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
    def __init__(self,url):
        self.Url = url
        self.UrlParse = urlparse(self.Url)
        self.html = urlopen(self.Url)
        self.bsObj = BeautifulSoup(self.html,'lxml')
        self.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/select/"
        return None


class Scraping(setUrl):
    def fetchList(self):
        self.List = []
        for htmlElement in self.bsObj.find("map", {"name":"point"}).findAll("area"):
            Name = htmlElement.attrs['alt']
            Href = htmlElement.attrs['href']
            self.List.append({Name:Href}) # "List" is consisted of dictionary.
        return self.List

    def renewUrl(self,Key):
        self.Key = Key
        for i in range(0,len(self.List),1):
            if self.Key in self.List[i].keys():
                self.NewUrl = (self.frontUrl + self.List[i][self.Key])
        return self.NewUrl


class ScrapePrefecture(Scraping):
    pass


class ScrapeCity(Scraping):
    pass


class ScrapeYear(Scraping):
    def fetchList(self):
        self.List = []
        for htmlElement in self.bsObj.find("td", {"class":"nwtop"}).findAll("a"):
            Number = htmlElement.get_text()[0:4] #erase 年
            Href = htmlElement.attrs['href']
            self.List.append({Number:Href})
        return self.List


class ScrapeMonth(setUrl):
    def renewUrl(self,value):
        self.month = int(value)
        self.monthList = np.arange(1,13,1)
        if self.month in self.monthList:
            self.NewUrl = (self.Url).replace("month=",("month=" + str(self.month)))
        else:
            print("SelectedMonth is not valid value")
        return self.NewUrl


class ScrapeDay(Scraping):
    def fetchList(self):
        self.List = []
        for htmlElement in self.bsObj.findAll("a",{"href":re.compile(".*day=.+&")}): # The values with red line and with "]" also are include.
            Number = htmlElement.get_text()[:-1] #erase 日
            Href = htmlElement.attrs['href']
            self.List.append({Number:Href})
        return self.List


class ViewPageYear(setUrl):
    def fetchIndex(self):
        self.index = []
        for Index in self.bsObj.find("table",{"id":"tablefix1"}).findAll("a"):
            self.index.append(int(Index.get_text()))
        return self.index

    def fetchData(self):
        self.datas = []
        for data in self.bsObj.find("table",{"id":"tablefix1"}).findAll("td",{"class":re.compile('data.*')}):
            try:
                dataValue = float(data.get_text())
            except ValueError:
                dataValue = data.get_text()
                if dataValue in ["--","///","#"]:
                    dataValue = ""
            self.datas.append(dataValue)
        return self.datas
    def MakeDataFrame(self):
        self.datas = np.array(self.datas).reshape(len(self.index),len(self.columns)).tolist()
        self.df = pd.DataFrame(data=self.datas,index=self.index,columns=self.columns)
        return self.df

class ViewPageMonth(ViewPageYear):
    def fetchIndex(self):
        self.index = []
        for Index in self.bsObj.find("table",{"id":"tablefix1"}).findAll("a"):
            self.index.append(int(Index.get_text()))
        return self.index
    def fetchData(self):
        self.datas = []
        for data in self.bsObj.find("table",{"id":"tablefix1"}).findAll("td",{"class":"data_0_0"}):
            try:
                dataValue = float(data.get_text())
            except ValueError:
                dataValue = data.get_text()
                if dataValue in ["--","///","#"]:
                    dataValue = ""
            self.datas.append(dataValue)
        return self.datas


class ViewPageDay(ViewPageMonth):
    pass

class ViewPageHour(ViewPageYear):
    def fetchIndex(self):
        self.index = np.arange(1,25,1) # 1~24時
        return self.index


#-----FUNCTION-----
def PrintArgs(dictionaries):
    keys=list(dictionaries.keys())
    values=list(dictionaries.values())
    for i in range (0,len(dictionaries),1):
        print(keys[i],'=',values[i])
    return None

def getViewPageUrl(prevUrl):
    global ObsSystem
    if   args['SelectedYear'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/annually_s.php')
    elif args['SelectedYear'] != None and args['SelectedMonth'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/monthly_s1.php')
    elif args['SelectedMonth'] != None and args['SelectedDay'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/daily_s1.php')
    elif args['SelectedDay'] != None:
        viewPageUrl = prevUrl.replace('index.php','view/hourly_s1.php')
    testUrl = setUrl(viewPageUrl)
    try:
        testUrl.bsObj.find("table",{"id":"tablefix1"}).findAll("a")
        ObsSystem = "GMA"
    except AttributeError:
        viewPageUrl = viewPageUrl.replace('_s','_a')
        ObsSystem = "AMEDaS"
    return viewPageUrl

def selectColumns(gmaColumns,amedasColumns):
    if   ObsSystem == "GMA":
        return gmaColumns
    elif ObsSystem == "AMEDaS":
        return amedasColumns
    else:
        return None

def saveCsv(Instance,Columns):
    Index = Instance.fetchIndex()
    Data = Instance.fetchData()
    Instance.columns = Columns
    df = Instance.MakeDataFrame()
    return df


#-----MAIN-----
# get arguments
args = {}
args['SelectedPrefecture'] = sys.argv[1]
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
outName = (args['SelectedPrefecture'] + args['SelectedCity'])

# PrefectureUrl
prefectureI = ScrapePrefecture(startPageUrl)
prefectureList = prefectureI.fetchList()
newUrl = prefectureI.renewUrl(args['SelectedPrefecture'])

# cityUrl
cityI = ScrapeCity(newUrl)
cityList = cityI.fetchList()
newUrl = cityI.renewUrl(args['SelectedCity'])

# yearUrl
if noneCounter <= 2 :
    yearI = ScrapeYear(newUrl)
    yearList = yearI.fetchList()
    yearI.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/"
    newUrl = yearI.renewUrl(args['SelectedYear'])
else:
    pass

# monthUrl
if noneCounter <= 1 :
    monthI = ScrapeMonth(newUrl)
    newUrl = monthI.renewUrl(args['SelectedMonth'])
else:
    pass

# dayUrl
if noneCounter == 0:
    dayI = ScrapeDay(newUrl)
    dayList = dayI.fetchList()
    dayI.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/"
    newUrl = dayI.renewUrl(args['SelectedDay'])
else:
    pass

# get data from SelectedMonth page
viewPageUrl = getViewPageUrl(newUrl)
print(viewPageUrl)
if   noneCounter == 3:
    outName += (".csv")
    viewI = ViewPageYear(viewPageUrl)
    gmaColumns = ["現地平均気圧 (hPa)","海面平均気圧 (hPa)","降水量合計 (mm)","最大日降水量 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均湿度 (%)","最小湿度 (%)","平均風速 (m/s)","最大風速 (m/s)","最大風速の風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","全天日射量 (MJ/M**2)","降雪合計 (cm)","降雪の日合計の最大 (cm)","最深積雪","雲量","雪日数","霧日数","雷日数"]
    amedasColumns = ["降水量合計 (mm)","降水量日最大 (mm)","1時間最大降水量 (mm)","10分間最大降水量","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均風速 (m/s)","最大風速 (m/s)","最大風速風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","降雪の合計 (cm)","日降雪の最大 (cm)","最深積雪 (cm)"]
    Columns = selectColumns(gmaColumns,amedasColumns)
    df = saveCsv(viewI,Columns)
elif noneCounter == 2:
    outName += (args['SelectedYear'] + ".csv")
    viewI = ViewPageMonth(viewPageUrl)
    gmaColumns = ["現地平均気圧 (hPa)","海面平均気圧 (hPa)","降水量合計 (mm)","最大日降水量 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均湿度 (%)","最小湿度 (%)","平均風速 (m/s)","最大風速 (m/s)","最大風速の風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","全天日射量 (MJ/M**2)","降雪合計 (cm)","降雪の日合計の最大 (cm)","最深積雪","雲量","雪日数","霧日数","雷日数"]
    amedasColumns = ["降水量合計 (mm)","降水量日最大 (mm)","1時間最大降水量 (mm)","10分間最大降水量 (mm)","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均風速 (m/s)","最大風速 (m/s)","最大風速風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","降雪の合計 (cm)","日降雪の最大 (cm)","最深積雪 (cm)"]
    Columns = selectColumns(gmaColumns,amedasColumns)
    df = saveCsv(viewI,Columns)
elif noneCounter == 1:
    outName += (args['SelectedYear'] + "_" + args['SelectedMonth'] + ".csv")
    viewI = ViewPageDay(viewPageUrl)
    gmaColumns = ["現地平均気圧 (hPa)","海面平均気圧 (hPa)","降水量合計 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","平均気温","最高気温","最低気温","日平均湿度 (%)","最小湿度 (%)","平均風速 (m/s)","最大風速 (m/s)","最大風速の風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","降雪合計 (cm)","最深積雪","天気概況昼","天気概況夜"]
    amedasColumns = ["降水量合計 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","平均気温","最高気温","最低気温","平均風速 (m/s)","最大風速 (m/s)","最大風向","最大瞬間風速 (m/s)","最大瞬間風速風向","最多風向","日照時間 (h)","降雪合計 (cm)","最深積雪 (cm)"]
    Columns = selectColumns(gmaColumns,amedasColumns)
    df = saveCsv(viewI,Columns)
elif noneCounter == 0:
    outName += (args['SelectedYear'] + "_" + args['SelectedMonth']+ "_" + args['SelectedDay'] + ".csv")
    viewI = ViewPageHour(viewPageUrl)
    gmaColumns = ["現地気圧 (hPa)","海面気圧 (hPa)","降水量 (mm)","気温","露天温度","蒸気圧 (hPa)","湿度 (%)","風速 (m/s)","風向","日照時間 (h)","全天日射量 (MJ/m**2)","降雪 (cm)","積雪 (cm)","天気","雲量","視程 (km)"]
    amedasColumns = ["降水量 (mm)","気温","風速 (m/s)","風向","日照時間 (h)","降雪 (cm)","積雪 (cm)"]
    Columns = selectColumns(gmaColumns,amedasColumns)
    df = saveCsv(viewI,Columns)
df.to_csv(outName,header=True,index=True)
