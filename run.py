from time import sleep

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
    net.pingAll()   # Checking network availability
    info('\n')
    info('\n\n')

    with Iperf_Server(net, 'PC7') as server:
        # Initializing client, routers, controller, and cap_file for Iperf testing
        client = net['PC1']
        routers = tuple(net[router] for router in ('Router1', 'Router2', 'Router3', 'Router4', 'Router5', 'Router6'))
        controller = net['c0']
        cap_file = 'tugas2_1301204395.pcap'

        info('Testing Iperf\n\n')
        generate_tcp_traffic(server, client, save_cap=True, cap_file=cap_file)
        controller.cmd(f'wireshark {cap_file}&')    # Open capture file in wireshark
        info('\n\n')

        info('Generating Delay Traffic\n\n')
        generate_delay_traffic(server, client, routers)
        info('\n\n')


    CLI(net)
    net.stop()


def enable_routing(net):
    '''
        Enable static ipv4 routing on all routers
    '''

    # Initializing routers
    routers = net.get('Router1', 'Router2', 'Router3', 'Router4', 'Router5', 'Router6')

    # Enabling ipv4 ip forwarding on every router
    for router in routers:
        router.cmd('sysctl net.ipv4.ip_forward=1')

    # Padding router list for easier indexing
    routers = [''] + routers


    # Adding static routes
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

def generate_tcp_traffic(server, client, time=10, cap_num=300, save_cap=False, cap_file='1301204395.pcap'):
    '''
        Generate tcp traffic with iperf
    '''
    read_count=20   # For shell output

    # Capturing traffic with tcpdump
    if save_cap:    # Write captured traffic to a file if true
        server.sendCmd(f'tcpdump tcp -c {cap_num} -w {cap_file}')
    else:
        server.sendCmd(f'tcpdump tcp -c {read_count}')

    client.cmdPrint(f'iperf -c {server.IP()} -t {time} -i 1')
    info('\n')

    # Outputing captured traffic
    if save_cap:    # Read from captured file
        server.waitOutput()
        server.cmdPrint(f'tcpdump -c {read_count} -r {cap_file}')
    else:           # Print server output
        info(server.waitOutput())
    info('\n')

def generate_delay_traffic(server, client, routers, time=5, save_cap=False, delays=('20ms','40ms','60ms','80ms','100ms')):
    '''
        Generate tcp traffic(s) for each delay
    '''

    def change_delay(router, delay):
        'Change the queue delay for every interface on the router'
        for intf in router.intfNames():
            router.cmd(f'tc qdisc del dev {intf} root')
            router.cmd(f'tc qdisc add dev {intf} root handle 1: netem delay {delay}')
    
    for delay in delays:
        for router in routers:  # Change the queue delay delay on all routers
            change_delay(router, delay)
        info(f'\nTraffic for queue delay {delay} packets\n\n')
        routers[0].cmdPrint('tc qdisc')
        info('\n')

        # Generating traffic
        generate_tcp_traffic(server=server, client=client, time=time, save_cap=save_cap, cap_file=f'delay_{delay}.pcap')

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
        sleep(1)    # iperf server needs a moment before accepting traffic
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        'Close iperf process'
        self.server.cmd('kill %iperf')

if __name__ == '__main__':
    main()