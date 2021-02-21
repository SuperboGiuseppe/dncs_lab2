import ipcalc
import yaml

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f):

    f.write("##### One Host and a Mysql server with the Docker ####")

    f.write("# -*- mode: ruby -*-\n")
    f.write("# vi: set ft=ruby :\n")

    f.write("# All Vagrant configuration is done below. The \"2\" in Vagrant.configure\n")
    f.write("# configures the configuration version (we support older styles for\n")
    f.write("# backwards compatibility). Please don't change it unless you know what\n")
    f.write("# you're doing.\n")
    f.write("Vagrant.configure(\"2\") do |config|\n")
    f.write("config.vm.box_check_update = true\n")
    f.write('config.vm.provider "virtualbox" do |vb|\n')
    f.write('vb.customize ["modifyvm", :id, "--usb", "on"]\n')
    f.write('vb.customize ["modifyvm", :id, "--usbehci", "off"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc4", "allow-all"]\n')
    f.write('vb.customize ["modifyvm", :id, "--nicpromisc5", "allow-all"]\n')
    f.write('vb.cpus = 1\n')
    f.write('end\n')


#this function write in the vagrant file a new PC host
def writeHost(f, Host, edges):

  #  print("adding an host to the vagrant file")

    #extrapolate each attribute from the touples
    Id = Host["id"]
    Name = Host["label"]
    Os  = Host["vm_image"]
    Ram = Host["ram"]
    N_Cpus = Host["n_cpus"]
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

    CustumScript = Host["custom_script"]
    #there must be a more efficient way to calculate this, this one is too trivial
    for x in Network:
      Gateway = str(x)

    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \"" + Name + "\"\n")

    
    f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: true\n") 
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started for " + Name + "\"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
    f.write("sudo route add -net " + str(IpNet) + " netmask " + Netmask + " gw " + Gateway + " dev " + Interface + "\n")
    f.write('cd /home/vagrant\n')
    f.write('git clone https://github.com/magnific0/wondershaper.git\n')
    f.write('cd wondershaper\n')
    for edge in edges:
      if UplinkBandwidth > 0 or DownlinkBandwidth > 0:
        f.write('sudo ./wondershaper -a ' + Interface)
        if DownlinkBandwidth > 0:
          f.write(' -d ' + str(DownlinkBandwidth))
        if UplinkBandwidth > 0:
          f.write(' -u ' + str(UplinkBandwidth))
        f.write('\n')
    #here there is the custum script
    f.write(CustumScript + " \n")

    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")

def writeWebServer(f, Web, edges):

    Id = Web["id"]
    Name = Web["label"]
    Os  = Web["vm_image"]
    Ram = Web["ram"]
    N_Cpus = Web["n_cpus"]
    
    Ip = Web["network_interfaces"][0]["ip_address"]
    Netmask = Web["network_interfaces"][0]["netmask"]
    Interface = Web["network_interfaces"][0]["name_interface"]
    EdgeReference = Web["network_interfaces"][0]["edge"]
    UplinkBandwidth = 0
    DownlinkBandwidth = 0
    for edge in edges:
      if EdgeReference[0] == edge["from"] and EdgeReference[1] == edge["to"]:
        UplinkBandwidth = edge["bandwidth_up"]
        DownlinkBandwidth = edge["bandwidth_down"]
    CustumScript = Web["custom_script"]
    IpNoSub = Ip.split("/")[0]
    Network = ipcalc.Network(Ip)
    IpNet = Network.network()
    for x in Network:
      Gateway = str(x)

    f.write('config.vm.define \"' + Name + '\" do |' + Name + '|\n')
    f.write(Name + '.vm.box = \"' + Os + '\" \n')
    f.write(Name + '.vm.hostname = \"' + Name + '\"\n')
    f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: true\n") 
    f.write(Name + '.vm.provision "file", source: \"../Dashboard_Server/telegraf.conf\", destination: \"/tmp/telegraf.conf\"\n')
    f.write(Name + '.vm.provision "shell", run: "always", inline: <<-SHELL\n')
    f.write('echo "Static Routig configuration Started for ' + Name + '\"\n')
    f.write('sudo sysctl -w net.ipv4.ip_forward=1\n')
    f.write("sudo route add -net " + str(IpNet) + " netmask " + Netmask + " gw " + Gateway + " dev " + Interface + "\n")
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
    f.write('wget https://dl.influxdata.com/telegraf/releases/telegraf_1.17.3-1_amd64.deb\n')
    f.write('sudo dpkg -i telegraf_1.17.3-1_amd64.deb\n')
    f.write('sudo mv /tmp/telegraf.conf /etc/telegraf/telegraf.conf\n')
    f.write('sudo systemctl restart telegraf\n')
    f.write('sudo systemctl enable telegraf\n')
    #here there is the custum script
    f.write(CustumScript + " \n")

    f.write('echo "Configuration END"\n')
    f.write('#echo ' + Name + ' is ready to Use"\n')
    f.write('SHELL\n')
    f.write('web1.vm.provision "docker" do |doc|\n')
    f.write('doc.pull_images "nginx"\n')
    f.write('doc.pull_images "php"\n')
    f.write('doc.run "nginx"\n')
    f.write('doc.run "php"\n')
    f.write('end\n')
    f.write(Name + '.vm.provider "virtualbox" do |vb|\n')
    f.write("vb.memory = " + Ram + "\n")
    f.write('end\n')
    f.write('end\n')

def writeDatabase(f, Db, edges):
    # Configure database server machine
    Id = Db["id"]
    Name = Db["label"]
    Os  = Db["vm_image"]
    Ram = Db["ram"]
    N_Cpus = Db["n_cpus"]

    Ip = Db["network_interfaces"][0]["ip_address"]
    Netmask = Db["network_interfaces"][0]["netmask"]
    Interface = Db["network_interfaces"][0]["name_interface"]
    EdgeReference = Db["network_interfaces"][0]["edge"]
    UplinkBandwidth = 0
    DownlinkBandwidth = 0
    for edge in edges:
      if EdgeReference[0] == edge["from"] and EdgeReference[1] == edge["to"]:
        UplinkBandwidth = edge["bandwidth_up"]
        DownlinkBandwidth = edge["bandwidth_down"]
    CustumScript = Db["custom_script"]
    IpNoSub = Ip.split("/")[0]
    Network = ipcalc.Network(Ip)
    IpNet = Network.network()
    for x in Network:
      Gateway = str(x)

    f.write('config.vm.define \"' + Name + '\" do |' + Name + '|\n')
    f.write(Name + '.vm.box = \"' + Os + '\" \n')
    f.write(Name + '.vm.hostname = \"' + Name + '\" \n')
    f.write(Name + ".vm.network \"private_network\", ip: \"" + IpNoSub +"\", netmask: \"" + Netmask + "\", virtualbox__intnet: \"broadcast_router-south-3\", auto_config: true\n") 
    f.write(Name + '.vm.provision "file", source: \"../Dashboard_Server/telegraf.conf\", destination: \"/tmp/telegraf.conf\"\n')
    f.write(Name + '.vm.provision "shell", run: "always", inline: <<-SHELL\n')
    f.write('echo "Static Routig configuration Started for db-1"\n')
    f.write('sudo sysctl -w net.ipv4.ip_forward=1\n')
    f.write("sudo route add -net " + str(IpNet) + " netmask " + Netmask + " gw " + Gateway + " dev " + Interface + "\n")
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

    f.write('wget https://dl.influxdata.com/telegraf/releases/telegraf_1.17.3-1_amd64.deb\n')
    f.write('sudo dpkg -i telegraf_1.17.3-1_amd64.deb\n')
    f.write('sudo mv /tmp/telegraf.conf /etc/telegraf/telegraf.conf\n')
    f.write('sudo systemctl restart telegraf\n')
    f.write('sudo systemctl enable telegraf\n')
    #here there is the custum script
    f.write(CustumScript + " \n")

    f.write('echo "Configuration END"\n')
    f.write('#echo "Host--B is ready to Use"	\n')
    f.write('SHELL\n')
    f.write(Name + '.vm.provision "docker" do |doc|\n')
    f.write('doc.pull_images "mysql"\n')
    f.write('doc.run "mysql"\n')
    f.write('end\n')
    f.write(Name + '.vm.provider "virtualbox" do |vb|\n')
    f.write('vb.memory = ' + str(Ram) +'\n')
    f.write('vb.cpus = ' + str(N_Cpus) + '\n')
    f.write('end\n')
    f.write('end\n')



#this function write in the vagrant file a new Router
def writeRouter(f, Router, edges):

   # print("adding a router to the vagrant file") 

    #extrapolate each attribute from the touples
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

    Ip3 = Router["network_interfaces"][2]["ip_address"]
    Netmask3 = Router["network_interfaces"][2]["netmask"]
    Interface3 = Router["network_interfaces"][2]["name_interface"]
    EdgeReference3 = Router["network_interfaces"][2]["edge"]
    UplinkBandwidth3 = 0
    DownlinkBandwidth3 = 0
    for edge in edges:
      if EdgeReference3[0] == edge["from"] and EdgeReference3[1] == edge["to"]:
        UplinkBandwidth3 = edge["bandwidth_up"]
        DownlinkBandwidth3 = edge["bandwidth_down"]
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

    CustumScript = Router["custom_script"]


    f.write("config.vm.define \""+ Name +"\" do |" + Name + "|\n")
    f.write(Name + ".vm.box = \"" + Os + "\"\n")
    f.write(Name + ".vm.hostname = \""+ Name +"\"\n")
    f.write(Name + '.vm.network "private_network", ip: \"' + IpNoSub1 + '\", netmask: \"' + Netmask1 + '\", virtualbox__intnet: "broadcast_router-south-1", auto_config: true\n')
    f.write(Name + '.vm.network "private_network", ip: \"' + IpNoSub2 + '\", netmask: \"' + Netmask2 + '\", virtualbox__intnet: "broadcast_router-south-2", auto_config: true\n')
    f.write(Name + '.vm.network "private_network", ip: \"' + IpNoSub3 + '\", netmask: \"' + Netmask3 + '\", virtualbox__intnet: "broadcast_router-south-3", auto_config: true\n')
    f.write(Name + ".vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
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
    
    if UplinkBandwidth3 > 0 or DownlinkBandwidth3 > 0:
      f.write('sudo ./wondershaper -a ' + Interface3)
      if DownlinkBandwidth3 > 0:
        f.write(' -d ' + str(DownlinkBandwidth3))
      if UplinkBandwidth3 > 0:
        f.write(' -u ' + str(UplinkBandwidth3))
      f.write('\n')
    #here there is the custum script
    f.write(CustumScript + " \n")

    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + str(Ram) + "\n")
    f.write('vb.cpus =' + str(N_Cpus) + "\n")
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
    "Ip": "192.168.10.10/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  }]
})

rout1 = (2,{
  "Id" : 2,
  "Name":"router1",
  "Type": "Router",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.10.2/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  },{
    "Ip": "192.168.10.3/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth2"
  },{
    "Ip": "192.168.10.4/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth3"
  }]
})

web1 = (3,{
  "Id" : 3,
  "Name":"web1",
  "Type": "Web",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.10.11/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  }]
})

db1 = (4,{
  "Id" : 4,
  "Name":"db1",
  "Type": "Db",
  "Ram": "1024",
  "Os": "bento/ubuntu-16.04",
  "custom_script":"echo 'THIS IS CUSTUM SCRIPT'",
  "Network" : [{
    "Ip": "192.168.10.12/24",
    "Netmask": "255.255.255.0",
    "Interface" : "eth1"
  }]
})

MyNet = [host1,rout1,web1,db1]

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

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
"""

def html_to_vagrantfile(nodes, edges):
    VagrantFile = open("Vagrantfile", "w")

    #read the data structure from input
    #Network = G.nodes.data():
    #file = codecs.open("NetworkGraphs/Template/OSPF_Routing_Template.html", "r", "utf-8")
    #html = file.read()

    #if "nodes = new vis.DataSet(" in html:
    #  listOfDevice = find_between(html, "nodes = new vis.DataSet(" , ")")
    #  print(listOfDevice)
    #  listOfDevice = yaml.load(listOfDevice) 

    #newNet = remap(listOfDevice)
    #N.B per Luca, Network è già la lista dei nodi che puoi esplorare
    #Network = MyNet #DA SOSTITUIRE CON "NEW NET" ALLA FINE

    BeginVagrantFile(VagrantFile)

    for node in nodes: 
      if node["type"] == "router":
        writeRouter(VagrantFile, node, edges)
      if node["type"] == "host":
        writeHost(VagrantFile, node, edges)
      if node["type"] == "Web":
        writeWebServer(VagrantFile, node, edges)
      if node["type"] == "Db":
        writeDatabase(VagrantFile, node, edges)
    VagrantFile.write("end\n")
    VagrantFile.close()
