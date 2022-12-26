from constant import *
import json

def show_reqs():
    for t in range(2):
        reqs = [[0 for i in range(N)] for j in range(M)]
        for j in range(M):
            file = REQ_FILE % (CLIENT_IP % j, PERIOD, t)
            f = open(file)
            data = json.load(f)
            for d in data:
                reqs[j][int(d['tid'])] += 1

        for line in reqs:
            print(line)
        print("-" * 50)


# 查看缓存分布
for mode in CACHE_MODE:
    print(mode)
    cache = [[0 for i in range(N)] for j in range(M)]
    filename = './data/%s_cache_1_2.txt' % mode
    with open(filename, 'r') as f:
        for line in f.readlines():
            x = line.split(' ')
            cache[int(x[0])][int(x[1])] = int(x[2])
    for line in cache:
        print(line)
    print("-" * 50)
