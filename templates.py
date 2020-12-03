from pyvis.network import Network

def template_ospf_routing():
    G = Network()
    G.add_node(0, image="./Images/router.png", label="router-1", shape="image", type="router", network_interfaces=[{"ip_address":"192.168.1.254/24", "netmask":"255.255.255.0", "name_interface":"eth1"}, {"ip_addresses":"192.168.100.1/24", "netmask":"255.255.255.0", "name_interface":"eth2"}, {"ip_addresses":"192.168.101.2/24", "netmask":"255.255.255.0", "name_interface":"eth3"}], vm_image="bento/ubuntu-16.04", ram="1024")
    G.add_node(1, image="./Images/router.png", label="router-2", shape="image", type="router", network_interfaces=[{"ip_address":"192.168.2.254/24", "netmask":"255.255.255.0", "name_interface":"eth1"}, {"ip_addresses":"192.168.100.2/24", "netmask":"255.255.255.0", "name_interface":"eth2"}, {"ip_addresses":"192.168.102.2/24", "netmask":"255.255.255.0", "name_interface":"eth3"}], vm_image="bento/ubuntu-16.04", ram="1024")
    G.add_node(2, image="./Images/router.png", label="router-3", shape="image", type="router", network_interfaces=[{"ip_address":"192.168.3.254/24", "netmask":"255.255.255.0", "name_interface":"eth1"}, {"ip_addresses":"192.168.101.1/24", "netmask":"255.255.255.0", "name_interface":"eth2"}, {"ip_addresses":"192.168.102.1/24", "netmask":"255.255.255.0", "name_interface":"eth3"}], vm_image="bento/ubuntu-16.04", ram="1024")
    G.add_node(3, image="./Images/host.png", label="host-a", shape="image", type="host", network_interfaces=[{"ip_address":"192.168.1.1/24", "netmask":"255.255.255.0", "name_interface":"eth1"}], vm_image="bento/ubuntu-16.04", ram="1024")
    G.add_node(4, image="./Images/host.png", label="host-b", shape="image", type="host", network_interfaces=[{"ip_address":"192.168.2.1/24", "netmask":"255.255.255.0", "name_interface":"eth1"}], vm_image="bento/ubuntu-16.04", ram="1024")
    G.add_node(5, image="./Images/host.png", label="host-c", shape="image", type="host", network_interfaces=[{"ip_address":"192.168.3.1/24", "netmask":"255.255.255.0", "name_interface":"eth1"}], vm_image="bento/ubuntu-16.04", ram="1024")
    G.add_edges([(0,1),(1,2),(2,0),(0,3),(1,4),(2,5)])
    G.show("test.html")
    return G