
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from topo import tugas2_1301204395

def main():
    setLogLevel('info')
    net = Mininet(tugas2_1301204395())
    net.start()

    info('\n\n')
    info('Enabling Routing\n\n')
    enable_routing(net)
    info('\n\n')

    CLI(net)
    net.stop()


def enable_routing(net):
    '''
        Enable static ipv4 routing on all routers
    '''
    routers = net.get('Router1', 'Router2', 'Router3', 'Router4', 'Router5', 'Router6')

    for router in routers:
        router.cmd('sysctl net.ipv4.ip_forward=1')

    routers = [''] + routers

    routers[1].cmd('ip route add 0.0.0.0/0 via 192.168.13.2')

    routers[2].cmd('ip route add 0.0.0.0/0 via 192.168.13.6')
    routers[2].cmd('ip route add 192.168.11.128/25 via 192.168.13.1') #

    routers[3].cmd('ip route add 0.0.0.0/0 via 192.168.13.14')
    routers[3].cmd('ip route add 192.168.10.0/25 via 192.168.13.18')
    routers[3].cmd('ip route add 192.168.13.20/30 via 192.168.13.18')
    
    routers[4].cmd('ip route add 192.168.11.128/25 via 192.168.13.10')
    routers[4].cmd('ip route add 192.168.13.0/30 via 192.168.13.10')
    routers[4].cmd('ip route add 192.168.10.128/25 via 192.168.13.10')
    routers[4].cmd('ip route add 192.168.13.4/30 via 192.168.13.10')
    routers[4].cmd('ip route add 192.168.12.0/25 via 192.168.13.10')
    routers[4].cmd('ip route add 192.168.13.20/30 via 192.168.13.13')
    routers[4].cmd('ip route add 192.168.10.0/25 via 192.168.13.13')
    routers[4].cmd('ip route add 192.168.13.16/30 via 192.168.13.13')
    routers[4].cmd('ip route add 192.168.12.128/26 via 192.168.13.13')

    routers[5].cmd('ip route add 0.0.0.0/0 via 192.168.13.17')

    routers[6].cmd('ip route add 0.0.0.0/0 via 192.168.13.9')
    routers[6].cmd('ip route add 192.168.11.128/25 via 192.168.13.5')
    routers[6].cmd('ip route add 192.168.13.0/30 via 192.168.13.5')
    routers[6].cmd('ip route add 192.168.10.128/25 via 192.168.13.5')

    net.pingAll()
    info('\n')


if __name__ == '__main__':
    main()