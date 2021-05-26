#########################################################################
# Name: main.py
#
# ScrapeData from https://www.data.jma.go.jp/obd/stats/etrn/index.php and make a graph
#
# Usage: python3 main.py <year> <month> <day> <headerKey> <previousN>
#
# Author: Ryosuke Tomita
# Date: 2021/05/12
#########################################################################
import os
import sys
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
    if   year == "None":
        csvName = (prefecture + city + ".csv")
    elif year != "None" and month == "None" :
        csvName = (prefecture + city + year + ".csv")
    elif month != "None" and day == "None":
        csvName = (prefecture + city + year + "_" + month + ".csv")
    elif day != "None":
        csvName = (prefecture + city + year + "_" + month + "_" + day + ".csv")
    return csvName
#-------parameter setting-------
HOME = os.getenv("HOME")
dataDir = os.path.join(HOME + "/jmaDataUse/data")
figDir = os.path.join(HOME + "/jmaDataUse/modules/fig")
PWD = os.getcwd()
year  = sys.argv[1]
month = sys.argv[2]
day   = sys.argv[3]
headerKey = sys.argv[4]
#previousN = sys.argv[5]
#if previousN > 5:
#    print("previousN is larger than expected")
#elif previousN == "":
#    previousN == 0
jp = fontjp()


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
            continue
        else:
            print(csvName)
            jma_dl.main(prefecture,city,year,month,day)
#-------read csv file-------
            csvFile = os.path.join(HOME + "/jmaDataUse/data/" + csvName)
            label = getLabelName(csvFile)
            Data = readcsv(csvFile)
#            Data.headerShow()
            x = Data.index
            #y = Data["現地平均気圧 (hPa)"]
            try:
                y = Data[headerKey]
            except KeyError:
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
            os.chdir(PWD)
