#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections, dumpNetConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCIntf, TCLink
from mininet.node import Host, Node

# 链路带宽 Mbit
_1MB = 1
UM_BW = _1MB * 10
MM_BW = _1MB * 100
MD_BW = _1MB * 1000

# 延迟
UM_DELAY = '1ms'
MM_DELAY = '2ms'
MD_DELAY = '50ms'

class MECTopo(Topo):
    "MEC cooperative network"
    def build(self, n=3):
        for id in range(n):
            mec = self.addHost('m%s' % (id + 1), ip='10.0.%s.1/24' % id)
            user = self.addHost('u%s' % (id + 1), ip='10.0.%s.2/24' % id)
            self.addLink(user, mec, cls=TCLink, bw=UM_BW, delay=UM_DELAY)
"""
mec ip: 10.0.n.1/24
user ip: 10.0.n.2/24
cloud ip: 10.0.200.254/24
"""

def get_mec_ip(mid):
    return '10.0.%s.1' % mid

def get_mec_ip_p(mid):
    return '10.0.%s.1/24' % mid

def mec2mec(net, M):
    for i in range(M):
        for j in range(i + 1, M):
            mi = net.get('m%s' % (i + 1))
            mj = net.get('m%s' % (j + 1))
            # 配置mec服务器的ip地址
            mi_dev = 'm%s-eth%s' % (i + 1, j)
            mj_dev = 'm%s-eth%s' % (j + 1, i + 1)
            mi.cmd('ifconfig %s %s netmask 255.255.255.0' % (mi_dev, get_mec_ip(i)))
            mj.cmd('ifconfig %s %s netmask 255.255.255.0' % (mj_dev, get_mec_ip(j)))
            # 添加mec服务器之间的链路
            net.addLink(mi, mj, cls=TCLink, 
                                params1={'ip': get_mec_ip_p(i), 'bw': MM_BW, 'delay': MM_DELAY}, 
                                params2={'ip': get_mec_ip_p(j), 'bw': MM_BW, 'delay': MM_DELAY})
            # 添加到特定主机的路由
            mi.cmd('sudo route add -host %s dev %s' % (get_mec_ip(j), mi_dev))
            mj.cmd('sudo route add -host %s dev %s' % (get_mec_ip(i), mj_dev))


def mec2dc(net, M):
    # mec <-> cloud
    cloud = net.addHost('cloud', cls=Node)
    for i in range(M):
        # 配置ip地址
        mec = net.get('m%s' % (i + 1))
        m_dev = 'm%s-eth%s' % (i + 1, M)
        c_ip_prefix = '10.0.200.254/24'
        c_ip = '10.0.200.254'
        c_dev = 'cloud-eth%s' % i
        mec.cmd('ifconfig %s %s netmask 255.255.255.0' % (m_dev, get_mec_ip(i)))
        cloud.cmd('ifconfig %s %s netmask 255.255.255.0' % (c_dev, c_ip))
        # 创建mec服务器和数据中心之间的链路
        net.addLink(mec, cloud, cls=TCLink, 
                                params1={'ip': get_mec_ip_p(i), 'bw': MD_BW, 'delay': MD_DELAY}, 
                                params2={'ip': c_ip_prefix, 'bw': MD_BW, 'delay': MD_DELAY})
        # 添加直接路由
        mec.cmd('sudo route add -host %s dev %s' % (c_ip, m_dev))
        cloud.cmd('sudo route add -host %s dev %s' % (get_mec_ip(i), c_dev))


def simpleTest():
    "Create and test a simple network"
    topo = MECTopo(n = 3)
    net = Mininet(topo)
    net.start()

    mec2mec(net, 3)
    mec2dc(net, 3)

    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)
    print( "Testing network connectivity" )
    CLI( net )
    net.pingAll() # 默认ping eth0 接口
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
