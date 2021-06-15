#########################################################################
# Name: main2.py
#
# ScrapeData from https://www.data.jma.go.jp/obd/stats/etrn/index.php and make a graph
#
# Usage: python3 main.py -y|--year <year> -m|--month <month> -d|--day <day> -k|--headerkey <headerKey> <previousN>
#
# Author: Ryosuke Tomita
# Date: 2021/05/12
#########################################################################
import os
import argparse
import re
from matplotlib.ticker import MaxNLocator
# created by user
from readcsv import readcsv
from myMatlib import *
import jma_dl


#-------FUNCTION-------
def getLabelName(csvName):
    matchObj = re.search('1|2.*[0-9]',str(csvName))
    return matchObj.group()

def getCsvName(year,month,day):
    if   year == None:
        csvName = (prefecture + city + ".csv")
    elif year != None and month == None :
        csvName = (prefecture + city + year + ".csv")
    elif month != None and day == None:
        csvName = (prefecture + city + year + "_" + month + ".csv")
    elif day != None:
        csvName = (prefecture + city + year + "_" + month + "_" + day + ".csv")
    return csvName
#-------parameter setting-------
HOME = os.getenv("HOME")
dataDir = os.path.join(HOME + "/jmaDataUse/data")
figDir = os.path.join(HOME + "/jmaDataUse/modules/fig")
PWD = os.getcwd()
jp = fontjp()

#-------parser setting-------
parser = argparse.ArgumentParser()
parser.add_argument("-y","--year",help="Select target year",type=str)
parser.add_argument("-m","--month",help="Select target month",type=str)
parser.add_argument("-d","--day",help="Select target day",type=str)
parser.add_argument("-k","--headerkey",help="From your data(.csv) has header. You can chose one. ex: python3 main2.py -y 2020 -k 現地平均気圧 (hPa)",type=str)
args = parser.parse_args()
year = args.year
month = args.month
day = args.day
headerKey = args.headerkey


#-------download csv data
prefectureI = jma_dl.ScrapePrefecture("https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view=")
prefectureList = prefectureI.fetchList()
for prefecture in prefectureList:
    newUrl = prefectureI.renewUrl(prefecture)
    cityI = jma_dl.ScrapeCity(newUrl)
    cityList = cityI.fetchList()
    for city in cityList:
        csvName = getCsvName(year,month,day)
        if os.path.isfile(csvName):
            print(csvName , " is already exist! Skip download data.")
            #continue
        else:
            print("Downloading ", csvName)
            jma_dl.main(prefecture,city,year,month,day)
#-------read csv file-------
            csvFile = os.path.join(HOME + "/jmaDataUse/data/" + csvName)
            label = getLabelName(csvFile)
            Data = readcsv(csvFile)
            x = Data.index
            try:
                y = Data[headerKey]
            except KeyError:
                print(headerKey, " is not exist!")
                continue #headerKey is not found.

#-------graph-------
            grapher = pltSet()
            fig = grapher.fig
            ax = grapher.ax

            linestyle=["hoge","solid","dashed","dashdot","dotted"]
            plotcolor=["hoge","b","g","o","r"]


            ax.plot(x,y,marker='.',
                    markersize=10,
                    markeredgewidth=1.,
                    markeredgecolor="k",
                    label= label,
                    color="b",
                    linestyle="solid")
            ax.xaxis.set_major_locator(MaxNLocator(integer=True)) #x axis is integer
            ax.set_xlabel(getLabelName(csvName),
                        fontsize=20,
                        fontproperties=jp())
            ax.set_ylabel(Data.header,
                        fontsize=20,
                        fontproperties=jp())

# grid setting
            plt.grid(b=True,
                    which='major',
                    color='gray',
                    linestyle='-',
                    alpha=0.2)
            plt.grid(b=True,
                    which='minor',
                    color='#999999',
                    linestyle='-',
                    alpha=0.2)
            ax.legend(ncol=2, bbox_to_anchor=(0.,1.02, 1., 0.102),loc=3)
            figName = csvName.replace(".csv","")
            os.chdir(figDir)
            fig.savefig(figName,bbox_inches="tight",pad_inches=0.5)
            print("figName")
            os.chdir(PWD)
