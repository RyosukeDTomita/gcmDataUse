#########################################################################
# Name: main.py
#
# ScrapeData from https://www.data.jma.go.jp/obd/stats/etrn/index.php and make a graph
#
# Usage: python3 main.py
#
# Author: Ryosuke Tomita
# Date: 2021/05/12
#########################################################################
import os
import sys
import re
# created by user
from readcsv import readcsv
from myMatlib import *
from matplotlib.ticker import MaxNLocator

#-------FUNCTION-------
def getLabelName(csvfile):
    matchObj = re.search('1|2.*[0-9]',str(csvfile))
    return matchObj.group()

#-------parameter setting-------
HOME = os.getenv("HOME")
dataDir = os.path.join(HOME + "/" + "kishotyo_kakonodatakensaku")
csvfile = os.path.join(dataDir + "/" + "sampleCsv/福島県小名浜2020.csv")
label = getLabelName(csvfile)
jp = fontjp()
#-------read csv file-------
Data = readcsv(csvfile)
#Data.headerShow()
x = Data.index
print(x)
y = Data["現地平均気圧 (hPa)"]
print(y)

#-------graph-------
grapher = pltSet()
fig = grapher.fig
ax = grapher.ax



ax.plot(x,y,marker='.',
        markersize=10,
        markeredgewidth=1.,
        markeredgecolor="k",
        label= label,
        color="b",
        linestyle="solid"
        )
ax.xaxis.set_major_locator(MaxNLocator(integer=True)) #x axis is integer
ax.set_xlabel("test",fontsize=20,fontproperties=jp())
ax.set_ylabel(Data.header,fontsize=20,fontproperties=jp())

# grid setting↲
plt.grid(b=True,which='major',
         color='gray',linestyle='-',alpha=0.2)
plt.grid(b=True,which='minor',
         color='#999999',linestyle='-',alpha=0.2)
linestyle=["hoge","solid","dashed","dashdot","dotted"]
plotcolor=["hoge","b","g","o","r"]
ax.legend(ncol=2, bbox_to_anchor=(0.,1.02, 1., 0.102),loc=3)
fig.savefig("test",bbox_inches="tight",pad_inches=0.5)
