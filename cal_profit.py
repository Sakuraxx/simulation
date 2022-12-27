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


# 记录平均请求时延
def cal_avg_req_delay(modes):
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

    print('Total Delay:', res)
    print('Total Requests:', reqCnt)

    # c_arr = np.array(res['cloud']) / np.array(reqCnt['cloud'])
    print('Average Request Delay:')
    for mode in modes:
        arr = np.array(res[mode])
        avgDelay = np.round(arr / reqCnt[mode], decimals=0)
        res[mode] = list(avgDelay)
        print(' ', mode[0:3], '\t', avgDelay)
    return res


if __name__ == '__main__':
    # modes = [c for c in CACHE_MODE]
    # modes.append('cloud')
    modes = ['ksp']
    avg_res = cal_avg_req_delay(modes)
    avg_json_file = AVG_RES_FILE % PERIOD
    with open(avg_json_file, 'w') as file:
            json.dump(avg_res, file)