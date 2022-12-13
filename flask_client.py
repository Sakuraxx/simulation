#!/usr/bin/env python3
# -*- coding: utf-8 -*-#请求http/query/接口
 
import requests, json
import time
import optparse
import os

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=15005)
parser.add_option('-u', dest='uIP') # 客户端(本地)的ip地址
parser.add_option('-c', dest='cacheMode') 
(options, args) = parser.parse_args()

UIP = options.uIP
RES_FILE = './data/%s_%s.txt' % (UIP, options.cacheMode)
REQ_FILE = './data/%s.json' % UIP
SINGAL_FILE = './data/signal.txt'

url = 'http://%s:%s/query/' % (options.ip, options.port)
# print('[Client] %s' % url)

# 读取请求文件
with open(REQ_FILE, 'r') as f:
    reqs = json.load(f)

# if os.path.exists(RES_FILE):
#     os.remove(RES_FILE)

print('Client %s start...' % UIP)

res_arr = []
# 发起请求
for send_dat in reqs:
    t1 = time.perf_counter()
    r = requests.post(url, data=json.dumps(send_dat)) # 发送到服务端
    t2 = time.perf_counter()
    dat_stream = r.content.decode('utf-8')
    # print(dat_stream)
    res_dat = json.loads(dat_stream)
    interval = round((t2 - t1) * 1000) # 请求时间间隔 单位ms
    print('[Client %s] Len:%sB Time:%sms' % (UIP, res_dat['len'], interval))
    res_arr.append('%s %s %s\n' % (res_dat['tid'], res_dat['len'], interval))
    time.sleep(0.5) 
    # break

print('Total Requests: ', len(reqs))

with open(RES_FILE, 'w') as f:
    # tid len time
    for line in res_arr:
        f.write(line)
    f.flush()

# 客户端程序运行结束
with open(SINGAL_FILE, 'a+') as f:
    f.write(UIP)
    f.flush()