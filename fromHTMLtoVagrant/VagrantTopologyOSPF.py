import ipcalc 
import codecs
import yaml

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f):

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
def writeHost(f,Host, edges):

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
    f.write(CustumScript + " \n")#here there is the custum script
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")




#this function write in the vagrant file a new Router
def writeRouter(f,Router, edges):

    Id = Router[1]["Id"]
    Name = Router[1]["Name"]
    Ram = Router[1]["Ram"]
    Os  = Router[1]["Os"]
    CustumScript = Router[1]["custom_script"]

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

    f.write("config.vm.define \""+ Name +"\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \""+ Name +"\"\n")

    if Id is 1:
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-1\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-3\", auto_config: false\n")
    if Id is 2:
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-2\", auto_config: false\n")
        f.write(Name + ".vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-inter-1\", auto_config: false\n")
    if Id is 3:
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
    f.write("network " + str(IpNet1) + "/" + NetmaskAbbr1 + " area 0.0.0.0\n")
    f.write("network " + str(IpNet2) + "/" + NetmaskAbbr2 + " area 0.0.0.0\n") 
    f.write("network " + str(IpNet3) + "/" + NetmaskAbbr3 + " area 0.0.0.0\n") 
    f.write("exit\n")
    f.write("interface " + Interface1 + "\n")
    f.write("ip address " + IpNoSub1 + "/" + NetmaskAbbr1 + "\n")
    f.write("exit\n")
    f.write("interface " + Interface2 + "\n")
    f.write("ip address " + IpNoSub2 + "/" + NetmaskAbbr2 + "\n")
    f.write("exit\n")
    f.write("interface " + Interface3 + "\n")
    f.write("ip address " + IpNoSub3 + "/" + NetmaskAbbr3 + "\n")
    f.write("do write\n")
    f.write("exit\n")
    f.write("exit\n")
    f.write("ip forwarding\n")
    f.write("exit'\n")
    f.write(CustumScript + " \n") #here there is the custum script
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
host1 = (4,{
  "Id" : 4,
  "Name":"host1",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.1.1/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  }]
})
host2 = (5,{
  "Id" : 5,
  "Name":"host2",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.2.1/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  }]
})
host3 = (6,{
  "Id" : 6,
  "Name":"host3",
  "Type": "Host",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.3.1/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  }]
})

rout1 = (1,{
  "Id" : 1,
  "Name":"router1",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script": "echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.1.254/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  },{
    "Ip": "192.168.100.1/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth2"
  },{
    "Ip": "192.168.101.2/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth3"
  }]
})
rout2 = (2,{
  "Id" : 2,
  "Name":"router2",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script": "echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.2.254/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  },{
    "Ip": "192.168.100.2/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth2"
  },{
    "Ip": "192.168.102.2/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth3"
  }]
})
rout3 = (3,{
  "Id" : 3,
  "Name":"ruoter3",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script": "echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.3.254/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  },{
    "Ip": "192.168.101.1/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth2"
  },{
    "Ip": "192.168.102.1/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth3"
  }]
})

MyNet = [host1,host2,host3,rout1,rout2,rout3]

def remap(newList):
    print("-------------------")

    for item in newList:
      print("Looking at device " + str(item))
      print("the TYPE is " + item["type"])
      if item["type"] == "router" : 

        for device in MyNet:
          if device[1]["Id"] is item["id"]:
            print("remap of device " + str(device[1]["Id"]) + " to device " + str(item["id"]))
            device[1]["Name"] = item["label"]
            device[1]["Ram"] = item["ram"]
            device[1]["Os"] = item["vm_image"]

            device[1]["Network"][0]["Ip"] = item["network_interfaces"][0]["ip_address"]
            device[1]["Network"][0]["Netmask"] = item["network_interfaces"][0]["netmask"]
            device[1]["Network"][0]["Interface"] = item["network_interfaces"][0]["name_interface"]

            device[1]["Network"][1]["Ip"] = item["network_interfaces"][1]["ip_address"]
            device[1]["Network"][1]["Netmask"] = item["network_interfaces"][1]["netmask"]
            device[1]["Network"][1]["Interface"] = item["network_interfaces"][1]["name_interface"]

            device[1]["Network"][2]["Ip"] = item["network_interfaces"][2]["ip_address"]
            device[1]["Network"][2]["Netmask"] = item["network_interfaces"][2]["netmask"]
            device[1]["Network"][2]["Interface"] = item["network_interfaces"][2]["name_interface"]        

    for item in newList:
      if item["type"] == "host" : 

        for device in MyNet:
           if device[1]["Id"] is item["id"]:
             print("remap of device " + str(device[1]["Id"]) + " to device " + str(item["id"]))
             device[1]["Name"] = item["label"]
             device[1]["Ram"] = item["ram"]
             device[1]["Os"] = item["vm_image"]

             device[1]["Network"][0]["Ip"] = item["network_interfaces"][0]["ip_address"]
             device[1]["Network"][0]["Netmask"] = item["network_interfaces"][0]["netmask"]
             device[1]["Network"][0]["Interface"] = item["network_interfaces"][0]["name_interface"]

    return MyNet

def html_to_vagrantfile(listOfDevice):
    VagrantFile = open("VagrantfileOSPF", "w")

    BeginVagrantFile(VagrantFile)
    for node in nodes:
      if node["type"] == "router":
        writeRouter(VagrantFile, node, edges)
      if node["type"] == "host":
        writeHost(VagrantFile, node, edges)        

    VagrantFile.close()

    #read the data structure from input
    #Network = G.nodes.data():
    #file = codecs.open(network_path, "r", "utf-8")
    #html = file.read()

    #if "nodes = new vis.DataSet(" in html:
      #listOfDevice = find_between(html, "nodes = new vis.DataSet(" , ")")
      #print(listOfDevice)
      #listOfDevice = yaml.load(listOfDevice) 


    #Network = remap(listOfDevice)
    #Network = listOfDevice
    #N.B per Luca, Network è già la lista dei nodi che puoi esplorare

    #first, let's write the beginnig of the VagrantFile

    #second, let's write each device with his feature
    #this topology has 3 hosts and 3 routers
    #call the respective function to "populate" the vagrant file

    #BeginVagrantFile(VagrantFile)

    #for device in Network: 
    #    typeOfDevice = device[1]["Type"]
        #print("the device is a " + typeOfDevice)

    #    if typeOfDevice is "Router":
    #        writeRouter(VagrantFile,device)


    #for device in Network:
    #    typeOfDevice = device[1]["Type"]
        #print("the device is a " + typeOfDevice)

    #    if typeOfDevice is "Host":
    #        writeHost(VagrantFile,device)



