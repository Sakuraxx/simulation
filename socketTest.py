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

def main():
    lg.setLogLevel('info')

    # 重新建立客户端信号文件
    if os.path.exists(SINGAL_FILE):
        os.remove(SINGAL_FILE)
    file = open(SINGAL_FILE,'w')
    file.close()

    M = 3
    CACHE_MODE = "ksp"
    # CACHE_MODE = "cloud"

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
    cloud.cmd('sudo python3 flask_server.py -i %s  -c %s & ' % (cloud.IP(), CACHE_MODE))
    for mec in mlist:
        serverInfo = mec.cmd('sudo python3 flask_server.py -i %s  -c %s &' % (mec.IP(), CACHE_MODE))
        info(serverInfo)

    time.sleep(5) # 暂停一下 等待服务器端处于运行状态

    # 开启客户端
    info('Start all clients\n')
    for i in range(M):
        user = ulist[i]
        homeMEC = mlist[i]
        clientInfo = user.cmd('sudo python3 flask_client.py -i %s -u %s -c %s &' #后台运行
                                % (homeMEC.IP(), user.IP(), CACHE_MODE))
        info(clientInfo)

    while True:
        cnt = wc_count(SINGAL_FILE)
        if cnt == M:
            break
        time.sleep(1)

    info('Stop simultaion.\n')
    net.stop()


def wc_count(file_name):
    import subprocess
    out = subprocess.getoutput("wc -l %s" % file_name)
    return int(out.split()[0])


if __name__ == '__main__':
    main()