
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
def writeHost(f,Host):

    #extrapolate each attribute from the touples
    Name = Host[1]["Name"]
    Os  = Host[1]["Os"]
    Ram = Host[1]["Ram"]
    Ip  = Host[1]["Ip"]
    Netmask = Host[1]["Netmask"]
    IpTrn = Ip.split(".")[0] + "." + Ip.split(".")[1] + "." + Ip.split(".")[2]

    print("adding an host to the vagrant file")

    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")

    if Host[0] is 0:
        f.write(Name + ".vm.network \"private_network\", ip: \"" + Ip +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: true\n")
    if Host[0] is 1:
        f.write(Name + ".vm.network \"private_network\", ip: \"" + Ip +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: true\n")
    if Host[0] is 2:
        f.write(Name + ".vm.network \"private_network\", ip: \"" + Ip +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-3\", auto_config: true\n")
    
    
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started for " + Name + "\"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
    f.write("sudo route add -net " + IpTrn+ ".0 netmask " + Netmask + " gw " + IpTrn+ ".254 dev eth1\n")
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")




#this function write in the vagrant file a new Router
def writeRouter(f,Router):

    #extrapolate each attribute from the touples
    Name = Router[1]["Name"]
    Ram = Router[1]["Ram"]
    Os  = Router[1]["Os"]
    IpEth1 = Router[1]["IpEth1"]
    IpEth2 = Router[1]["IpEth2"]
    IpEth3 = Router[1]["IpEth3"]
    IpEth1Trn = IpEth1.split(".")[0] + "." + IpEth1.split(".")[1] + "." + IpEth1.split(".")[2]
    IpEth2Trn = IpEth2.split(".")[0] + "." + IpEth2.split(".")[1] + "." + IpEth2.split(".")[2]
    IpEth3Trn = IpEth3.split(".")[0] + "." + IpEth3.split(".")[1] + "." + IpEth3.split(".")[2]

    print("adding a router to the vagrant file")

    f.write("config.vm.define \""+ Name +"\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \""+ Name +"\"\n")

    if Router[0] is 3:
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-1\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-3\", auto_config: false\n")
    if Router[0] is 4:
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-2\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-1\", auto_config: false\n")
    if Router[0] is 5:
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-3\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-3\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-2\", auto_config: false\n")  

    f.write(Name + ".vm.provision \"shell\", inline: <<-SHELL\n")
    f.write("echo \" Quagga "+ Name +" start installing\"\n")
    f.write("#sudo sysctl -w net.ipv4.ip_forward=1\n")
    f.write("sudo apt-get update\n")
    f.write("sudo apt-get install quagga quagga-doc traceroute\n")
    f.write("sudo cp /usr/share/doc/quagga/examples/zebra.conf.sample /etc/quagga/zebra.conf\n")
    f.write("sudo cp /usr/share/doc/quagga/examples/ospfd.conf.sample /etc/quagga/ospfd.conf\n")
    f.write("sudo chown quagga.quaggavty /etc/quagga/*.conf\n")
    f.write("sudo /etc/init.d/quagga start\n")
    f.write("sudo sed -i s'/zebra=no/zebra=yes/' /etc/quagga/daemons\n")
    f.write("sudo sed -i s'/ospfd=no/ospfd=yes/' /etc/quagga/daemons\n")
    f.write("sudo echo 'VTYSH_PAGER=more' >>/etc/environment\n")
    f.write("sudo echo 'export VTYSH_PAGER=more' >>/etc/bash.bashrc\n")
    f.write("sudo /etc/init.d/quagga restart\n")
    f.write("echo \"Routing Protocol ospf Configuration Started\"\n")
    f.write("sudo vtysh -c '\n")
    f.write("configure terminal\n")
    f.write("router ospf\n")
    f.write("network " + IpEth1Trn + ".0/24 area 0.0.0.0\n")
    f.write("network " + IpEth2Trn + ".0/24 area 0.0.0.0\n") 
    f.write("network " + IpEth3Trn + ".0/24 area 0.0.0.0\n") 
    f.write("exit\n")
    f.write("interface eth1\n")
    f.write("ip address " + IpEth1 + "/24\n")
    f.write("exit\n")
    f.write("interface eth2\n")
    f.write("ip address " + IpEth2 + "/24\n")
    f.write("exit\n")
    f.write("interface eth3\n")
    f.write("ip address " + IpEth3 + "/24\n")
    f.write("do write\n")
    f.write("exit\n")
    f.write("exit\n")
    f.write("ip forwarding\n")
    f.write("exit'\n")
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write("# " + Name + ".vm.provision \"shell\", path: \"common.sh\"\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")



#the following is a fake graph that i used for testing
#instead of typing everytime the input in the command line
host1 = (1,{
  "Name":"hostbanana",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "Ip": "192.168.1.1",
  "Netmask": "255.255.255.0"
})
host2 = (2,{
  "Name":"hostmela",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "Ip": "192.168.2.1",
  "Netmask": "255.255.255.0"
})
host3 = (3,{
  "Name":"hostpera",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "Ip": "192.168.3.1",
  "Netmask": "255.255.255.0"
})

rout1 = (4,{
  "Name":"routerjack",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "IpEth1": "192.168.1.254",
  "IpEth2": "192.168.100.1",
  "IpEth3": "192.168.101.2"
})
rout2 = (5,{
  "Name":"routersteve",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "IpEth1": "192.168.2.254",
  "IpEth2": "192.168.100.2",
  "IpEth3": "192.168.102.2"
})
rout3 = (6,{
  "Name":"ruoterjhon",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "Ip": "192.168.1.1",
  "IpEth1": "192.168.3.254",
  "IpEth2": "192.168.101.1",
  "IpEth3": "192.168.102.1"
})

fakeNet = [host1,host2,host3,rout1,rout2,rout3]

def main():
    VagrantFile = open("VagrantfileOFFICIALE", "w")

    #read the data structure from input
    #Network = G.nodes.data():
    Network = fakeNet

    #first, let's write the beginnig of the VagrantFile
    BeginVagrantFile(VagrantFile)


    #second, let's write each device with his feature
    #this topology has 3 hosts and 3 routers
    #call the respective function to "populate" the vagrant file

    for device in Network: 
        typeOfDevice = device[1]["Type"]
        print("the device is a " + typeOfDevice)

        if typeOfDevice is "Router":
            writeRouter(VagrantFile,device)


    for device in Network:
        typeOfDevice = device[1]["Type"]
        print("the device is a " + typeOfDevice)

        if typeOfDevice is "Host":
            writeHost(VagrantFile,device)

    VagrantFile.write("end\n")
    VagrantFile.close()


main()
