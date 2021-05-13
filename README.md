# 気象庁の過去の気象データ検索
[気象庁の過去の気象データ検索](https://www.data.jma.go.jp/obd/stats/etrn/index.php)のデータを活用するための非公式プログラムです。
## ProgramList
### kishotyo_dl.py
[気象庁の過去の気象データ検索](https://www.data.jma.go.jp/obd/stats/etrn/index.php)からデータをCSV形式でダウンロードできます。

```
python3 kishotyo_dl.py <県名> <市> <年> <月> <日>
```
上のように実行することで任意の場所時間のデータをCSVでダウンロードできます。指定できる県名は以下の通りです。
![指定できる県名](https://www.data.jma.go.jp/obd/stats/data/image/map/map00.png "指定できる県名")
指定できる市町村は、[気象庁の過去の気象データ検索](https://www.data.jma.go.jp/obd/stats/etrn/index.php)から検索するか、追記するcitySearch.pyを使用してください。
![市町村の例](https://www.data.jma.go.jp/obd/stats/data/image/map/map36.png "市町村選択ページ例")
地図で赤くプロットされている市町村のデータは気象台で観測されていますが、青と緑でプロットされた市町村はアメダスで観測されたデータです。これらはcsvのヘッダーが異なる点にご注意ください。また、市町村によって観測している項目が異なります。


さらに、引数の指定の仕方を変えることで、年平均、月平均、日平均、1時間平均データをダウンロードできます。

```
python3 kishotyo_dl.py 福島県 小名浜        #年平均データ(1910年~現在)
python3 kishotyo_dl.py 福島県 小名浜 2020   #2020年の月ごとのデータ
python3 kishotyo_dl.py 福島県 小名浜 2020 1 #2020年1月のデータ(データ間隔は日)
python3 kishotyo_dl.py 福島県 小名浜 2020 1 #2020年1月のデータ(データ間隔は1時間)
```
保存されるデータの名前は **<県名><市名><年>_<月>_<日>.csv**に設定されています。(プログラム実行時に指定しなかった引数は省略されます。)
ダウンロードできるデータのサンプルは同リポジトリ内のcsvファイルをご覧ください。


#### kishotyo_dl.pyに必要なライブラリ
- beautifulsoup4
- pandas
- numpy
- sys
- re

anacondaを使う場合には以下でインストールできます。他のものはデフォルトでanacondaに入っていると思います。

```
#how to install nessesary libraries with anaconda
conda install beautifulsoup4
conda install pandas
conda install numpy
```

#### データについて
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

## citySearch.py
ダウンロードできる市区町村を表示する。

```
python3 citySearch.py 福島県 #福島県の市区町村をを表示
python3 citySearch.py ALL    #日本全国の市区町村を表示
```
