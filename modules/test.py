import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p","--prefecture",help="chose target prefecture name from https://www.data.jma.go.jp/obd/stats/data/image/map/map00.png ,type=str")
parser.add_argument("-c","--city",help="chose target city Name",type=str)
args = parser.parse_args()
prefecture=args.prefecture
print(prefecture)
