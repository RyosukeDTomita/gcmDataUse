#########################################################################
# Name: gcm-dl.py
#
# Download "気象庁過去の気象データ検索" data as csvfile (kishotyo_dl.py module version)
#
# Usage:
#    ```
#    import gcm_dl.py
#    gcm_dl.main("福島県","小名浜","2020","1","4")   #hourly data
#    gcm_dl.main("福島県","小名浜","2020","1",None)  #daily data
#    gcm_dl.main("福島県","小名浜","2020",None,None) #month data
#    gcm_dl.main("福島県","小名浜",None,None,None)   #yearly data
#    ```
#
# Author: Ryosuke Tomita
# Date: 2021/5/14
##########################################################################
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
            pass
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


#-----FUNCTIONS-----

def getViewPageUrl(args,prevUrl):
    global ObsSystem
    if   args['year'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/annually_s.php')
    elif args['year'] != None and args['month'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/monthly_s1.php')
    elif args['month'] != None and args['day'] == None:
        viewPageUrl = prevUrl.replace('index.php','view/daily_s1.php')
    elif args['day'] != None:
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

def noneCounter(args):
    noneCnt = 0
    for arg in args.values():
        if arg == None:
            noneCnt += 1
    return noneCnt


#-----MAIN-----
def main(prefecture,city,year,month,day):
    args = {}
    print(type(day))
    args['prefecture'] = prefecture
    args['city']       = city
    args['year']       = str(year)
    args['month']      = str(month)
    args['day']        = str(day)

    noneCnt = noneCounter(args)

    startPageUrl = "https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view="
    outName = ("../data/" + args['prefecture'] + args['city'])

    # PrefectureUrl
    prefectureI = ScrapePrefecture(startPageUrl)
    prefectureList = prefectureI.fetchList()
    newUrl = prefectureI.renewUrl(args['prefecture'])

    # cityUrl
    cityI = ScrapeCity(newUrl)
    cityList = cityI.fetchList()
    newUrl = cityI.renewUrl(args['city'])

    # yearUrl
    if noneCnt <= 2 :
        yearI = ScrapeYear(newUrl)
        yearList = yearI.fetchList()
        yearI.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/"
        newUrl = yearI.renewUrl(args['year'])
    else:
        pass

    # monthUrl
    if noneCnt <= 1 :
        monthI = ScrapeMonth(newUrl)
        newUrl = monthI.renewUrl(args['month'])
    else:
        pass

    # dayUrl
    if noneCnt == 0:
        dayI = ScrapeDay(newUrl)
        dayList = dayI.fetchList()
        dayI.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/"
        newUrl = dayI.renewUrl(args['day'])
    else:
        pass

    # get data from SelectedMonth page
    viewPageUrl = getViewPageUrl(args,newUrl)
    if   noneCnt == 3:
        outName += (".csv")
        viewI = ViewPageYear(viewPageUrl)
        gmaColumns = ["現地平均気圧 (hPa)","海面平均気圧 (hPa)","降水量合計 (mm)","最大日降水量 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均湿度 (%)","最小湿度 (%)","平均風速 (m/s)","最大風速 (m/s)","最大風速の風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","全天日射量 (MJ/M**2)","降雪合計 (cm)","降雪の日合計の最大 (cm)","最深積雪","雲量","雪日数","霧日数","雷日数"]
        amedasColumns = ["降水量合計 (mm)","降水量日最大 (mm)","1時間最大降水量 (mm)","10分間最大降水量","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均風速 (m/s)","最大風速 (m/s)","最大風速風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","降雪の合計 (cm)","日降雪の最大 (cm)","最深積雪 (cm)"]
        Columns = selectColumns(gmaColumns,amedasColumns)
        df = saveCsv(viewI,Columns)
    elif noneCnt == 2:
        outName += (args['year'] + ".csv")
        viewI = ViewPageMonth(viewPageUrl)
        gmaColumns = ["現地平均気圧 (hPa)","海面平均気圧 (hPa)","降水量合計 (mm)","最大日降水量 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均湿度 (%)","最小湿度 (%)","平均風速 (m/s)","最大風速 (m/s)","最大風速の風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","全天日射量 (MJ/M**2)","降雪合計 (cm)","降雪の日合計の最大 (cm)","最深積雪","雲量","雪日数","霧日数","雷日数"]
        amedasColumns = ["降水量合計 (mm)","降水量日最大 (mm)","1時間最大降水量 (mm)","10分間最大降水量 (mm)","日平均気温","日最高気温","日最低気温","最高気温","最低気温","平均風速 (m/s)","最大風速 (m/s)","最大風速風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","降雪の合計 (cm)","日降雪の最大 (cm)","最深積雪 (cm)"]
        Columns = selectColumns(gmaColumns,amedasColumns)
        df = saveCsv(viewI,Columns)
    elif noneCnt == 1:
        outName += (args['year'] + "_" + args['month'] + ".csv")
        viewI = ViewPageDay(viewPageUrl)
        gmaColumns = ["現地平均気圧 (hPa)","海面平均気圧 (hPa)","降水量合計 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","平均気温","最高気温","最低気温","日平均湿度 (%)","最小湿度 (%)","平均風速 (m/s)","最大風速 (m/s)","最大風速の風向","最大瞬間風速 (m/s)","最大瞬間風速風向","日照時間 (h)","降雪合計 (cm)","最深積雪","天気概況昼","天気概況夜"]
        amedasColumns = ["降水量合計 (mm)","最大1時間降水量 (mm)","最大10分間降水量 (mm)","平均気温","最高気温","最低気温","平均風速 (m/s)","最大風速 (m/s)","最大風向","最大瞬間風速 (m/s)","最大瞬間風速風向","最多風向","日照時間 (h)","降雪合計 (cm)","最深積雪 (cm)"]
        Columns = selectColumns(gmaColumns,amedasColumns)
        df = saveCsv(viewI,Columns)
    elif noneCnt == 0:
        outName += (args['year'] + "_" + args['month']+ "_" + args['day'] + ".csv")
        viewI = ViewPageHour(viewPageUrl)
        gmaColumns = ["現地気圧 (hPa)","海面気圧 (hPa)","降水量 (mm)","気温","露天温度","蒸気圧 (hPa)","湿度 (%)","風速 (m/s)","風向","日照時間 (h)","全天日射量 (MJ/m**2)","降雪 (cm)","積雪 (cm)","天気","雲量","視程 (km)"]
        amedasColumns = ["降水量 (mm)","気温","風速 (m/s)","風向","日照時間 (h)","降雪 (cm)","積雪 (cm)"]
        Columns = selectColumns(gmaColumns,amedasColumns)
        df = saveCsv(viewI,Columns)
    df.to_csv(outName,header=True,index=True)
    return None
