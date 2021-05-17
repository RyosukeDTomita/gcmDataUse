import sys
def getoutname(year,month,day):
    if   year == None:
        csvname = (prefecture + city + ".csv")
    elif year != None and month == None:
        csvname = (prefecture + city + "_" + year + ".csv")
    elif month != None and day == None:
        csvname = (prefecture + city + "_" + year + "_" + month + ".csv")
    elif day != None:
        csvname = (prefecture + city + "_" + year + "_" + month + "_" + day + ".csv")
    return csvname

prefecture = "福島県"
city = "小名浜"
year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]
csvname = getoutname(year,month,day)
print(csvname)
