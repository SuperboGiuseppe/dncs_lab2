import ipcalc 

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f):
    print("writing the beginning of the vagrant file")
    f.write("# -*- mode: ruby -*- \n# vi: set ft=ruby :\n\n")
    f.write("#All Vagrant configuration is done below. The 2 in Vagrant.configure\n#configures the configuration version we support older styles for\n#backwards compatibility. Please don't change it unless you know what\n#you're doing.\n")
    f.write("Vagrant.configure(\"2\") do |config|\n")
    f.write("config.vm.box_check_update = true\n")
    f.write("config.vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.customize [\"modifyvm\", :id, \"--usb\", \"on\"]\n")
    f.write("vb.customize [\"modifyvm\", :id, \"--usbehci\", \"off\"]\n")
    f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc2\", \"allow-all\"]\n")
    f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc3\", \"allow-all\"]\n")
    f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc4\", \"allow-all\"]\n")
    f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc5\", \"allow-all\"]\n")
    f.write("vb.cpus = 1\n")
    f.write("end\n")


#this function write in the vagrant file a new PC host
def writeHost(f, Host, edges, network):

    Id = Host["id"]
    Name = Host["label"]
    Os  = Host["vm_image"]
    Ram = Host["ram"]
    N_Cpus = Host["n_cpus"]
    CustumScript = Host["custom_script"]
    Ip = Host["network_interfaces"][0]["ip_address"]
    Netmask = Host["network_interfaces"][0]["netmask"]
    Interface = Host["network_interfaces"][0]["name_interface"]
    EdgeReference = Host["network_interfaces"][0]["edge"]
    UplinkBandwidth = 0
    DownlinkBandwidth = 0
    for edge in edges:
      if EdgeReference[0] == edge["from"] and EdgeReference[1] == edge["to"]:
        UplinkBandwidth = edge["bandwidth_up"]
        DownlinkBandwidth = edge["bandwidth_down"]
    IpNoSub = Ip.split("/")[0]
    Network = ipcalc.Network(Ip)
    IpNet = Network.network()


    IpRouter2 = network[1]["network_interfaces"][0]["ip_address"]
    NetmaskRouter2 = network[1]["network_interfaces"][0]["netmask"]
    NetworkRouter2 = ipcalc.Network(IpRouter2)
    IpNetRouter2 = str(NetworkRouter2.network())
    """
    Ip2 = Topology[4][1]["Network"][0]["Ip"]
    Mask2 = Topology[4][1]["Network"][0]["Netmask"]
    Network2 = ipcalc.Network(Ip2)
    IpNet2 = str(Network2.network())
    """

    IpRouter1_1 = network[0]["network_interfaces"][0]["ip_address"]
    NetmaskRouter1_1 = network[0]["network_interfaces"][0]["netmask"]
    NetworkRouter1_1 = ipcalc.Network(IpRouter1_1)
    IpNetRouter1_1 = str(NetworkRouter1_1.network())
    """
    Ip3 = Topology[3][1]["Network"][0]["Ip"]
    Mask3 = Topology[3][1]["Network"][0]["Netmask"]
    Network3 = ipcalc.Network(Ip3)
    IpNet3 = str(Network3.network())
    """

    IpRouter1_2 = network[0]["network_interfaces"][1]["ip_address"]
    NetmaskRouter1_2 = network[0]["network_interfaces"][1]["netmask"]
    NetworkRouter1_2 = ipcalc.Network(IpRouter1_2)
    IpNetRouter1_2 = str(NetworkRouter1_2.network())
    """
    Ip4 = Topology[3][1]["Network"][1]["Ip"]
    Mask4 = Topology[3][1]["Network"][1]["Netmask"]
    Network4 = ipcalc.Network(Ip4)
    IpNet4 = str(Network4.network())
    """

    IpSwitch_1 = network[2]["network_interfaces"][0]["ip_address"]
    NetmaskSwitch_1 = network[2]["network_interfaces"][0]["netmask"]
    NetworkSwitch_1 = ipcalc.Network(IpSwitch_1)
    IpNetSwitch_1 = str(NetworkSwitch_1.network())
    """
    Ip8 = Topology[5][1]["Network"][0]["Ip"]
    Mask8 = Topology[5][1]["Network"][0]["Netmask"]
    Network8 = ipcalc.Network(Ip8)
    IpNet8 = str(Network8.network())
    """

    IpSwitch_2 = network[2]["network_interfaces"][1]["ip_address"]
    NetmaskSwitch_2 = network[2]["network_interfaces"][1]["netmask"]
    NetworkSwitch_2 = ipcalc.Network(IpSwitch_2)
    IpNetSwitch_2 = str(NetworkSwitch_2.network())
    """
    Ip12 = Topology[5][1]["Network"][1]["Ip"]
    Mask12 = Topology[5][1]["Network"][1]["Netmask"]
    Network12 = ipcalc.Network(Ip12)
    IpNet12 = str(Network12.network())
    """

    if Id == 4:
      Gateway = IpSwitch_1.split("/")[0]

    if Id == 5:
      Gateway = IpSwitch_2.split("/")[0]

    if Id == 6:
      Gateway = IpRouter2.split("/")[0]

    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os +"\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")
    if Id == 4:
      f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub + "\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_host_" + Name + "\", auto_config: true\n")
    if Id == 5:
      f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub + "\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_host_" + Name + "\", auto_config: true\n")
    if Id == 6:
      f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub + "\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: true\n") 
    
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started for " + Name + "\"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")

    f.write("sudo route add -net " + IpNetRouter2 + " netmask " + NetmaskRouter2 + " gw " + Gateway + " dev " + Interface + "\n")
    f.write("sudo route add -net " + IpNetRouter1_1 + " netmask " + NetmaskRouter1_1 + " gw " + Gateway + " dev " + Interface + "\n")
    f.write("sudo route add -net " + IpNetRouter1_2 + " netmask " + NetmaskRouter1_2 + " gw " + Gateway + " dev " + Interface + "\n")  

    if Id == 4: 
      f.write("sudo route add -net "+ IpNetSwitch_2 + " netmask " + NetmaskSwitch_2 + " gw " + Gateway + " dev " + Interface + "\n")
    if Id == 5:
      f.write("sudo route add -net " + IpNetSwitch_1 + " netmask " + NetmaskSwitch_1 + " gw " + Gateway + " dev " + Interface + "\n")
    if Id == 6: 
      f.write("sudo route add -net " + IpNetSwitch_1 + " netmask " + NetmaskSwitch_1 + " gw " + Gateway + " dev " + Interface + "\n")
      f.write("sudo route add -net " + IpNetSwitch_2 + " netmask " + NetmaskSwitch_2 + " gw " + Gateway + " dev " + Interface + "\n")
    
    f.write('cd /home/vagrant\n')
    f.write('git clone https://github.com/magnific0/wondershaper.git\n')
    f.write('cd wondershaper\n')
    if UplinkBandwidth > 0 or DownlinkBandwidth > 0:
      f.write('sudo ./wondershaper -a ' + Interface)
      if DownlinkBandwidth > 0:
        f.write(' -d ' + str(DownlinkBandwidth))
      if UplinkBandwidth > 0:
        f.write(' -u ' + str(UplinkBandwidth))
      f.write('\n')
    f.write(CustumScript + " \n")  #here there is the custum script
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    if Id == 4:
      f.write(Name + ".vm.provision \"shell\", inline: <<-SHELL\n")
      f.write("echo \"Installation of Web-Server\"\n")
      f.write("sudo apt-get update\n")
      f.write("sudo apt-get install -y apache2\n")
      f.write("echo \"Web-ServerServer is installed and Runing\"\n")
      f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + str(Ram) + "\n")
    f.write("vb.cpus = " + str(N_Cpus) + "\n")
    f.write("end\n")
    f.write("end\n")




#this function write in the vagrant file a new Router
def writeRouter(f, Router, edges, network):

    Id = Router["id"]
    Name = Router["label"]
    Os  = Router["vm_image"]
    Ram = Router["ram"]
    N_Cpus = Router["n_cpus"]

    Ip1 = Router["network_interfaces"][0]["ip_address"]
    Netmask1 = Router["network_interfaces"][0]["netmask"]
    Interface1 = Router["network_interfaces"][0]["name_interface"]
    EdgeReference1 = Router["network_interfaces"][0]["edge"]
    UplinkBandwidth1 = 0
    DownlinkBandwidth1 = 0
    for edge in edges:
      if EdgeReference1[0] == edge["from"] and EdgeReference1[1] == edge["to"]:
        UplinkBandwidth1 = edge["bandwidth_up"]
        DownlinkBandwidth1 = edge["bandwidth_down"]
    IpNoSub1 = Ip1.split("/")[0]
    NetmaskAbbr1 = Ip1.split("/")[1]

    Ip2 = Router["network_interfaces"][1]["ip_address"]
    Netmask2 = Router["network_interfaces"][1]["netmask"]
    Interface2 = Router["network_interfaces"][1]["name_interface"]
    EdgeReference2 = Router["network_interfaces"][1]["edge"]
    UplinkBandwidth2 = 0
    DownlinkBandwidth2 = 0
    for edge in edges:
      if EdgeReference2[0] == edge["from"] and EdgeReference2[1] == edge["to"]:
        UplinkBandwidth2 = edge["bandwidth_up"]
        DownlinkBandwidth2 = edge["bandwidth_down"]
    IpNoSub2 = Ip2.split("/")[0]
    NetmaskAbbr2 = Ip2.split("/")[1]

    CustomScript = Router["custom_script"]

    if Id == 1: 
      tag = "1"
    if Id == 2: 
      tag = "2"  

    IpRouter2 = network[1]["network_interfaces"][0]["ip_address"]
    NetmaskRouter2 = network[1]["network_interfaces"][0]["netmask"]
    NetworkRouter2 = ipcalc.Network(IpRouter2)
    IpNetRouter2 = str(NetworkRouter2.network())
    """
    Ip2 = Topology[4][1]["Network"][0]["Ip"]
    Mask2 = Topology[4][1]["Network"][0]["Netmask"]
    Network2 = ipcalc.Network(Ip2)
    IpNet2 = str(Network2.network())
    """

    IpRouter1_1 = network[0]["network_interfaces"][0]["ip_address"]
    NetmaskRouter1_1 = network[0]["network_interfaces"][0]["netmask"]
    NetworkRouter1_1 = ipcalc.Network(IpRouter1_1)
    IpNetRouter1_1 = str(NetworkRouter1_1.network())
    """
    Ip3 = Topology[5][1]["Network"][2]["Ip"]
    Mask3 = Topology[5][1]["Network"][2]["Netmask"]
    Network3 = ipcalc.Network(Ip3)
    IpNet3 = str(Network3.network())
    """

    IpSwitch_1 = network[2]["network_interfaces"][0]["ip_address"]
    NetmaskSwitch_1 = network[2]["network_interfaces"][0]["netmask"]
    NetworkSwitch_1 = ipcalc.Network(IpSwitch_1)
    IpNetSwitch_1 = str(NetworkSwitch_1.network())
    
    """
    Ip8 = Topology[5][1]["Network"][0]["Ip"]
    Mask8 = Topology[5][1]["Network"][0]["Netmask"]
    Network8 = ipcalc.Network(Ip8)
    IpNet8 = str(Network8.network())
    """

    IpSwitch_2 = network[2]["network_interfaces"][1]["ip_address"]
    NetmaskSwitch_2 = network[2]["network_interfaces"][1]["netmask"]
    NetworkSwitch_2 = ipcalc.Network(IpSwitch_2)
    IpNetSwitch_2 = str(NetworkSwitch_2.network())
    
    """
    Ip12 = Topology[5][1]["Network"][1]["Ip"]
    Mask12 = Topology[5][1]["Network"][1]["Netmask"]
    Network12 = ipcalc.Network(Ip12)
    IpNet12 = str(Network12.network())
    """

    GatewaySwitch = network[2]["network_interfaces"][2]["ip_address"]
    GatewaySwitch = GatewaySwitch.split("/")[0]

    GatewayRouter1 = network[0]["network_interfaces"][1]["ip_address"]
    GatewayRouter1 = GatewayRouter1.split("/")[0]

    GatewayRouter2 = network[1]["network_interfaces"][1]["ip_address"]
    GatewayRouter2 = GatewayRouter2.split("/")[0]

    f.write("config.vm.define \"" + Name+ "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")

    f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub1 + "\", netmask: \"" + Netmask1 + "\", virtualbox__intnet: \"broadcast_router-south-" + tag + "\", auto_config: true\n")
    f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub2 + "\", netmask: \"" + Netmask2 + "\", virtualbox__intnet: \"broadcast_router-inter\", auto_config: true\n")
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started\"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")

    if Id == 1: 
      f.write("sudo route add -net " + IpRouter2 + " netmask " + NetmaskRouter2 + " gw " + GatewayRouter2 + " dev " + Interface2 + "\n")
      f.write("sudo route add -net " + IpSwitch_1 + " netmask " + NetmaskSwitch_1 + " gw " + GatewaySwitch + " dev " + Interface1 + "\n")
      f.write("sudo route add -net " + IpSwitch_2 + " netmask " + NetmaskSwitch_2 + " gw " + GatewaySwitch + " dev " + Interface1 + "\n")
    if Id == 2: 
      f.write("sudo route add -net " + IpRouter1_1 + " netmask " + NetmaskRouter1_1 + " gw " + GatewayRouter1 + " dev " + Interface2 + "\n")
      f.write("sudo route add -net " + IpSwitch_1 + " netmask " + NetmaskSwitch_1 + " gw " + GatewayRouter1 + " dev " + Interface2 + "\n")
      f.write("sudo route add -net " + IpSwitch_2 + " netmask " + NetmaskSwitch_2 + " gw " + GatewayRouter1 + " dev " + Interface2 + "\n")

    f.write('cd /home/vagrant\n')
    f.write('git clone https://github.com/magnific0/wondershaper.git\n')
    f.write('cd wondershaper\n')
    if UplinkBandwidth1 > 0 or DownlinkBandwidth1 > 0:
      f.write('sudo ./wondershaper -a ' + Interface1)
      if DownlinkBandwidth1 > 0:
        f.write(' -d ' + str(DownlinkBandwidth1))
      if UplinkBandwidth1 > 0:
        f.write(' -u ' + str(UplinkBandwidth1))
      f.write('\n')

    if UplinkBandwidth2 > 0 or DownlinkBandwidth2 > 0:
      f.write('sudo ./wondershaper -a ' + Interface2)
      if DownlinkBandwidth2 > 0:
        f.write(' -d ' + str(DownlinkBandwidth2))
      if UplinkBandwidth2 > 0:
        f.write(' -u ' + str(UplinkBandwidth2))
      f.write('\n')
    f.write(CustomScript + " \n") #here there is the custum script
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")

#this function write in the vagrant file a new Router
def writeSwitch(f, Switch, edges, network):

    Id = Switch["id"]
    Name = Switch["label"]
    Ram = Switch["ram"]
    N_Cpus = Switch["n_cpus"]
    Os  = Switch["vm_image"]
    CustomScript = Switch["custom_script"]

    IpA = Switch["network_interfaces"][0]["ip_address"]
    NetmaskA = Switch["network_interfaces"][0]["netmask"]
    InterfaceA = Switch["network_interfaces"][0]["name_interface"]
    EdgeReferenceA = Switch["network_interfaces"][0]["edge"]
    UplinkBandwidthA = 0
    DownlinkBandwidthA = 0
    for edge in edges:
      if EdgeReferenceA[0] == edge["from"] and EdgeReferenceA[1] == edge["to"]:
        UplinkBandwidthA = edge["bandwidth_up"]
        DownlinkBandwidthA = edge["bandwidth_down"]

    IpB = Switch["network_interfaces"][1]["ip_address"]
    NetmaskB = Switch["network_interfaces"][1]["netmask"]
    InterfaceB = Switch["network_interfaces"][1]["name_interface"]
    EdgeReferenceB = Switch["network_interfaces"][1]["edge"]
    UplinkBandwidthB = 0
    DownlinkBandwidthB = 0
    for edge in edges:
      if EdgeReferenceB[0] == edge["from"] and EdgeReferenceB[1] == edge["to"]:
        UplinkBandwidthB = edge["bandwidth_up"]
        DownlinkBandwidthB = edge["bandwidth_down"]

    IpSW = Switch["network_interfaces"][2]["ip_address"]
    NetmaskSW = Switch["network_interfaces"][2]["netmask"]
    InterfaceSW = Switch["network_interfaces"][2]["name_interface"]
    EdgeReferenceSW = Switch["network_interfaces"][2]["edge"]
    UplinkBandwidthSW = 0
    DownlinkBandwidthSW = 0
    for edge in edges:
      if EdgeReferenceSW[0] == edge["from"] and EdgeReferenceSW[1] == edge["to"]:
        UplinkBandwidthSW = edge["bandwidth_up"]
        DownlinkBandwidthSW = edge["bandwidth_down"]

    Gateway = network[0]["network_interfaces"][0]["ip_address"]
    Gateway = Gateway.split("/")[0]

    IpRouter2 = network[1]["network_interfaces"][0]["ip_address"]
    NetmaskRouter2 = network[1]["network_interfaces"][0]["netmask"]
    NetworkRouter2 = ipcalc.Network(IpRouter2)
    IpNetRouter2 = str(NetworkRouter2.network())
    
    """
    Ip2 = Topology[4][1]["Network"][0]["Ip"]
    Mask2 = Topology[4][1]["Network"][0]["Netmask"]
    Network2 = ipcalc.Network(Ip2)
    IpNet2 = str(Network2.network())
    """

    IpRouter1_2 = network[0]["network_interfaces"][1]["ip_address"]
    NetmaskRouter1_2 = network[0]["network_interfaces"][1]["netmask"]
    NetworkRouter1_2 = ipcalc.Network(IpRouter1_2)
    IpNetRouter1_2 = str(NetworkRouter1_2.network())
    """
    Ip4 = Topology[3][1]["Network"][1]["Ip"]
    Mask4 = Topology[3][1]["Network"][1]["Netmask"]
    Network4 = ipcalc.Network(Ip4)
    IpNet4 = str(Network4.network())
    """

    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os +"\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")
    f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: false\n")
    f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_host_" + network[0]["label"] + "\", auto_config: false\n")
    f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_host_" + network[1]["label"] + "\", auto_config: false\n")
    f.write(Name + ".vm.provision \"shell\", inline: <<-SHELL\n")
    f.write("echo \"OpenVSwitch Installation is started\"\n")
    f.write("apt-get update\n")
    f.write("apt-get install -y tcpdump\n")
    f.write("apt-get install -y openvswitch-common openvswitch-switch apt-transport-https ca-certificates curl software-properties-common\n")
    f.write("echo \"OpenVSwitch Bridge Configuration Started\"\n")
    f.write("sudo ovs-vsctl add-br SW1\n")
    f.write("sudo ovs-vsctl add-br HA\n")
    f.write("sudo ovs-vsctl add-br HB\n")
    f.write("sudo ovs-vsctl add-port SW1 eth1\n")
    f.write("sudo ovs-vsctl add-port HA eth2\n")
    f.write("sudo ovs-vsctl add-port HB eth3\n")
    f.write("echo \"Bridge configuration END\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"OpenVSwitch Ip addressing is started\"\n")
    f.write("sudo ifconfig SW1 " + IpSW + "\n")
    f.write("sudo ifconfig HA " + IpA + "\n")
    f.write("sudo ifconfig HB " + IpB + "\n")
    f.write("sudo ifconfig SW1 up\n")
    f.write("sudo ifconfig HA up\n")
    f.write("sudo ifconfig HB up\n")
    f.write("sudo ifconfig eth1 up\n")
    f.write("sudo ifconfig eth2 up\n")
    f.write("sudo ifconfig eth3 up\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
    f.write("sudo route add -net " + IpRouter2 +" netmask " + NetmaskRouter2 + " gw " + Gateway + " dev " + InterfaceSW + "\n")
    f.write("sudo route add -net " + IpRouter1_2 +" netmask " + NetmaskRouter1_2 + " gw " + Gateway + " dev " + InterfaceSW + "\n")

    f.write('cd /home/vagrant\n')
    f.write('git clone https://github.com/magnific0/wondershaper.git\n')
    f.write('cd wondershaper\n')
    if UplinkBandwidthA > 0 or DownlinkBandwidthA > 0:
      f.write('sudo ./wondershaper -a ' + InterfaceA)
      if DownlinkBandwidthA > 0:
        f.write(' -d ' + str(DownlinkBandwidthA))
      if UplinkBandwidthA > 0:
        f.write(' -u ' + str(UplinkBandwidthA))
      f.write('\n')

    if UplinkBandwidthB > 0 or DownlinkBandwidthB > 0:
      f.write('sudo ./wondershaper -a ' + InterfaceB)
      if DownlinkBandwidthB > 0:
        f.write(' -d ' + str(DownlinkBandwidthB))
      if UplinkBandwidthB > 0:
        f.write(' -u ' + str(UplinkBandwidthB))
      f.write('\n')
    
    if UplinkBandwidthSW > 0 or DownlinkBandwidthSW > 0:
      f.write('sudo ./wondershaper -a ' + InterfaceSW)
      if DownlinkBandwidthSW > 0:
        f.write(' -d ' + str(DownlinkBandwidthSW))
      if UplinkBandwidth3 > 0:
        f.write(' -u ' + str(UplinkBandwidthSW))
      f.write('\n')

    f.write(CustomScript + " \n") #here there is the custum script
    f.write("echo \"Configuration END\"\n")
    f.write("echo \""+ Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram +"\n")
    f.write("end\n")
    f.write("end\n")
       
        

    



"""
#the following is a fake graph that i used for testing
#instead of typing everytime the input in the command line
host1 = (1,{
  "Id" : 1,
  "Name":"host1",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "172.16.8.5/22",
    "Netmask": "255.255.252.0",
    "Interface" : "eth1"
  }]
})
host2 = (2,{
  "Id" : 2,
  "Name":"host2",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "172.16.12.5/22",
    "Netmask": "255.255.252.0",
    "Interface" : "eth1"
  }]
})
host3 = (3,{
  "Id" : 3,
  "Name":"host3",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "172.16.2.5/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  }]
})

rout1 = (4,{
  "Id" : 4,
  "Name": "router1",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "172.16.3.5/28",
    "Netmask": "255.255.255.240",
    "Interface" : "eth1"
  },{
    "Ip": "172.16.4.9/30",
    "Netmask": "255.255.255.252",
    "Interface" : "eth2"
  }]
})
rout2 = (5,{
  "Id" : 5,
  "Name":"router2",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "172.16.2.10/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  },{
    "Ip": "172.16.4.10/30",
    "Netmask": "255.255.255.252",
    "Interface" : "eth2"
  }]
})
switch1 = (6,{
  "Id" : 6,
  "Name":"switch1",
  "Type": "Switch",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "172.16.8.10/22",
    "Netmask": "255.255.252.0",
    "Interface" : "HA"
  },{
    "Ip": "172.16.12.10/22",
    "Netmask": "255.255.252.0",
    "Interface" : "HB"
  },{
    "Ip": "172.16.3.2/28",
    "Netmask": "255.255.255.240",
    "Interface" : "SW1"
  }]
})

fakeNet = [host1,host2,host3,rout1,rout2,switch1]
"""

def html_to_vagrantfile(nodes, edges):
    VagrantFile = open("Vagrantfile", "w")

    BeginVagrantFile(VagrantFile)
    for node in nodes:
      if node["type"] == "router":
        writeRouter(VagrantFile, node, edges, nodes)
      if node["type"] == "switch":
        writeSwitch(VagrantFile, node, edges, nodes)
      if node["type"] == "host":
        writeHost(VagrantFile, node, edges, nodes)        
    VagrantFile.write('end\n')
    VagrantFile.close()


    #read the data structure from input
    #Network = G.nodes.data():
    #Network = fakeNet
    #N.B per Luca, Network è già la lista dei nodi che puoi esplorare

    #first, let's write the beginnig of the VagrantFile
    #BeginVagrantFile(VagrantFile,Network)


    #second, let's write each device with his feature
    #this topology has 3 hosts, 1 switch and 3 routers
    #for device in Network:
        #call the respective function to "populate" the vagrant file
    #    typeOfDevice = device[1]["Type"]
    #    print("the device is a " + typeOfDevice)

    #    if typeOfDevice is "Router":
    #        writeRouter(VagrantFile,device,Network)

    #for device in Network:
        #call the respective function to "populate" the vagrant file
    #    typeOfDevice = device[1]["Type"]
    #    print("the device is a " + typeOfDevice)
    #    if typeOfDevice is "Switch":
    #        writeSwitch(VagrantFile,device,Network)


    #for device in Network:
        #call the respective function to "populate" the vagrant file
    #    typeOfDevice = device[1]["Type"]
    #    print("the device is a " + typeOfDevice)
    #    if typeOfDevice is "Host":
    #        writeHost(VagrantFile,device,Network)


