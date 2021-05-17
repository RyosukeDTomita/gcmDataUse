##########################################################################
# Name: readcsv.py
#
# Read CSV Data downloaded by kishotyo_dl.py
#
# Usage: 
#
# Author: Ryosuke Tomita
# Date: 2021/05/12
##########################################################################
import pandas as pd

class readcsv:
    def __init__(self,csvfile):
        self.csvfile = csvfile
        self.df = pd.read_csv(self.csvfile,header=0,index_col=0)
        return None
    def __getattr__(self,attrName):
        if   attrName == "df":
            return self.df
        elif attrName == "index":
            return self.df.index
        elif attrName == "columns":
            return self.df.columns
    def __getitem__(self,Header):
        self.header = Header
        self.selectedColumn = self.df.loc[:,Header]
        return self.selectedColumn
    def headerShow(self):
        for Header in self.df.columns:
            print(Header)
        return self.df.columns
