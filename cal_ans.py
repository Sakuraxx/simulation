from constant import *
import json

ps = [2, 4, 5, 8, 10]

avg_req_delay = {}
for p in ps:
    res_file = AVG_RES_FILE % p
    f = open(res_file)
    data = json.load(f)
    ret = sum(data['ksp']) // len(data['ksp'])
    avg_req_delay[str(p)] = ret

print(avg_req_delay)