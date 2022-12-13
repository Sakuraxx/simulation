"""
polt.py

"""
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

config = {
    "font.family": 'SimHei',
    "font.size": 15,
    "mathtext.fontset":'stix',
    'font.weight': 'normal',
    'xtick.direction': 'in',
    'ytick.direction': 'in'
}
rcParams.update(config)

def plot_comparsion(xlabel, ylabel, xrange, ksp, st=None, dis=None, mixco=None, cmd=0):
    xticks = np.arange(len(xrange))  # 在横坐标上的位置
    KSP_label = 'OKSP'
    Mixco_label = 'MixCo'

    # 设置x轴刻度
    plt.xlim(xticks[0], xticks[-1])

    # 设置y轴刻度
    # plt.ylim(1, 100)

    plt.plot(xticks, ksp, marker='o', lw=1, label=KSP_label, color='brown', clip_on = False)
    if st is not None: plt.plot(xticks, st, marker='v', lw=1, label='Self-Top', color='teal', clip_on = False)
    if dis is not None: plt.plot(xticks, dis, marker='s', lw=1, label='Distributed', color='olive', clip_on = False)
    if mixco is not None: plt.plot(xticks, mixco, marker='P', lw=1, label=Mixco_label, color='royalblue', clip_on = False)

    plt.legend()  # 显示图例，即label

    # 设置网格线
    plt.grid(axis='y', linestyle='--')

    # tick label与坐标轴间的距离
    if cmd != 7: plt.tick_params(axis='x', which='major', pad=10)
    plt.tick_params(axis='y', which='major', pad=5)

    # 四周显示刻度
    plt.tick_params(bottom=True, top=True, left=True, right=True)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    pig_name = 'E:/研究生/VR-Network-Trans/总结文档/毕业论文图/res.svg'

    plt.tight_layout()  # 自动调整子图参数，使
    # 之填充整个图像区域
    plt.savefig(pig_name)
    plt.show()

if __name__ == '__main__':
    y = '平均时延节省量 / ms'
    period = 10
    x = '运行周期 / 10分钟'
    filename = 'E:/Experiment/simulation/ans.json'
    with open(filename, 'r') as f:
        res = json.load(f)
    print(res)
    xrange = [m for m in range(9)]
    plot_comparsion(x, y, xrange, res['ksp'], res['selfTop'], res['distributed'], res['mixco'])


