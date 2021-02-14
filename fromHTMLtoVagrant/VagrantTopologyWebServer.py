import ipcalc 
import yaml

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f):
    f.write('# webserver and a host you can access the webserver from your browser with ip address 10.0.0.50 or from the host \n')
    f.write('# -*- mode: ruby -*-\n')
    f.write('# vi: set ft=ruby :\n')

    f.write('Vagrant.configure("2") do |config|\n')
    f.write('# Configure web server machine\n')


def writeWebServer(f, Web, edges):

    Id = Web["id"]
    Name = Web["label"]
    Os  = Web["vm_image"]
    Ip = Web["network_interfaces"][0]["ip_address"]
    Ram = Web["ram"]
    N_Cpus = Web["n_cpus"]
    InterfaceName = Web["network_interfaces"][0]["name_interface"]
    EdgeReference = Web["network_interfaces"][0]["edge"]
    UplinkBandwidth = 0
    DownlinkBandwidth = 0
    for edge in edges:
      if EdgeReference[0] == edge["from"] and EdgeReference[1] == edge["to"]:
        UplinkBandwidth = edge["bandwidth_up"]
        DownlinkBandwidth = edge["bandwidth_down"]
    CustumScript = Web["custom_script"]
    

    f.write('config.vm.define \"' + Name + '\" do |' + Name + '|\n')
    f.write(Name + '.vm.box = \"' + Os + '\"\n')
    f.write(Name + '.vm.hostname = \"' + Name + '\"\n')
    f.write(Name + '.vm.network "private_network", ip: \"' + Ip + '\" \n')
    f.write(Name + '.vm.provision "shell", inline: <<-SHELL \n')       
    f.write('echo "Starting Provision: web server"\n')
    f.write('sudo apt-get update\n')
    f.write('sudo apt-get install -y nginx\n')
    f.write('touch /var/www/html/index.php\n')
    f.write('sudo apt-get install -y php-fpm php-mysql\n')
    f.write('cd /home/vagrant\n')
    f.write('git clone https://github.com/magnific0/wondershaper.git\n')
    f.write('cd wondershaper\n')
    for edge in edges:
      if UplinkBandwidth > 0 or DownlinkBandwidth > 0:
        f.write('sudo ./wondershaper -a ' + InterfaceName)
        if DownlinkBandwidth > 0:
          f.write(' -d ' + str(DownlinkBandwidth))
        if UplinkBandwidth > 0:
          f.write(' -u ' + str(UplinkBandwidth))
        f.write('\n')
    #here there is the custum script
    f.write(CustumScript + " \n")

    f.write('echo "Provision web server complete"\n')
    f.write('SHELL\n')
    f.write(Name + '.vm.provider "virtualbox" do |vb|\n')
    f.write('vb.memory = ' + str(Ram) + '\n')
    f.write('vb.cpus = ' + str(N_Cpus) + '\n')
    f.write('end\n')
    f.write('end\n')


def writeDatabase(f, Db, edges):

    Id = Db["id"]
    Name = Db["label"]
    Os  = Db["vm_image"]
    Ip = Db["network_interfaces"][0]["ip_address"]
    Ram = Db["ram"]
    N_Cpus = Db["n_cpus"]
    InterfaceName = Db["network_interfaces"][0]["name_interface"]
    EdgeReference = Db["network_interfaces"][0]["edge"]
    UplinkBandwidth = 0
    DownlinkBandwidth = 0
    for edge in edges:
      if EdgeReference[0] == edge["from"] and EdgeReference[1] == edge["to"]:
        UplinkBandwidth = edge["bandwidth_up"]
        DownlinkBandwidth = edge["bandwidth_down"]
    CustumScript = Db["custom_script"]

    f.write('# Configure database server machine\n')
    f.write('config.vm.define \"' + Name + '\" do |' + Name + '|\n')
    f.write(Name + '.vm.box = \"' + Os + '\"\n')
    f.write(Name + '.vm.hostname = \"' + Name + '\"\n')
    f.write(Name + '.vm.network "private_network", ip: \"' + Ip + '\" \n')

    f.write(Name + '.vm.provision "shell", run: "always", inline: <<-SHELL\n')
    f.write('sudo apt update\n')
    f.write('sudo DEBIAN_FRONTEND=noninteractive apt-get -q -y install mysql-server\n')
    f.write('echo \"WARNING: It is necessary to set the root password of mysql-server before using it!!!\"\n')
    f.write('echo \"Example password configuration: mysqladmin -u root password mysecretpasswordgoeshere\"\n')
    f.write('sleep 10\n')
    f.write('cd /home/vagrant\n')
    f.write('git clone https://github.com/magnific0/wondershaper.git\n')
    f.write('cd wondershaper\n')
    for edge in edges:
      if UplinkBandwidth > 0 or DownlinkBandwidth > 0:
        f.write('sudo ./wondershaper -a ' + InterfaceName)
        if DownlinkBandwidth > 0:
          f.write(' -d ' + str(DownlinkBandwidth))
        if UplinkBandwidth > 0:
          f.write(' -u ' + str(UplinkBandwidth))
        f.write('\n')

    #here there is the custum script
    f.write(CustumScript + " \n")
    f.write('echo "Provision database server complete"\n')
    f.write('SHELL\n')
    f.write(Name + '.vm.provider "virtualbox" do |vb|\n')
    f.write('vb.memory = ' + str(Ram) + '\n')
    f.write('vb.cpus = ' + str(N_Cpus) + '\n')
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

      print("remap of device " + str(device[1]["Id"] + " to device " + str(item["id"])))
      device[1]["Name"] = item["label"]
      device[1]["Ram"] = item["ram"]
      device[1]["Os"] = item["vm_image"]
      device[1]["N_Cpus"] = item["n_cpus"]

      device[1]["Network"][0]["Ip"] = item["network_interfaces"][0]["ip_address"]
      device[1]["Network"][0]["Netmask"] = item["network_interfaces"][0]["netmask"]
      device[1]["Network"][0]["Interface"] = item["network_interfaces"][0]["name_interface"]
      #device[1]["Network"][0]["Uplink_bandwidth"] = 


      if item["type"] == "web" : 

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
      if item["type"] == "db" : 

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

    #Network = MyNet #RICAMBIALA CON NEWNET
    #N.B per Luca, Network è già la lista dei nodi che puoi esplorare

    BeginVagrantFile(VagrantFile)
    for node in nodes:
      if node["type"] == "web":
        writeWebServer(VagrantFile, node, edges)
      if node["type"] == "db":
        writeDatabase(VagrantFile, node, edges)
    VagrantFile.write('end\n')
    VagrantFile.close()

