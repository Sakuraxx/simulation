# txt 数据格式 mid tid pre_num fail_num
import json

P_PATH = './data'
CLIENT_IP = '10.0.%s.2'
DN_FILE = 'dn_10_1.txt'
N = 200
M = 3

pred_dn = {}
fail_dn = {}

for j in range(M):
    pred_dn[CLIENT_IP % j] = []
    fail_dn[CLIENT_IP % j] = []

with open('%s/%s' % (P_PATH, DN_FILE)) as dn_file:
    for line in dn_file.readlines():
        fields = line.split(" ")
        pred_dn[CLIENT_IP % fields[0]].append((fields[1], fields[2]))
        fail_dn[CLIENT_IP % fields[0]].append((fields[1], fields[3]))



for j in range(M):
    TOT_REQ = 20
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
    with open('%s/%s.json' % (P_PATH, IP), 'w') as req_file:
        json.dump(reqs, req_file)