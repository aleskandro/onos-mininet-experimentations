#!/usr/bin/python

"""
multicluster.py: multiple ONOS clusters example

We create two ONOSClusters, "east" and "west", and
a LinearTopo data network where the first and second halves
of the network are connected to each ONOSCluster,
respectively.

The size of the ONOSCluster is determined by its
topology. In this example the topology is a
SingleSwitchTopo of size 1, so the "Cluster" is
actually a single node (for performance and
resource usage reasons.) However, it is possible
to use larger cluster sizes in a large (!) Mininet VM,
(e.g. 12 GB of RAM for two 3-node ONOS clusters.)

The MultiSwitch class is a customized version of
ONOSOVSSwitch that has a "controller" instance variable
(and parameter)
"""

from mininet.net import Mininet
from mininet.topo import LinearTopo, SingleSwitchTopo, Topo
from mininet.log import setLogLevel
from mininet.topolib import TreeTopo
from mininet.clean import cleanup

from onos import ONOSCluster, ONOSOVSSwitch, ONOSCLI, RenamedTopo


class MultiSwitch( ONOSOVSSwitch ):
    "Custom OVSSwitch() subclass that connects to different clusters"

    def __init__( self, *args, **kwargs ):
        "controller: controller/ONOSCluster to connect to"
        self.controller = kwargs.pop( 'controller', None )
        ONOSOVSSwitch.__init__( self, *args, **kwargs )

    def start( self, controllers ):
        "Start and connect to our previously specified controller"
        return ONOSOVSSwitch.start( self, [ self.controller ] )


class MyTopo( Topo ):

    def __init__( self ):
        Topo.__init__( self )

        hostsCount = 50
        asdnCount = 5

        switches = []
        hosts = []
        i = 1
        while i <= hostsCount:
            hosts.append(self.addHost('h%d' % i))
            switches.append(self.addSwitch('s%d' % (i)))
            self.addLink(hosts[i-1],switches[i-1])
            i += 1

        asdn = 1
        while asdn <= asdnCount:
            
            low =  int((asdn - 1) * hostsCount / asdnCount)
            i = high =  int((asdn) * hostsCount / asdnCount)
            if (asdn != asdnCount):
                self.addLink(switches[i], switches[i-1]) # Border device

            while i > low:
                print ("asdn = %d, i = %d, j = nd  %d to %d "% (asdn, i,  high, low))
                #c = ddint((asdn ) * hostsCount / asdnCount) - i
                #j = int(asdn * hostsCount/asdnCount) - 1 - c
                j = i - 1
                while j > low:
                    print ("asdn = %d, i = %d, j = %d  %d to %d "% (asdn, i, j, high, low))
                    self.addLink(switches[i-1], switches[j-1])
                    j -= 1
                i -= 1
            asdn += 1
       
        self.addLink(switches[15], switches[45])
        self.addLink(switches[25], switches[45])


def run():
    "Test a multiple ONOS cluster network"
    setLogLevel( 'info' )
    # East and west control network topologies (using RenamedTopo)
    # We specify switch and host prefixes to avoid name collisions
    # East control switch prefix: 'east_cs', ONOS node prefix: 'east_onos'
    # Each network is a renamed SingleSwitchTopo of size clusterSize
    # It's also possible to specify your own control network topology
    clusterSize = 1
    etopo = RenamedTopo( SingleSwitchTopo, clusterSize,
                         snew='east_cs', hnew='east_onos' )
    wtopo = RenamedTopo( SingleSwitchTopo, clusterSize,
                         snew='west_cs', hnew='west_onos' )

    netopo = RenamedTopo( SingleSwitchTopo, clusterSize,
                        snew='ne_cs', hnew='ne_onos')
    nwtopo = RenamedTopo( SingleSwitchTopo, clusterSize,
                        snew='nw_cs', hnew='nw_onos')
    stopo = RenamedTopo( SingleSwitchTopo, clusterSize,
                        snew='sh_cs', hnew='sh_onos')

    # east and west ONOS clusters
    # Note that we specify the NAT node names to avoid name collisions
    east = ONOSCluster( 'east', topo=etopo, ipBase='192.168.123.0/24',
                        nat='enat0' )
    west = ONOSCluster( 'west', topo=wtopo, ipBase='192.168.124.0/24',
                        nat='wnat0' )

    northEast = ONOSCluster ('north_east', topo=netopo, ipBase='192.168.220.0/24', nat='nenat0' )
    northWest = ONOSCluster ('north_west', topo=nwtopo, ipBase='192.168.221.0/24', nat='nwnat0' )
    south = ONOSCluster ('south', topo=stopo, ipBase='192.168.222.0/24', nat='snat0' )
    
    # Data network topology
    print "TOPO"
    topo = MyTopo()
    # Create network
    net = Mininet( topo=topo, switch=MultiSwitch, controller=[ east, west, northEast, northWest, south ] )
    # Assign switches to controllers
    count = len( net.switches )

    cArray = [ east, west, northEast, northWest, south ] #, northEast, northWest, south ]
    controllersCount = len(cArray)
    a = 1
    for i, switch in enumerate( net.switches ):
    #    switch.controller = cArray[i % cArrayLen]    
    #    switch.controller = east if i < count/2 else west
    #   if i  >= a * count / cArrayLen: 
    #       a = a + 1
        
        switch.controller = cArray[int(controllersCount * i / count)]
    # Start up network
    net.start()
    ONOSCLI( net )  # run our special unified Mininet/ONOS CLI
    net.stop()

# Add a "controllers" command to ONOSCLI

def do_controllers( self, line ):
    "List controllers assigned to switches"
    cmap = {}
    for s in self.mn.switches:
        c = getattr( s, 'controller', None ).name
        cmap.setdefault( c, [] ).append( s.name )
    for c in sorted( cmap.keys() ):
        switches = ' '.join( cmap[ c ] )
        print '%s: %s' % ( c, switches )

ONOSCLI.do_controllers = do_controllers


if __name__ == '__main__':
    run()
