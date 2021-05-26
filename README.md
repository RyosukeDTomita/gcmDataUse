# 気象庁の過去の気象データ検索
[気象庁の過去の気象データ検索](https://www.data.jma.go.jp/obd/stats/etrn/index.php)のデータをスクレイピングしてCSV形式で保存します。

## リポジトリの概要
本リポジトリでは2種類の形でプログラムを提供しています。
1. [csvDownloader/](https://github.com/RyosukeDTomita/jmaDataUse/tree/master/csvDownloader): 非開発者向け。いくつかのデータが必要な方など。
2. [modules/](https://github.com/RyosukeDTomita/jmaDataUse/tree/master/modules): 開発者向け(WIP)。モジュールとして提供しています。

## データについて
![指定できる県名](https://www.data.jma.go.jp/obd/stats/data/image/map/map00.png "指定できる県名")
指定できる市町村は、[気象庁の過去の気象データ検索](https://www.data.jma.go.jp/obd/stats/etrn/index.php)から検索するか、追記するcitySearch.pyを使用してください。
![市町村の例](https://www.data.jma.go.jp/obd/stats/data/image/map/map36.png "市町村選択ページ例")
地図で赤くプロットされている市町村のデータは気象台で観測されていますが、青と緑でプロットされた市町村はアメダスで観測されたデータです。これらはcsvのヘッダーが異なる点にご注意ください。また、市町村によって観測している項目が異なります。

ダウンロードできるデータのサンプルは同リポジトリ内の[sampleCsv](https://github.com/RyosukeDTomita/jmaDataUse/tree/master/sampleCsv)をご覧ください。
******


## 必要なライブラリ
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

