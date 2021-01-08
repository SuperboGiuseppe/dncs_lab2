import ipcalc 
import codecs
import yaml

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f):
    f.write('# webserver and a host you can access the webserver from your browser with ip address 10.0.0.50 or from the host \n')
    f.write('# -*- mode: ruby -*-\n')
    f.write('# vi: set ft=ruby :\n')

    f.write('Vagrant.configure("2") do |config|\n')
    f.write('# Configure web server machine\n')


def writeWebServer(f,Web):

    Id = Web[1]["Id"]
    Name = Web[1]["Name"]
    Os  = Web[1]["Os"]
    Ip = Web[1]["Ip"]

    f.write('config.vm.define \"' + Name + '\" do |' + Name + '|\n')
    f.write(Name + '.vm.box = "\"' + Os + '\"\n')
    f.write(Name + '.vm.hostname = \"' + Name + '\"\n')
    f.write(Name + '.vm.network "private_network", ip: \"' + Ip + '\" \n')
    f.write(Name + '.vm.provision "shell", inline: <<-SHELL \n')       
    f.write('echo "Starting Provision: web server"\n')
    f.write('sudo apt-get update\n')
    f.write('sudo apt-get install -y nginx\n')
    f.write('touch /var/www/html/index.php\n')
    f.write('sudo apt-get install -y php-fpm php-mysql\n')
    f.write('echo "Provision web server complete"\n')
    f.write('SHELL\n')
    f.write('end\n')



def writeDatabase(f,Db):

    Id = Db[1]["Id"]
    Name = Db[1]["Name"]
    Os  = Db[1]["Os"]
    Ip = Db[1]["Ip"]

    f.write('# Configure database server machine\n')
    f.write('config.vm.define \"' + Name + '\" do |' + Name + '|\n')
    f.write(Name + '.vm.box = \"' + Os + '\"\n')
    f.write(Name + '.vm.hostname = "' + Name + '"\n')
    f.write(Name + '.vm.network "private_network", ip: \"' + Ip + '\" \n')
    f.write('end\n')
    f.write('end\n')


web1 = (1,{
  "Id" : 1,
  "Name":"web1",
  "Os": "ubuntu/xenial64",
  "Ip": "10.0.0.50"
})

db1 = (2,{
  "Id" : 2,
  "Name":"db1",
  "Os": "ubuntu/xenial64",
  "Ip": "10.0.0.51"
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

def main():
    VagrantFile = open("VagrantfileWEBSERVER", "w")

    #read the data structure from input
    #Network = G.nodes.data():
    #file = codecs.open("NetworkGraphs/Template/OSPF_Routing_Template.html", "r", "utf-8")
    #html = file.read()

    #if "nodes = new vis.DataSet(" in html:
    #  listOfDevice = find_between(html, "nodes = new vis.DataSet(" , ")")
    #  print(listOfDevice)
    #  listOfDevice = yaml.load(listOfDevice) 

    #newNet = remap(listOfDevice)

    Network = MyNet #RICAMBIALA CON NEWNET

    BeginVagrantFile(VagrantFile)
    writeWebServer(VagrantFile,web1)
    writeDatabase(VagrantFile,db1)

    VagrantFile.close()


main()
