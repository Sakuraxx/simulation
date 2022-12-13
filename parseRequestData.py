# txt 数据格式 mid tid pre_num fail_num
import json
from constant import *

def parse_dn_file(t):
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
        TOT_REQ = 100
        reqs = []
        IP = CLIENT_IP % j
        for req in pred_dn[IP]:
            if TOT_REQ <= 0: break
            for k in range(int(req[1])):
                reqs.append({'tid': req[0], 'type': 1})
                TOT_REQ -= 1
        for req in fail_dn[IP]:
            if TOT_REQ <= 0: break
            for k in range(int(req[1])):
                reqs.append({'tid': req[0], 'type': 2})
                TOT_REQ -= 1

        print(IP)
        print(len(reqs))
        req_file ='%s/%s_%s_%s.json' % (REQ_ROOT, IP, PERIOD, t)
        with open(req_file, 'w') as req_file:
            json.dump(reqs, req_file)

if __name__ == '__main__':
    for t in range(T):
        parse_dn_file(t)