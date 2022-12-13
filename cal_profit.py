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
    res = {}
    reqCnt = {}
    for mode in modes:
        res[mode] = []
        reqCnt[mode] = []
        for t in range(1, T):
            delay = 0
            cnt = 0
            for j in range(M):
                delay_file = DELAY_RES_FILE % (j, mode, PERIOD, t)
                delay += cal_tot_delay(delay_file)
                cnt += wc_count(delay_file)
            res[mode].append(delay)
            reqCnt[mode].append(cnt)

    print(res)
    print(reqCnt)

    c_arr = np.array(res['cloud']) / np.array(reqCnt['cloud'])
    for mode in CACHE_MODE:
        arr = np.array(res[mode])
        ans = c_arr - arr / reqCnt[mode]
        ans = np.round(ans, decimals=0)
        res[mode] = list(ans)

    print(res)

    with open(ANS_FILE, 'w') as file:
            json.dump(res, file)