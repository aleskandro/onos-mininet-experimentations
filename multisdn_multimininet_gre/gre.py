from mininet.topo import Topo

class MyTopo( Topo ):
    "topology to connect two mininet networks together."

    def __init__( self ):
        Topo.__init__( self )

        spines = []
        leaves = []
        hosts  = []
        sb1 = self.addSwitch('sb1', dpid="0000000000000B11")
        spines.append(sb1)
        spines.append(self.addSwitch('sb2', dpid="0000000000000B12"))
        self.addLink(spines[0],spines[1])

        k = 4
        h = 6
        i = 1
        c = 0
        while i <= k:
            leaves.append(self.addSwitch('sb1%d' % i, dpid="0000000000000B0%d" % i))
            for spine in spines:
                self.addLink(leaves[i-1], spine)
            j = 1
            while j <= h:
                hosts.append(self.addHost('hb%d%d' % (i, j), ip='10.2.2.%d' % (i * 10 + j)))
                self.addLink(hosts[c], leaves[i-1])
                j += 1
                c += 1
            i += 1

        # Add hosts and switches
        hb1 = self.addHost( 'hb1', ip='10.2.2.1' )
        #s1 = self.addSwitch( 's1' )

        # Add link h1 -> s1
        self.addLink( hb1, sb1 )
#        sb1.cmd('ovs-vsctl add-port sb1 sb1-gre1 -- set interface sb1-gre1 type=gre options:remote_ip=10.32.32.170')


topos = { 'mytopo': ( lambda: MyTopo() ) }

