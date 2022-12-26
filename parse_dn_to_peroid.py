import numpy as np
import os

M = 3
N = 100
PERIOD = 10

arr_p = [[0 for i in range(N)] for j in range(M)] # 预测请求
arr_f = [[0 for i in range(N)] for j in range(M)] # 补救请求

# 以最小时间单位来分割dn生成请求
dn_file = './data/dn_10_0.txt'
with open(dn_file, 'r') as f:
    for line in f.readlines():
        x = line.split(' ')
        arr_p[int(x[0])][int(x[1])] += int(x[2])
        arr_p[int(x[0])][int(x[1])] += int(x[3])


dn_sec = np.zeros((PERIOD, M, N))

for s in range(PERIOD):
    for j in range(M):
        for i in range(N):
            if arr_p[j][i] > 0:
                dn_sec[s][j][i] = 1 # 预测请求
                arr_p[j][i] -= 1
            elif arr_f[j][i] > 0:
                dn_sec[s][j][i] = 1 # 补救请求
                arr_f[j][i] -= 1


# 1sec为一个周期
dir = './data/dn/1/'
if not os.path.exists(dir):
    os.makedirs(dir)
for s in range(PERIOD):
    file = dir + str(s)
    with open(file, 'w') as f:
        for j in range(M):
            for i in range(N):
                f.write("%d %d %d\n" % (j, i, dn_sec[s][j][i]))

# 2sec为一个周期
