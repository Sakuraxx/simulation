import numpy as np
import os
import random

random.seed(0)

M = 3
N = 200
PERIOD = 10

def get_dn_sec():
    arr_p = [[0 for i in range(N)] for j in range(M)] # 预测请求
    arr_f = [[0 for i in range(N)] for j in range(M)] # 补救请求

    # 以最小时间单位来分割dn生成请求
    dn_file = './data/dn_10.txt'
    with open(dn_file, 'r') as f:
        for line in f.readlines():
            x = line.split(' ')
            arr_p[int(x[0])][int(x[1])] += int(x[2])
            arr_p[int(x[0])][int(x[1])] += int(x[3])

    dn_sec = np.zeros((PERIOD, M, N, 2)) # m0 n0 1(预测请求数) 0（补救请求数）

    for s in range(PERIOD):
        for j in range(M):
            for i in range(N):
                if arr_p[j][i] > 0:
                    dn_sec[s][j][i][0] = 1 # 预测请求
                    arr_p[j][i] -= 1
                elif arr_f[j][i] > 0:
                    dn_sec[s][j][i][1] = 1 # 补救请求
                    arr_f[j][i] -= 1
    return dn_sec

def gen_dn_per_P(dn, P):
    dir = './data/dn/%s/' % P
    if not os.path.exists(dir):
        os.makedirs(dir)
    for s in range(PERIOD // P):
        file = dir + str(s)
        with open(file, 'w') as f:
            for j in range(M):
                for i in range(N):
                    f.write("%d %d %d %d\n" % (j, i, dn[s][j][i][0], dn[s][j][i][1]))

def random_change_the_req_of_diff_peroid(dn_sec):
    for j in range(M):
        for i in range(N):
            for t in range(PERIOD):
                t1 = random.randint(0, PERIOD - 1)
                t2 = random.randint(0, PERIOD - 1)
                tmp = dn_sec[t1][j][i]
                dn_sec[t1][j][i] = dn_sec[t2][j][i]
                dn_sec[t2][j][i] = tmp
    return dn_sec

def print_req_num_in_diff_peroid(dn, tt):
    for t in range(PERIOD // tt):
        print(t, dn[t].sum())

# 生成指定时间间隔的请求量
def gen_dn_on_given_turn(dn_sec, turn, p):
    dn = np.zeros((turn, M, N, 2)) # m0 n0 1(预测请求数) 0（补救请求数）
    tt = p
    for x in range(turn):
        for j in range(M):
            for i in range(N):
                s = x * tt
                ret = get_dn_between_t1_t2(dn_sec, s, s + tt, j, i)
                dn[x][j][i][0] = ret[0]
                dn[x][j][i][1] = ret[1]
    return dn

def get_dn_between_t1_t2(dn_sec, t1, t2, j, i):
    pn = 0
    fn = 0
    # print(t1, t2)
    for k in range(t1, t2):
        pn += dn_sec[k][j][i][0]
        fn += dn_sec[k][j][i][1]
    return (pn, fn)


def gen_dn_in_gap():
    dn_sec = np.zeros((PERIOD, M, N, 2))
    for t in range(PERIOD):
        for j in range(M):
            for i in range(N):
                if t % 2 == 0 and i % 2 == 0:
                    dn_sec[t][j][i][0] = 1
                else:
                    dn_sec[t][j][i][0] = 1
                n = random.randint(1, 10)
                if n % 2 == 0:
                     dn_sec[t][j][i][0] = 0
    return dn_sec

if __name__ == '__main__':
    
    # dn_sec = get_dn_sec()
    dn_sec = gen_dn_in_gap()
    print_req_num_in_diff_peroid(dn_sec, 1)
    print('totReq', dn_sec.sum())
    # 1sec为一个周期，每个周期的的请求量逐次递减
    # gen_dn_per_P(dn_sec, 1)

    # dn = gen_dn_on_given_turn(dn_sec, 2, 5)
    # print_req_num_in_diff_peroid(dn, 5)
    # gen_dn_per_P(dn, 5)


    # 打乱请求，每个周期的请求量不定
    # dn_sec = random_change_the_req_of_diff_peroid(dn_sec)
    # print_req_num_in_diff_peroid(dn_sec, 1)
    # gen_dn_per_P(dn_sec, 1)
    # print('totReq', dn_sec.sum())

    # dn = gen_dn_on_given_t(dn_sec, 5)
    # print_req_num_in_diff_peroid(dn, 2)
    # gen_dn_per_P(dn, 2)
