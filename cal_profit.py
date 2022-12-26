from constant import *
from util import *
import numpy as np
import json

# 计算时延节省量

def cal_tot_delay(filename):
    res = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            fields = line.split(' ')
            res += int(fields[-1])
    return res

if __name__ == '__main__':
    modes = [c for c in CACHE_MODE]
    modes.append('cloud')
    # modes = ['ksp', 'cloud']
    res = {}
    reqCnt = {}
    for mode in modes:
        res[mode] = []
        reqCnt[mode] = []
        for t in range(3, 4):
            delay = 0
            cnt = 0
            for j in range(M):
                delay_file = DELAY_RES_FILE % (j, mode, PERIOD, t)
                delay += cal_tot_delay(delay_file)
                cnt += wc_count(delay_file)
            res[mode].append(delay)
            reqCnt[mode].append(cnt)

    print('Total Delay:', res)
    print('Total Requests:', reqCnt)

    c_arr = np.array(res['cloud']) / np.array(reqCnt['cloud'])
    for mode in modes:
        arr = np.array(res[mode])
        avgDelay = arr / reqCnt[mode]
        ans = c_arr - avgDelay
        ans = np.round(ans, decimals=0) # 平均时延节省量
        ans = np.round(ans / c_arr * 100, decimals=0) # 平均时延节省率
        res[mode] = list(ans)
        print(' ', mode, avgDelay)
    print('Total Saved Delay Rate:', res)
    print('=' * 30)

    res_json_file = RES_JSON_FILE % PERIOD
    with open(res_json_file, 'w') as file:
            json.dump(res, file)