from collections import defaultdict

from mininet.topo import Topo

class tugas2_1301204395(Topo):
    '''
        Topology for tugas2 NETOS
    '''
    def build(self):
        '''
            Build the topology
        '''

        routers_param = {
            'Router1' : {
                'ip' : '192.168.11.129/25'
            },
            'Router2': {
                'ip' : '192.168.10.129/25'
            },
            'Router3': {
                'ip' : '192.168.12.129/26'
            },
            'Router4' : {
                'ip' : '192.168.11.1/25'
            },
            'Router5' : {
                'ip' : '192.168.10.1/25'
            },
            'Router6' : {
                'ip' : '192.168.12.1/25'
            }
        }

        hosts_param = {
            'PC0' : {
                'ip' : '192.168.11.130/25',
                'defaultRoute' : '192.168.11.129/25'
            },
            'PC1' : {
                'ip' : '192.168.12.130/26',
                'defaultRoute' : '192.168.12.129/26'
            },
            'PC2' : {
                'ip' : '192.168.11.2/25',
                'defaultRoute' : '192.168.11.1/25'
            },
            'PC3' : {
                'ip' : '192.168.10.130/25',
                'defaultRoute' : '192.168.10.129/25'
            },
            'PC6' : {
                'ip' : '192.168.12.2/25',
                'defaultRoute' : '192.168.12.1/25'
            },
            'PC7' : {
                'ip' : '192.168.10.2/25',
                'defaultRoute' : '192.168.10.1/25'
            }
        }

        for router, param in routers_param.items():
            self.addNode(router, **param)
        
        for host, param in hosts_param.items():
            self.addHost(host, **param)

        
