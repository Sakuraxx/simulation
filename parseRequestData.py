# txt 数据格式 mid tid pre_num fail_num
import json
from constant import *

def parse_dn_file(t):
    cnt = 0
    pred_dn = {}
    fail_dn = {}

    for j in range(M):
        pred_dn[CLIENT_IP % j] = []
        fail_dn[CLIENT_IP % j] = []
    dn_file = DN_FILE % (PERIOD, t)
    with open(dn_file, 'r') as file:
        for line in file.readlines():
            fields = line.split(" ")
            pred_dn[CLIENT_IP % fields[0]].append((fields[1], fields[2]))
            fail_dn[CLIENT_IP % fields[0]].append((fields[1], fields[3]))

    for j in range(M):
        reqs = []
        IP = CLIENT_IP % j
        for req in pred_dn[IP]:
            for k in range(int(req[1])):
                reqs.append({'tid': req[0], 'type': 1})
        for req in fail_dn[IP]:
            for k in range(int(req[1])):
                reqs.append({'tid': req[0], 'type': 2})

        # print(IP)
        # print(len(reqs))
        req_file = REQ_FILE % (IP, PERIOD, t)
        with open(req_file, 'w') as req_file:
            json.dump(reqs, req_file)
        cnt += len(reqs)
    return cnt

if __name__ == '__main__':
    for t in range(T):
        print(t, parse_dn_file(t))