#!/usr/bin/python3
#coding=utf-8

from flask import Flask, request, jsonify
import json
import optparse
import random
import requests
import time
from extractFrame import *
from constant import *

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='')
parser.add_option('-p', dest='port', type='int', default=15005)
parser.add_option('-c', dest='cacheMode')
(options, args) = parser.parse_args()

LOCAL_IP = options.ip
CACHE_MODE = options.cacheMode


# 生成指定大小比例的数据
def make_preidct_msg(p):
    nbytes = round(TILE_SIZE * p)
    t1 = time.perf_counter()
    x = bytearray( [ 0 for i in range(nbytes) ] )
    t2 = time.perf_counter()
    # with open('data.txt', 'a+') as f:
    #     f.write('Create data: %sB, %sms\n' % (nbytes, round((t2 - t1) * 1000)))
    #     f.flush()
    return x

# 创建并启动Flask应用
app = Flask(__name__)
app.debug = True
@app.route('/query/', methods=['post'])
def post_http():
    if not request.data:  # 检测是否有数据
        return ('fail')
    dat_stream = request.data.decode('utf-8')
    req_dat = json.loads(dat_stream)
    destIP = ""
    if CACHE_MODE == CLOUD_CACHE: # 直接向云端服务器请求
        destIP = CLOUD_IP
    else:
        destIP = check_cacheTable(req_dat["tid"])
    if destIP == LOCAL_IP: destIP = ""
    if destIP == "":
        req_dat = retrieve_from_local(req_dat)
    else:
        req_dat = fetch_from_other_MEC(req_dat, destIP)
    return jsonify(req_dat) # 返回JSON数据

# 向另外一个服务器请求数据
def fetch_from_other_MEC(dat, ip):
    port = "15005"
    url = 'http://%s:%s/query/' % (ip, port)
    r = requests.post(url, data=json.dumps(dat))
    return json.loads(r.content.decode('utf-8'))

# 查看缓存表，确定请求路径
def check_cacheTable(tid):
    destIP = ""
    with open(CACHE_JSON, 'r') as load_f:
        load_dict = json.load(load_f)
        hostIPs = load_dict[tid]
        if len(hostIPs) == 1: # 只有一个IP则为云端服务器
            destIP = CLOUD_IP
        else:
            in_local = LOCAL_IP in hostIPs
            if in_local == False: # 取得另外一个MEC服务器的IP
                destIP = hostIPs[0] if hostIPs[0] != CLOUD_IP else hostIPs[1]
    if destIP == LOCAL_IP: # 防止云端服务器递归向自己请求
        destIP = ""
    # with open('server.txt', 'a+') as f:
    #     f.write("%s -> %s\n" % (LOCAL_IP, destIP))
    #     f.flush()
    return destIP

# 从本地获取内容
def retrieve_from_local(dat):
    p = 1
    if dat['type'] == 2: # 补救请求
        p = 0.2
        extract_one_frame()
    msg = make_preidct_msg(p)
    dat['len'] = len(msg)
    dat['data'] = str(msg, encoding='utf-8')
    return dat

if __name__ == '__main__':
    app.run(host=LOCAL_IP, port=options.port)
