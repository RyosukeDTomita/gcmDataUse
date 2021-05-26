# modules/
## 注意点
[気象庁の過去の気象データ検索](https://www.data.jma.go.jp/obd/stats/etrn/index.php)では、**アメダスと気象台の2種類のデータ形式**が混在しており、地点によって得られるデータが異なります。
本スクリプトでは、ヘッダーの長さの違いによって判別していますが、データ形式によって指定できる物理量が異なる場合があります。

|              |        |
|--------------|--------|
|地点          |形式    |
|福島県小名浜市|気象台  |
|福島県平市    |アメダス|
******


## 必要なライブラリ
- beautifulsoup4
- pandas
- numpy
- sys
- re

anacondaを使う場合には以下でインストールできます。他のものはデフォルトでanacondaに入っていると思います。

```shell
#how to install nessesary libraries with anaconda
conda install beautifulsoup4
conda install pandas
conda install numpy
```
******


## [jma_dl.py](https://github.com/RyosukeDTomita/jmaDataUse/blob/master/modules/jma_dl.py)
指定した条件でデータをスクレイピングし、csv形式で保存します。
指定できる県名や市町村は以下の図をご覧ください。
保存されるデータの名前は **<県名><市名><年>_<月>_<日>.csv**に設定されています。(プログラム実行時に指定しなかった引数は省略されます。)
ダウンロードできるデータのサンプルは同リポジトリ内の[sampleCsv](https://github.com/RyosukeDTomita/jmaDataUse/tree/master/sampleCsv)をご覧ください。

```python3
import jma_dl.py
jma_dl.main("福島県","小名浜",2020,1,4)         #hourly data
jma_dl.main("福島県","小名浜",2020,1,None)      #daily data
jma_dl.main("福島県","小名浜",2020,None,None)   #month data
jma_dl.main("福島県","小名浜",None,None,None)   #yearly data
```
![指定できる県名](https://www.data.jma.go.jp/obd/stats/data/image/map/map00.png "指定できる県名")
指定できる市町村は、[気象庁の過去の気象データ検索](https://www.data.jma.go.jp/obd/stats/etrn/index.php)から検索するか、追記するcitySearch.pyを使用してください。
![市町村の例](https://www.data.jma.go.jp/obd/stats/data/image/map/map36.png "市町村選択ページ例")

地図で赤くプロットされている市町村のデータは気象台で観測されていますが、青と緑でプロットされた市町村はアメダスで観測されたデータです。これらはcsvのヘッダーが異なる点にご注意ください。

また、jma_dl.pyを使って指定できる県や市町村を検索するのに使用できます。

```python3
>>> import jma_dl
>>> startPageUrl = "https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view="
>>> prefectureI = jma_dl.ScrapePrefecture(startPageUrl)
>>> prefectureI.fetchList() #使用できる県のリストを表示
['茨城県', '長崎県', '岐阜県', '和歌山県', '福岡県', '静岡県', '石狩地方', '新潟県', '秋田県', '広島県', '山形県', '留萌地方', '島根県', '佐賀県', '大分県', '沖縄県', '十勝地方', '福井県', '高知県', '愛媛県', '山口県', '石川県', '網走・北見・紋別地方', '愛知県', '根室地方', '胆振地方', '釧路地方', '福島県', '岩手県', '長野県', '鳥取県', '宗谷地方', '徳島県', '東京都', '香川県', '三重県', '渡島地方', '兵庫県', '埼玉県', '千葉県', '南極', '青森県', '栃木県', '宮崎県', '京都府', '空知地方', '後志地方', '宮城県', '檜山地方', '滋賀県', '熊本県', '群馬県', '神奈川県', '大阪府', '富山県', '上川地方', '岡山県', '日高地方', '鹿児島県', '山梨県', '奈良県']
>>> newUrl = prefectureI.renewUrl('茨城県') #茨城県をスクレイピングするために、茨城県のデータがあるページのリンクを取得
>>> print(newUrl)
https://www.data.jma.go.jp/obd/stats/etrn/select/prefecture.php?prec_no=40&block_no=&year=&month=&day=&view=

>>> cityI = jma_dl.ScrapeCity(newUrl)
>>> cityI.fetchList() #使用できる市のリスト
['常総', '日立', '愛宕山', '大能', '鉾田', '門井', '古河', '筑波山', '水戸', '美野里', '笠間', '下館', '北茨城', '鹿嶋', 'つくば（館野）', '常陸大宮', '大子', '江戸崎', '徳田', '坂東', '土浦', '神峰山', '龍ケ崎', '花園', '下妻', '中野', '高萩', '柿岡']
```
## [readcsv.py](https://github.com/RyosukeDTomita/jmaDataUse/blob/master/modules/readcsv.py)

ダウンロードしたcsvファイルを処理するのに使います。

```python3
>>> from readcsv import readcsv
>>> import os
>>> os.listdir("/home/tomita/jmaDataUse/sampleCsv")
['福島県小名浜2020.csv', '福島県平.csv', '福島県小名浜.csv', '福島県小名浜2020_1_4.csv', '福島県小名浜2020_1.csv', '福島県平2020.csv', '福島県平2020_1.csv', '福島県平2020_1_4.csv']

>>> Data = readcsv("/home/tomita/jmaDataUse/sampleCsv/福島県小名浜2020_1.csv")
>>> Data.df #DataFrameを取得
    現地平均気圧 (hPa)  海面平均気圧 (hPa)  降水量合計 (mm)  ...  最深積雪  天気概況昼  天気概況夜
1         1020.0        1020.6         NaN  ...   NaN    NaN    NaN
2         1020.6        1021.2         NaN  ...   NaN    NaN    NaN
3         1015.9        1016.5         0.0  ...   NaN    NaN    NaN
4         1014.2        1014.8         0.0  ...   NaN    NaN    NaN
5         1020.5        1021.1         0.0  ...   NaN    NaN    NaN
6         1024.9        1025.5         NaN  ...   NaN    NaN    NaN
7         1024.8        1025.4         6.5  ...   NaN    NaN    NaN
8         1002.8        1003.4         8.0  ...   NaN    NaN    NaN
9         1008.0        1008.6         0.0  ...   NaN    NaN    NaN
10        1016.2        1016.8         0.0  ...   NaN    NaN    NaN
11        1014.8        1015.4         NaN  ...   NaN    NaN    NaN
12        1010.4        1011.0         0.0  ...   NaN    NaN    NaN
13        1011.5        1012.1         0.0  ...   NaN    NaN    NaN
14        1019.3        1019.9         0.0  ...   NaN    NaN    NaN
15        1015.8        1016.4         5.0  ...   NaN    NaN    NaN
16        1020.9        1021.5         NaN  ...   NaN    NaN    NaN
17        1019.2        1019.8         NaN  ...   NaN    NaN    NaN
18        1013.5        1014.1         0.0  ...   NaN    NaN    NaN
19        1013.8        1014.4         NaN  ...   NaN    NaN    NaN
20        1011.3        1011.9         NaN  ...   NaN    NaN    NaN
21        1020.0        1020.6         NaN  ...   NaN    NaN    NaN
22        1027.6        1028.3         0.0  ...   NaN    NaN    NaN
23        1020.8        1021.4         4.0  ...   NaN    NaN    NaN
24        1021.3        1021.9         NaN  ...   NaN    NaN    NaN
25        1027.7        1028.3         NaN  ...   NaN    NaN    NaN
26        1026.3        1026.9         NaN  ...   NaN    NaN    NaN
27        1026.4        1027.0         NaN  ...   NaN    NaN    NaN
28        1019.4        1020.0        18.5  ...   NaN    NaN    NaN
29        1001.8        1002.4        84.5  ...   NaN    NaN    NaN
30         997.4         998.0         0.0  ...   NaN    NaN    NaN
31        1003.3        1003.9         NaN  ...   NaN    NaN    NaN

[31 rows x 20 columns]
>>> Data.columns #columnsを表示
Index(['現地平均気圧 (hPa)', '海面平均気圧 (hPa)', '降水量合計 (mm)', '最大1時間降水量 (mm)',
       '最大10分間降水量 (mm)', '平均気温', '最高気温', '最低気温', '日平均湿度 (%)', '最小湿度 (%)',
       '平均風速 (m/s)', '最大風速 (m/s)', '最大風速の風向', '最大瞬間風速 (m/s)', '最大瞬間風速風向',
       '日照時間 (h)', '降雪合計 (cm)', '最深積雪', '天気概況昼', '天気概況夜'],
      dtype='object')
>>> Data.index #indexを表示(ここでは日にち)
Int64Index([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
           dtype='int64')
>>> Data.headerShow() #columnsを縦に表示
現地平均気圧 (hPa)
海面平均気圧 (hPa)
降水量合計 (mm)
最大1時間降水量 (mm)
最大10分間降水量 (mm)
平均気温
最高気温
最低気温
日平均湿度 (%)
最小湿度 (%)
平均風速 (m/s)
最大風速 (m/s)
最大風速の風向
最大瞬間風速 (m/s)
最大瞬間風速風向
日照時間 (h)
降雪合計 (cm)
最深積雪
天気概況昼
天気概況夜
Index(['現地平均気圧 (hPa)', '海面平均気圧 (hPa)', '降水量合計 (mm)', '最大1時間降水量 (mm)',
       '最大10分間降水量 (mm)', '平均気温', '最高気温', '最低気温', '日平均湿度 (%)', '最小湿度 (%)',
       '平均風速 (m/s)', '最大風速 (m/s)', '最大風速の風向', '最大瞬間風速 (m/s)', '最大瞬間風速風向',
       '日照時間 (h)', '降雪合計 (cm)', '最深積雪', '天気概況昼', '天気概況夜'],
      dtype='object')
>>> Data["海面平均気圧 (hP)"] #columを指定してデータを取得
1     1020.6
2     1021.2
3     1016.5
4     1014.8
5     1021.1
6     1025.5
7     1025.4
8     1003.4
9     1008.6
10    1016.8
11    1015.4
12    1011.0
13    1012.1
14    1019.9
15    1016.4
16    1021.5
17    1019.8
18    1014.1
19    1014.4
20    1011.9
21    1020.6
22    1028.3
23    1021.4
24    1021.9
25    1028.3
26    1026.9
27    1027.0
28    1020.0
29    1002.4
30     998.0
31    1003.9
Name: 海面平均気圧 (hPa), dtype: float64
```

## matplotlib関連
### [fontjp](https://github.com/RyosukeDTomita/jmaDataUse/blob/master/modules/fontjp.py)
- fontjp.py  : SourceHancodeJP-Regular.otfのパスを通します。使用するには、ダウンロードリンク](https://codeload.github.com/adobe-fonts/source-han-code-jp/zip/2.000R)からzipファイルをダウンロードし、解凍後にSourceHancodeJP-Regular.otfをインストールしてください。

```python3
from fontjp import fontjp
jp = fontjp()
ax.set_xlabel("test",fontproperties=jp.font)
```

```
from fontjp import fontjp
jp = fontjp()
ax.set_xlabel("test",fontproperties=jp())
```
### myMatlib.py
個人的に好きなmatplotlibのrcParamsの設定です。

```python3
from myMatlib import *
from fontjp import fontjp
grapher = pltSet()
fig = grapher.fig
ax = grapher.ax
x = np.arange(1,10,1)
y = x **2

ax.plot(x,y,marker='.',
        markersize=10,
        markeredgewidth=1.,
        markeredgecolor="k",
        label= "label",
        color="b",
        linestyle="solid")
ax.set_xlabel("x",
            fontsize=20,
            fontproperties=jp())
ax.set_ylabel("y",
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
fig.savefig("test",bbox_inches="tight",pad_inches=0.5)
```
うまくモジュール化できなかったところは今後の課題です。おそらく、plot等の機能は__name__ == __main__じゃないと走らないのかもしれません。



## [main.py](https://github.com/RyosukeDTomita/jmaDataUse/blob/master/modules/main.py)(モジュール使用例)

[main.py](https://github.com/RyosukeDTomita/jmaDataUse/blob/master/modules/main.py)では、[jma_dl.py](https://github.com/RyosukeDTomita/jmaDataUse/blob/master/modules/jma_dl.py)を使い、指定した日時の全県全市の気象データを取得し、まとめて図を作成してみます。
使用できる物理量はダウンロードしたcsvファイルのヘッダーを参照してください。

```shell
#全県全市の2020年1月の気象データを保存し、現地平均気圧の図を作成。
python3 main.py 2020 1 None "現地平均気圧 (hPa)"

#全県全市の2020年1月4日の気象データを保存し、降水量の図を作成。
python3 main.py 2020 1 4 "降水量 (mm)"
```
![sample](https://github.com/RyosukeDTomita/jmaDataUse/blob/master/modules/sampleFig/上川地方旭川2020_1.png
)
******


## データについて
ダウンロードするデータにはいくつかの意味のある記号が含まれているものがあります。
これらの意味は気象庁の[値欄の記号の説明](https://www.data.jma.go.jp/obd/stats/data/mdrr/man/remark.html)をご覧ください。

ただし、データの利便性の向上のため、本スクリプトでは"--","///","#"は空白に変換しています。

|                |                                                                                     |
|----------------|-------------------------------------------------------------------------------------|
|よく出てくる記号|説明                                                                                 |
|--              |該当現象、または該当現象による量がない場合。                                         |
|0               |該当現象は存在しているが、1に足りない場合。                                          |
|0.0             |該当現象は存在しているが0.1に足りない場合。ただし、降水量の場合には0.5 mm以下を表す。|
|]               |値が信用できないため、通常は上位の統計には用いない。                                 |
|×              |欠測の場合、または欠測によって値が求められないとき。                                 |
|///             |欠測または、観測を行っていない場合。                                                 |
|空白            |データなし                                                                           |
******


