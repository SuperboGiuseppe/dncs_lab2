import ipcalc 
import yaml

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f):
    f.write('Vagrant.configure("2") do |config|\n')
    f.write('config.vm.box_check_update = true\n')
    f.write('config.vm.provider "virtualbox" do |vb|\n')
    f.write('vb.customize ["modifyvm", :id, "--usb", "on"]\n')
    f.write('vb.customize ["modifyvm", :id, "--usbehci", "off"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc4", "allow-all"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc5", "allow-all"]\n')
    f.write('vb.cpus = 1\n')
    f.write('end\n')


def writeServer(f, Server, edges):

    Id = Server[1]["id"]
    Name = Server[1]["label"]
    Ram = Server[1]["Ram"]
    Os  = Server[1]["Os"]
    CustumScript = Server[1]["custom_script"]

    Ip1 = Router[1]["Network"][0]["Ip"]
    Netmask1 = Router[1]["Network"][0]["Netmask"]
    Interface1 = Router[1]["Network"][0]["Interface"]
    IpNoSub1 = Ip1.split("/")[0]
    NetmaskAbbr1 = Ip1.split("/")[1]

    Ip2 = Router[1]["Network"][1]["Ip"]
    Netmask2 = Router[1]["Network"][1]["Netmask"]
    Interface2 = Router[1]["Network"][1]["Interface"]
    IpNoSub2 = Ip2.split("/")[0]
    NetmaskAbbr2 = Ip2.split("/")[1]

    Ip3 = Router[1]["Network"][2]["Ip"]
    Netmask3 = Router[1]["Network"][2]["Netmask"]
    Interface3 = Router[1]["Network"][2]["Interface"]
    IpNoSub3 = Ip3.split("/")[0]
    NetmaskAbbr3 = Ip3.split("/")[1]
    
    Network1 = ipcalc.Network(Ip1)
    IpNet1 = Network1.network()
    for x in Network1:
      Gateway1 = str(x)

    Network2 = ipcalc.Network(Ip2)
    IpNet2 = Network2.network()
    for x in Network2:
      Gateway2 = str(x)

    Network3 = ipcalc.Network(Ip3)
    IpNet3 = Network3.network()
    for x in Network3:
      Gateway3 = str(x)   

    UplinkBandwidth = 0
    DownlinkBandwidth = 0
    for edge in edges:
      if EdgeReference[0] == edge["from"] and EdgeReference[1] == edge["to"]:
        UplinkBandwidth = edge["bandwidth_up"]
        DownlinkBandwidth = edge["bandwidth_down"]
    CustumScript = Server["custom_script"]

    #new stuff
    f.write('config.vm.define "' + Name + '" do |' + Name + '|\n')
    f.write(Name + '.vm.box = "'+ Os +'"\n')
    f.write(Name + '.vm.hostname = "' + Name + '"\n')
    f.write(Name + '.vm.network "private_network", ip: "172.16.3.5", netmask: "255.255.255.240", virtualbox__intnet: "broadcast_router-south-1", auto_config: true\n')
    f.write(Name + '.vm.network "private_network", ip: "172.16.4.9",netmask: "255.255.255.252", virtualbox__intnet: "broadcast_router-inter", auto_config: true\n')
    f.write(Name + '.vm.provision "docker" do |dockerimage|\n')
	f.write('dockerimage.pull_images "nginx"\n')
	f.write('dockerimage.run "nginx"\n')
	f.write('webserver.vm.provision "shell", run: "always", inline: <<-SHELL\n')
	f.write('echo "Static Routig configuration Started"\n')
	f.write('sudo sysctl -w net.ipv4.ip_forward=1\n')
	f.write('sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.4.10 dev eth2\n')
	f.write('sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.3.2 dev eth1\n')
	f.write('sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.3.2 dev eth1\n')

    for edge in edges:
      if UplinkBandwidth > 0 or DownlinkBandwidth > 0:
        f.write('sudo wondershaper -a ' + InterfaceName)
        if DownlinkBandwidth > 0:
          f.write(' -d ' + str(DownlinkBandwidth))
        if UplinkBandwidth > 0:
          f.write(' -u ' + str(UplinkBandwidth))
        f.write('\n')
    #here there is the custum script
    f.write(CustumScript + " \n")

	f.write('echo "Configuration END"\n')
	f.write('echo "' + Name + ' is ready to Use"\n')
	f.write('SHELL\n')
    f.write(Name + '.vm.provider "virtualbox" do |vb|\n')
    f.write('vb.memory = ' + Ram + '\n')
    f.write('end\n')
	f.write('end\n')
    f.write('end\n')


#this function write in the vagrant file a new PC host
def writeHost(f,Host):

  #  print("adding an host to the vagrant file")

    #extrapolate each attribute from the touples
    Id = Host[1]["Id"]
    Name = Host[1]["Name"]
    Ram = Host[1]["Ram"]
    Os  = Host[1]["Os"]
    CustumScript = Host[1]["custom_script"]
    
    Ip = Host[1]["Network"][0]["Ip"]
    Netmask = Host[1]["Network"][0]["Netmask"]
    Interface = Host[1]["Network"][0]["Interface"]
    IpNoSub = Ip.split("/")[0]

    Network = ipcalc.Network(Ip)
    IpNet = Network.network()

    #there must be a more efficient way to calculate this, this one is too trivial
    for x in Network:
      Gateway = str(x)

    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")

    if Id is 4:
        f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: true\n")
    if Id is 5:
        f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: true\n")
    if Id is 6:
        f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-3\", auto_config: true\n")
    
    
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started for " + Name + "\"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
    f.write("sudo route add -net " + str(IpNet) + " netmask " + Netmask + " gw " + Gateway + " dev " + Interface + "\n")





    #newstuff
    f.write('config.vm.define "host-a" do |hosta|\n')
    f.write('hosta.vm.box = "bento/ubuntu-16.04"\n')
    f.write('hosta.vm.hostname = "host-a"\n')
    f.write('hosta.vm.network "private_network", ip: "172.16.8.5", netmask: "255.255.252.0", virtualbox__intnet: "broadcast_host_a", auto_config: true\n')
    f.write('hosta.vm.provision "shell", run: "always", inline: <<-SHELL\n')
	f.write('echo "Static Routig configuration Started for Host--A"\n')
	f.write('sudo sysctl -w net.ipv4.ip_forward=1\n')
	f.write('sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.8.10 dev eth1\n')
    f.write('sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.8.10 dev eth1\n')
    f.write('sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.8.10 dev eth1\n')
    f.write('sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.8.10 dev eth1\n')

    #here there is the custum script
    f.write(CustumScript + " \n")

    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")

def writeSwitch(f,Switch,Topology):

    #extrapolate each attribute from the touples
    Name = Switch[1]["Name"]
    Ram = Switch[1]["Ram"]
    Os  = Switch[1]["Os"]
    CustumScript = Switch[1]["custom_script"]

    IpA = Switch[1]["Network"][0]["Ip"]
    NetmaskA = Switch[1]["Network"][0]["Netmask"]
    InterfaceA = Switch[1]["Network"][0]["Interface"]

    IpB = Switch[1]["Network"][1]["Ip"]
    NetmaskB = Switch[1]["Network"][1]["Netmask"]
    InterfaceB = Switch[1]["Network"][1]["Interface"]

    IpSW = Switch[1]["Network"][2]["Ip"]
    NetmaskSW = Switch[1]["Network"][2]["Netmask"]
    InterfaceSW = Switch[1]["Network"][2]["Interface"]

    Gateway = Topology[3][1]["Network"][0]["Ip"]
    Gateway = Gateway.split("/")[0]

    Ip2 = Topology[4][1]["Network"][0]["Ip"]
    Mask2 = Topology[4][1]["Network"][0]["Netmask"]
    Network2 = ipcalc.Network(Ip2)
    IpNet2 = str(Network2.network())

    Ip4 = Topology[3][1]["Network"][1]["Ip"]
    Mask4 = Topology[3][1]["Network"][1]["Netmask"]
    Network4 = ipcalc.Network(Ip4)
    IpNet4 = str(Network4.network())


    print("adding a switch to the vagrant file")
    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os +"\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")
    f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: false\n")
    f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_host_" + Topology[0][1]["Name"] + "\", auto_config: false\n")
    f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_host_" + Topology[1][1]["Name"] + "\", auto_config: false\n")
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
    f.write("sudo route add -net " + IpNet2 +" netmask " + Mask2 + " gw " + Gateway + " dev " + InterfaceSW + "\n")
    f.write("sudo route add -net " + IpNet4 +" netmask " + Mask4 + " gw " + Gateway + " dev " + InterfaceSW + "\n")

    #here there is the custum script
    f.write(CustumScript + " \n")

    f.write("echo \"Configuration END\"\n")
    f.write("echo \""+ Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    # User can select the desired menmory for the machine. we must allow them
    f.write("vb.memory = " + Ram +"\n")
    f.write("end\n")
    f.write("end\n")


    #newstuff
    f.write('config.vm.define "switch" do |switch|\n')
    f.write('switch.vm.box = "bento/ubuntu-16.04"\n')
    f.write('switch.vm.hostname = "switch"\n')
    f.write('switch.vm.network "private_network", virtualbox__intnet: "broadcast_router-south-1", auto_config: false\n')
    f.write('switch.vm.network "private_network", virtualbox__intnet: "broadcast_host_a", auto_config: false\n')
    f.write('switch.vm.network "private_network", virtualbox__intnet: "broadcast_host_b", auto_config: false\n')
    f.write('switch.vm.provision "shell", inline: <<-SHELL\n')
	f.write('echo "OpenVSwitch Installation is started"\n')
	f.write('apt-get update\n')
	f.write('apt-get install -y tcpdump\n')
	f.write('apt-get install -y openvswitch-common openvswitch-switch apt-transport-https ca-certificates curl software-properties-common\n')
	f.write('echo "OpenVSwitch Bridge Configuration Started"\n')
	f.write('sudo ovs-vsctl add-br SW1\n')
	f.write('sudo ovs-vsctl add-br HA\n')
	f.write('sudo ovs-vsctl add-br HB\n')
	f.write('sudo ovs-vsctl add-port SW1 eth1\n')
	f.write('sudo ovs-vsctl add-port HA eth2\n')
	f.write('sudo ovs-vsctl add-port HB eth3\n')
	f.write('echo "Bridge configuration END"\n')
	f.write('SHELL\n')
	f.write('switch.vm.provision "shell", run: "always", inline: <<-SHELL\n')
	f.write('echo "OpenVSwitch Ip addressing is started"\n')
	f.write('sudo ifconfig SW1 172.16.3.2/28\n')
	f.write('sudo ifconfig HA 172.16.8.10/22\n')
	f.write('sudo ifconfig HB 172.16.12.10/22\n')
	f.write('sudo ifconfig SW1 up\n')
	f.write('sudo ifconfig HA up\n')
	f.write('sudo ifconfig HB up\n')
	f.write('sudo ifconfig eth1 up\n')
	f.write('sudo ifconfig eth2 up\n')
	f.write('sudo ifconfig eth3 up\n')
	f.write('sudo sysctl -w net.ipv4.ip_forward=1\n')
	f.write('sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.3.5 dev SW1\n')
	f.write('sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.3.5 dev SW1\n')
	f.write('echo "Configuration END"\n')
	f.write('echo "Switch is ready to Use"\n')
	f.write('SHELL\n')
	f.write('switch.vm.provider "virtualbox" do |vb|\n')
    f.write('vb.memory = 1024\n')
    f.write('end\n')
    f.write('end\n')



"""
web1 = (1,{
  "Id" : 1,
  "Name":"web1",
  "Os": "ubuntu/xenial64",
  "Ip": "10.0.0.50",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'"
})

db1 = (2,{
  "Id" : 2,
  "Name":"db1",
  "Os": "ubuntu/xenial64",
  "Ip": "10.0.0.51",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'"
})


MyNet = [web1,db1]
"""


def html_to_vagrantfile(nodes, edges):
    VagrantFile = open("Vagrantfile3SERVERS2HOST", "w")

    #read the data structure from input
    #Network = G.nodes.data():
    #file = codecs.open("NetworkGraphs/Template/OSPF_Routing_Template.html", "r", "utf-8")
    #html = file.read()

    #if "nodes = new vis.DataSet(" in html:
    #  listOfDevice = find_between(html, "nodes = new vis.DataSet(" , ")")
    #  print(listOfDevice)
    #  listOfDevice = yaml.load(listOfDevice) 

    #newNet = remap(listOfDevice)

    #Network = MyNet #RICAMBIALA CON NEWNET
    #N.B per Luca, Network è già la lista dei nodi che puoi esplorare

    BeginVagrantFile(VagrantFile)
    for node in nodes:
      if node["type"] == "web":
        writeWebServer(VagrantFile, node, edges)
      if node["type"] == "db":
        writeDatabase(VagrantFile, node, edges)
    
    VagrantFile.close()

