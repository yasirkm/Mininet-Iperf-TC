from collections import defaultdict
from itertools import combinations

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink

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
                'ip' : '192.168.11.129/25',
                'cls' : CPULimitedHost
            },
            'Router2': {
                'ip' : '192.168.10.129/25',
                'cls' : CPULimitedHost
            },
            'Router3': {
                'ip' : '192.168.12.129/26',
                'cls' : CPULimitedHost
            },
            'Router4' : {
                'ip' : '192.168.11.1/25',
                'cls' : CPULimitedHost
            },
            'Router5' : {
                'ip' : '192.168.10.1/25',
                'cls' : CPULimitedHost
            },
            'Router6' : {
                'ip' : '192.168.12.1/25',
                'cls' : CPULimitedHost
            }
        }

        hosts_param = {
            'PC0' : {
                'ip' : '192.168.11.130/25',
                'defaultRoute' : 'via 192.168.11.129',
                'cls' : CPULimitedHost
            },
            'PC1' : {
                'ip' : '192.168.12.130/26',
                'defaultRoute' : 'via 192.168.12.129',
                'cls' : CPULimitedHost
            },
            'PC2' : {
                'ip' : '192.168.11.2/25',
                'defaultRoute' : 'via 192.168.11.1',
                'cls' : CPULimitedHost
            },
            'PC3' : {
                'ip' : '192.168.10.130/25',
                'defaultRoute' : 'via 192.168.10.129',
                'cls' : CPULimitedHost
            },
            'PC6' : {
                'ip' : '192.168.12.2/25',
                'defaultRoute' : 'via 192.168.12.1',
                'cls' : CPULimitedHost
            },
            'PC7' : {
                'ip' : '192.168.10.2/25',
                'defaultRoute' : 'via 192.168.10.1',
                'cls' : CPULimitedHost
            }
        }

        pc_router_pairs = (('PC0', 'Router1'), ( 'PC3', 'Router2'), ('PC1','Router3'), ('PC2', 'Router4'), ('PC7', 'Router5'), ('PC6', 'Router6'))

        links_param = {
            'Router1' : { #
                'Router2' : {
                    'params1' : {
                        'ip' : '192.168.13.1/30'
                    },
                    'params2' : {
                        'ip' : '192.168.13.2/30'
                    },
                    'cls' : TCLink
                },
                'Router5' : {
                    'params1' : {
                        'ip' : '192.168.13.21/30'
                    },
                    'params2' : {
                        'ip' : '192.168.13.22/30'
                    },
                    'cls' : TCLink
                }
            },
            
            'Router2' : {
                'Router6' : {
                    'params1' : {
                        'ip' : '192.168.13.5/30'
                    },
                    'params2' : {
                        'ip' : '192.168.13.6/30'
                    },
                    'cls' : TCLink
                }
            },
            
            'Router4' : {
                'Router6' : {
                    'params1' : {
                        'ip' : '192.168.13.9/30'
                    },
                    'params2' : {
                        'ip' : '192.168.13.10/30'
                    },
                    'cls' : TCLink
                }
            },
            
            'Router3' : { #
                'Router4' : {
                    'params1' : {
                        'ip' : '192.168.13.13/30'
                    },
                    'params2' : {
                        'ip' : '192.168.13.14/30'
                    },
                    'cls' : TCLink
                },
                'Router5' : {
                    'params1' : {
                        'ip' : '192.168.13.17/30'
                    },
                    'params2' : {
                        'ip' : '192.168.13.18/30'
                    },
                    'cls' : TCLink
                }
            }       
        }

        for router, param in routers_param.items():
            self.addNode(router, **param)
        
        for host, param in hosts_param.items():
            self.addHost(host, **param)

        for pc, router in pc_router_pairs:
            self.addLink(pc, router)

        for router1, router2 in combinations(routers_param, 2):
            try:
                param = links_param[router1][router2]
            except KeyError:
                param = {'cls':TCLink}
            self.addLink(router1, router2, **param)