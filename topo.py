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

        for router, param in routers_param:
            self.addNode(router, **param)
        
        for i in (x for x in range(8) if x not in (4,5)):
            self.addHost(f'PC{i}')

        
