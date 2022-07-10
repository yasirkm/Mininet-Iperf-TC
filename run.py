
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

def generate_tcp_traffic(server, client, time=10, cap_num=300, save_cap=False, cap_file='1301204395.pcap'):   # CLO 3
    '''
        Generate tcp traffic with iperf
    '''
    read_count=20

    if save_cap:
        server.sendCmd(f'tcpdump tcp -c {cap_num} -w {cap_file}')
    else:
        server.sendCmd(f'tcpdump tcp -c {read_count}')

    client.cmdPrint(f'iperf -c {server.IP()} -t {time} -i 1')
    info('\n')

    if save_cap:
        server.waitOutput()
        server.cmdPrint(f'tcpdump -c {read_count} -r {cap_file}')
    else:
        info(server.waitOutput())
    info('\n')

class Iperf_Server():
    '''
        Context manager for running iperf server
    '''
    def __init__(self, net, server):
        'Initiate server node'
        self.server = net[server]

    def __enter__(self):
        'Run iperf server process on server node'
        self.server.cmd('iperf -s &')
        sleep(1)
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        'Close iperf process'
        self.server.cmd('kill %iperf')

if __name__ == '__main__':
    main()