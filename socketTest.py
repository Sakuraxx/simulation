#!/usr/bin/python

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
import time
from myTopo import MECTopo
from myTopo import *

def main():
    lg.setLogLevel('info')

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
        clientInfo = user.cmd('sudo python3 flask_client.py -i %s -u %s -c %s' 
                                % (homeMEC.IP(), user.IP(), CACHE_MODE))
        info(clientInfo)

    CLI( net ) 
    net.stop()

if __name__ == '__main__':
    main()

"""
'/home/mininet/.local/lib/python3.8/site-packages'
"""