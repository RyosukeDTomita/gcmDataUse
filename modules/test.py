from readcsv import readcsv
import re
csvfile = "../sampleCsv/福島県小名浜.csv"
pattern = re.compile('.*\]$')
Data = readcsv(csvfile)
print(Data.columns)

for i in Data.columuns:

