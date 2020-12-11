import ipcalc 

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f,Network):
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
def writeHost(f,Host,Topology):

    print("adding an host to the vagrant file")

    #extrapolate each attribute from the touples
    Id = Host[1]["Id"]
    Name = Host[1]["Name"]
    Os  = Host[1]["Os"]
    Ram = Host[1]["Ram"]

    Ip = Host[1]["Network"][0]["Ip"]
    Netmask = Host[1]["Network"][0]["Netmask"]
    Interface = Host[1]["Network"][0]["Interface"]
    IpNoSub = Ip.split("/")[0]

    Network = ipcalc.Network(Ip)
    IpNet = Network.network()

    for x in Network:
      Gateway = str(x)

    #IpA = Topology[0][1]["Network"][0]["Ip"]
    #NetmaskA = Topology[0][1]["Network"][0]["Netmask"]
    #InterfaceA = Topology[0][1]["Network"][0]["Interface"]
    #IpNoSubA = Ip.split("/")[0]
    #Network = ipcalc.Network(IpA)
    #IpNetA = Network.network()

    #IpB = Topology[1][1]["Network"][0]["Ip"]
    #NetmaskB = Topology[1][1]["Network"][0]["Netmask"]
    #InterfaceB = Topology[1][1]["Network"][0]["Interface"]
    #IpNoSubB = Ip.split("/")[0]
    #Network = ipcalc.Network(IpB)
    #IpNetB = Network.network()

    #IpC = Topology[2][1]["Network"][0]["Ip"]
    #NetmaskC = Topology[2][1]["Network"][0]["Netmask"]
    #InterfaceC = Topology[2][1]["Network"][0]["Interface"]
    #IpNoSubC = Ip.split("/")[0]
    #Network = ipcalc.Network(IpC)
    #IpNetC = Network.network()

    Ip2 = Topology[4][1]["Network"][0]["Ip"]
    Mask2 = Topology[4][1]["Network"][0]["Netmask"]
    Network2 = ipcalc.Network(Ip2)
    IpNet2 = Network.network()

    Ip3 = Topology[3][1]["Network"][0]["Ip"]
    Mask3 = Topology[3][1]["Network"][0]["Netmaks"]
    Network3 = ipcalc.Network(Ip3)
    IpNet3 = Network.network()

    Ip4 = Topology[3][1]["Network"][1]["Ip"]
    Mask4 = Topology[3][1]["Network"][1]["Netmask"]
    Network4 = ipcalc.Network(Ip4)
    IpNet4 = Network.network()

    Ip8 = Topology[5][1]["Network"][0]["Ip"]
    Mask8 = Topology[5][1]["Network"][0]["Netmask"]
    Network8 = ipcalc.Network(Ip8)
    IpNet8 = Network.network()

    Ip12 = Topology[4][1]["Network"][1]["Ip"]
    Mask12 = Topology[4][1]["Network"][1]["Netmask"]
    Network12 = ipcalc.Network(Ip12)
    IpNet12 = Network.network()


    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os +"\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")
    f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub + "\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_host_" + Name + "\", auto_config: true\n")
    f.write("#.vm.provision \"shell\", inline: <<-SHELL\n")
    f.write("#echo \"Installation of Lynx Text-Based Browser to access the Web-Server via terminal on " + Name + "\"\n")
    f.write("#sudo apt-get update\n")
    f.write("#sudo apt-get install -y lynx\n")
    f.write("#echo \"Lynx-Browser is installed\"\n")
    f.write("#SHELL\n")
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started for " + Name + "\"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")

    f.write("sudo route add -net " + IpNet2 + " netmask " + Mask2 + " gw " + Gateway + " dev " + Interface + "\n")
    f.write("sudo route add -net " + IpNet3 + " netmask " + Mask3 + " gw " + Gateway + " dev " + Interface + "\n")
    f.write("sudo route add -net " + IpNet4 + " netmask " + Mask4 + " gw " + Gateway + " dev " + Interface + "\n")  

    if Id is 1: 
      f.write("sudo route add -net "+ IpNet12 + " netmask " + Mask12 + " gw " + Gateway + " dev " + Interface + "\n")

    if Id is 2:
      f.write("sudo route add -net " + IpNet8 + " netmask " + Mask8 + " gw " + Gateway + " dev " + Interface + "\n")
      
    if Id is 3: 
      f.write("sudo route add -net " + IpNet8 + " netmask " + Mask8 + " gw " + Gateway + " dev " + Interface + "\n")
      f.write("sudo route add -net " + IpNet12 + " netmask " + Mask12 + " gw " + Gateway + " dev " + Interface + "\n")
    
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")




#this function write in the vagrant file a new Router
def writeRouter(f,Router,Topology):

    #extrapolate each attribute from the touples
    Name = Router[1]["Name"]
    Ram = Router[1]["Ram"]
    Os  = Router[1]["Os"]
    IpEth1 = Router[1]["IpEth1"]
    IpEth2 = Router[1]["IpEth2"]

    IpSwitchEth1 = Network[5][1]["IpEth1"]
    IpSwitchEth1Trn = IpSwitchEth1.split(".")[0] +"."+ IpSwitchEth1.split(".")[1] +"."+ IpSwitchEth1.split(".")[2]

    IpSwitchEth2 = Network[5][1]["IpEth2"]
    IpSwitchEth2Trn = IpSwitchEth2.split(".")[0] +"."+ IpSwitchEth2.split(".")[1] +"."+ IpSwitchEth2.split(".")[2]

    Gw = Network[5][1]["IpEth3"]

    IpRouter2Eth1 = Network[4][1]["IpEth1"]
    IpRouter2Eth1Trn = IpRouter2Eth1.split(".")[0] +"."+ IpRouter2Eth1.split(".")[1] +"."+ IpRouter2Eth1.split(".")[2]

    IpSwitchEth3 = Network[5][1]["IpEth3"]
    IpSwitchEth3Trn = IpSwitchEth3.split(".")[0] +"."+ IpSwitchEth3.split(".")[1] +"."+ IpSwitchEth3.split(".")[2]

    if Router[0] is 4: 
      tmp = "1"
    if Router[0] is 5: 
      tmp = "2"  

    print("adding a router to the vagrant file")
    f.write("config.vm.define \"" + Name+ "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")
    
    if Router[0] is 4:
      f.write(Name + ".vm.network \"private_network\", ip: \"" + IpEth1 + "\", netmask: \"255.255.255.240\", virtualbox__intnet: \"broadcast_router-south-"+tmp+"\", auto_config: true\n")
      f.write(Name + ".vm.network \"private_network\", ip: \"" + IpEth2 + "\",netmask: \"255.255.255.252\", virtualbox__intnet: \"broadcast_router-inter\", auto_config: true\n")
    
    if Router[0] is 5:
      f.write(Name + ".vm.network \"private_network\", ip: \"" + IpEth1 + "\", netmask: \"255.255.255.0\", virtualbox__intnet: \"broadcast_router-south-"+tmp+"\", auto_config: true\n")
      f.write(Name + ".vm.network \"private_network\", ip: \"" + IpEth2 + "\",netmask: \"255.255.255.252\", virtualbox__intnet: \"broadcast_router-inter\", auto_config: true\n")
    

    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started\"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")

    if Router[0] is 4: 
      f.write("sudo route add -net "+IpRouter2Eth1Trn+".0 netmask 255.255.255.0 gw "+Network[4][1]["IpEth2"]+" dev eth2\n")
      f.write("sudo route add -net "+IpSwitchEth1Trn+".0 netmask 255.255.252.0 gw "+Gw+" dev eth1\n")
      f.write("sudo route add -net "+IpSwitchEth2Trn+".0 netmask 255.255.252.0 gw "+Gw+" dev eth1\n")

    if Router[0] is 5: 
      f.write("sudo route add -net "+IpSwitchEth3Trn+".0 netmask 255.255.255.240 gw "+Network[3][1]["IpEth2"]+" dev eth2\n")
      f.write("sudo route add -net "+IpSwitchEth1Trn+".0 netmask 255.255.252.0 gw "+Network[3][1]["IpEth2"]+" dev eth2\n")
      f.write("sudo route add -net "+IpSwitchEth2Trn+".0 netmask 255.255.252.0 gw "+Network[3][1]["IpEth2"]+" dev eth2\n")

    
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")

#this function write in the vagrant file a new Router
def writeSwitch(f,Switch,Topology):

    #extrapolate each attribute from the touples
    Name = Switch[1]["Name"]
    Ram = Switch[1]["Ram"]
    Os  = Switch[1]["Os"]

    IpA = Switch[1]["Network"][1]["Ip"]
    NetmaskA = Switch[1]["Network"][1]["Netmask"]
    InterfaceA = Switch[1]["Network"][1]["Interface"]

    IpB = Switch[1]["Network"][0]["Ip"]
    NetmaskB = Switch[1]["Network"][0]["Netmask"]
    InterfaceB = Switch[1]["Network"][0]["Interface"]

    IpSW = Switch[1]["Network"][3]["Ip"]
    NetmaskSW = Switch[1]["Network"][3]["Netmask"]
    InterfaceSW = Switch[1]["Network"][3]["Interface"]

    Gateway = Topology[3][1]["Network"][0]["Ip"]
    Gateway = Gateway.split("/")[0]

    Ip2 = Topology[4][1]["Network"][0]["Ip"]
    Mask2 = Topology[4][1]["Network"][0]["Netmask"]
    Network2 = ipcalc.Network(Ip2)
    IpNet2 = Network.network()

    Ip4 = Topology[3][1]["Network"][1]["Ip"]
    Mask4 = Topology[3][1]["Network"][1]["Netmask"]
    Network4 = ipcalc.Network(Ip4)
    IpNet4 = Network.network()


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
    f.write("echo \"Configuration END\"\n")
    f.write("echo \""+ Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    # User can select the desired menmory for the machine. we must allow them
    f.write("vb.memory = " + Ram +"\n")
    f.write("end\n")
    f.write("end\n")
       
        

    



#the following is a fake graph that i used for testing
#instead of typing everytime the input in the command line
host1 = (1,{
  "Id" : 1,
  "Name":"host1",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
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
  "Network" : [{
    "Ip": "172.16.8.10/22",
    "Netmask": "255.255.252.0",
    "Interface" : "HB"
  },{
    "Ip": "172.16.12.10/22",
    "Netmask": "255.255.252.0",
    "Interface" : "HA"
  },{
    "Ip": "172.16.3.2/28",
    "Netmask": "255.255.255.240",
    "Interface" : "SW1"
  }]
})

fakeNet = [host1,host2,host3,rout1,rout2,switch1]

def main():
    VagrantFile = open("VagrantfileSWITCH", "w")

    #read the data structure from input
    #Network = G.nodes.data():
    Network = fakeNet

    #first, let's write the beginnig of the VagrantFile
    BeginVagrantFile(VagrantFile,Network)


    #second, let's write each device with his feature
    #this topology has 3 hosts, 1 switch and 3 routers
    for device in Network:
        #call the respective function to "populate" the vagrant file
        typeOfDevice = device[1]["Type"]
        print("the device is a " + typeOfDevice)

        if typeOfDevice is "Router":
            writeRouter(VagrantFile,device,Network)

    for device in Network:
        #call the respective function to "populate" the vagrant file
        typeOfDevice = device[1]["Type"]
        print("the device is a " + typeOfDevice)
        if typeOfDevice is "Switch":
            writeSwitch(VagrantFile,device,Network)


    for device in Network:
        #call the respective function to "populate" the vagrant file
        typeOfDevice = device[1]["Type"]
        print("the device is a " + typeOfDevice)
        if typeOfDevice is "Host":
            writeHost(VagrantFile,device,Network)

    VagrantFile.write("end\n")
    VagrantFile.close()

main()
