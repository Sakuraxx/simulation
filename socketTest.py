#!/usr/bin/python

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
import time
from myTopo import MECTopo
from myTopo import *
import os
from constant import *
from util import *

def recreateSignalFile():
    # 重新建立客户端信号文件
    if os.path.exists(SINGAL_FILE):
        os.remove(SINGAL_FILE)
    file = open(SINGAL_FILE,'w')
    file.close()

def run(mode, t):
    lg.setLogLevel('info')
    recreateSignalFile()

    net = Mininet(MECTopo(n=M))
    net.start()

    # 建立MEC之间、MEC和云端之间的链路
    mec2mec(net, M)
    mec2dc(net, M)

    mlist = []
    ulist = []
    for i in range(M):
        mlist.append(net.get('m%s' % (i + 1)))
        ulist.append(net.get('u%s' % (i + 1)))

    # 开启服务器
    info('\nStart all servers\n')
    cloud = net.get('cloud')
    cloud.cmd('sudo python3 flask_server.py -i %s -c %s -t %s &'
                                    % (cloud.IP(), mode, t))
    for mec in mlist:
        serverInfo = mec.cmd('sudo python3 flask_server.py -i %s -c %s -t %s &'
                                    % (mec.IP(), mode, t))
        info(serverInfo)

    time.sleep(5) # 暂停一下 等待服务器端处于运行状态

    # 开启客户端
    info('Start all clients\n')
    for i in range(M):
        user = ulist[i]
        homeMEC = mlist[i]
        clientInfo = user.cmd('sudo python3 flask_client.py -i %s -u %s -c %s -t %s &' #后台运行
                                % (homeMEC.IP(), user.IP(), mode, (t + 1))) # 客户端使用下一轮的请求
        info(clientInfo)

    while True:
        cnt = wc_count(SINGAL_FILE)
        if cnt == M:
            break
        time.sleep(1)

    info('Stop simultaion.\n')
    net.stop()

def printCurMode(mode, t):
     print('-'*20)
     print(mode, t)
     print('-'*20)

if __name__ == '__main__':
    # modes = [c for c in CACHE_MODE]
    # modes.append('cloud')
    # modes = ['selfTop', 'mixco', 'cloud']
    modes = ['cloud']
    for mode in modes:
        for t in range(0, T - 1):
            printCurMode(mode, t)
            run(mode, t)
            time.sleep(2)


