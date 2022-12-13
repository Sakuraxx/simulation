# txt 数据格式 mid tid 0/1
# 所有MEC服务器都读取同一个cache文件
# {"1": ["10.0.200.254"], "2": ["10.0.200.254"]}

import json
from constant import *


cache_arr = [[0 for j in range(M)] for i in range(N)]

with open(CACHE_TXT, 'r') as cache_file:
    for line in cache_file.readlines():
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


# print(cache_json)
with open(CACHE_JSON, 'w') as file:
    json.dump(cache_json, file)