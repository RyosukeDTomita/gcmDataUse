import matplotlib.pyplot as plt
from fontjp import fontjp
class pltSet:
    def __init__(self):
        self.fig = plt.figure(figsize = (9,6))
        self.ax = self.fig.add_subplot(111)

        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['mathtext.fontset'] = 'stix'
        plt.rcParams["font.size"] =15
        plt.rcParams['xtick.labelsize'] = 24
        plt.rcParams['ytick.labelsize'] = 24
        plt.rcParams['xtick.direction'] = 'in' # x軸の向きを内側に設定
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.linewidth'] = 1.0
        plt.rcParams['axes.grid'] = False
        plt.rcParams["legend.borderaxespad"] = 0. #凡例の箱をの位置をグラフに合わせて左に寄せる
        plt.rcParams["legend.fancybox"] = False # 丸角
        plt.rcParams["legend.framealpha"] = 1 # 透明度の指定、0で塗りつぶしなし
        plt.rcParams["legend.edgecolor"] = 'gray' # edgeの色を変更
        plt.rcParams["legend.handlelength"] = 1 # 凡例の線の長さを調節
        plt.rcParams["legend.handletextpad"] = 2. # 凡例の線と凡例のアイコンの距離
        plt.rcParams["legend.markerscale"] = 1
        plt.rcParams['figure.dpi'] = 300 #画質
        self.cnt = 0
        return None

# plt.show(),fig.savefig(),plt.grid(),ax.legend are not collectlly work in module.
