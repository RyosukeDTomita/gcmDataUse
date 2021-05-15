##########################################################################
# Name: citySearch.py
#
# fetch available cities list of selected Prefecture.
#
# Usage: python3 citySearch.py <県>
#
# Author: Ryosuke Tomita
# Date: 2021/05/11
##########################################################################

#-----module-----
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import sys

class setUrl:
    def __init__(self,value):
        self.Url = value
        self.UrlParse = urlparse(self.Url)
        self.html = urlopen(self.Url)
        self.bsObj = BeautifulSoup(self.html,'lxml')
        return None

class Area(setUrl):
    def fetchList(self):
        self.List = []
        self.NameList = []
        self.HrefList = []
        for htmlElement in self.bsObj.find("map", {"name":"point"}).findAll("area"):
            Name = htmlElement.attrs['alt']
            Href = htmlElement.attrs['href']
            self.NameList.append(Name)
            self.HrefList.append(Href)
            self.List.append({Name:Href})
        return self.List

    def renewUrl(self,value):
        self.Key = value
        self.frontUrl = "https://www.data.jma.go.jp/obd/stats/etrn/select/"
        if self.Key == "ALL":
            return self.Url

        self.NewUrl = ""
        for i in range(0,len(self.List),1):
            if self.Key in self.List[i].keys():
                self.NewUrl = (self.frontUrl + self.List[i][self.Key])
        if not self.NewUrl:
            return None
        else:
            return self.NewUrl

class City(Area):
    pass

#-----FUNCTION-----
def PrintArgs(dictionaries):
    keys=list(dictionaries.keys())
    values=list(dictionaries.values())
    for i in range (0,len(dictionaries),1):
        print(keys[i],'=',values[i])
    return None

def ErrorMessage():
    print("SelectedArea is not valid value.")
    print("Please see https://www.data.jma.go.jp/obd/stats/data/image/map/map00.png")
    print("ex: python3 citySearch.py 福島県")
    return None

def EraseDuplicate(List):
    List = list(set(list(List)))
    return List

def PrintCityList(AreaUrl):
    cityI = City(AreaUrl)
    cityList = cityI.fetchList()
    cityNameList = cityI.NameList
    cityNameList = EraseDuplicate(cityNameList)
    print("-----AREA =", areaI.Key,"-----")
    for i in range (0,len(cityNameList),1):
        if re.match('.*県',cityNameList[i]):
            continue
        else:
            print(cityNameList[i])
    return None
#-----MAIN-----
args = {}
args['SelectedArea'] = sys.argv[1]
PrintArgs(args)

startPageUrl = "https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view="

# area
areaI = Area(startPageUrl)
areaList = areaI.fetchList()
newUrl = areaI.renewUrl(args['SelectedArea'])

# search city
if   newUrl != None and args['SelectedArea'] != "ALL": #SelectedArea is prefecture name.
    PrintCityList(newUrl)
elif args['SelectedArea'] == "ALL": #SelectedArea is ALL
    areaKey = areaI.NameList
    areaKey = EraseDuplicate(areaKey)
    for n in range (0,len(areaKey),1):
        newUrl = areaI.renewUrl(areaKey[n])
        PrintCityList(newUrl)
elif newUrl == None:
    ErrorMessage()
