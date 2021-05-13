##########################################################################
# Name: gcm-dl.py
#
# Scraping "気象庁過去の気象データ検索"
#
# Usage:
#
# Author: Ryosuke Tomita
# Date: 2021/05/13
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
        self.UrlParse = urlparse(self.url)
