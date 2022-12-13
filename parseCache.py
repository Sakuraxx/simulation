# txt 数据格式 mid tid 0/1
# 所有MEC服务器都读取同一个cache文件
# {"1": ["10.0.200.254"], "2": ["10.0.200.254"]}

import json
from constant import *

def parse_cache_file(cache_mode, t):

    cache_arr = [[0 for j in range(M)] for i in range(N)]
    cache_txt = CACHE_TXT % (cache_mode, PERIOD, t)
    with open(cache_txt, 'r') as file:
        for line in file.readlines():
            fields = line.split(" ")
            mid = int(fields[0])
            tid = int(fields[1])
            cache_arr[tid][mid] = int(fields[2])

    cache_json = {}
    for i in range(N):
        cache_json[i] = [CLOUD_IP]
        for j in range(M):
            IP = MEC_IP % j
            if cache_arr[i][j]: cache_json[i].append(IP)

    cache_json_file = CACHE_JSON % (cache_mode, PERIOD, t)
    with open(cache_json_file, 'w') as file:
        json.dump(cache_json, file)

if __name__ == '__main__':
    for mode in CACHE_MODE:
        for t in range(T):
            parse_cache_file(mode, t)