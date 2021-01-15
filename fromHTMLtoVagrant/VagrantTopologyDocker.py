import ipcalc 
import codecs
import yaml

#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f,Docker):

    Name = Docker[1]["Name"]
    Os  = Docker[1]["Os"]

    f.write('## to access webserver try this in your webbrowser : (http://localhost:8081/) you will see the webpage.\n')
    f.write('# -*- mode: ruby -*-\n')
    f.write('# vi: set ft=ruby :\n')
 
    f.write('Vagrant.configure("2") do |config|\n')
    f.write('config.vm.box = \"' + Os + '\"\n')
    f.write('config.vm.network "forwarded_port", guest: 80, host: 8081\n')
    f.write('config.vm.provision "docker" do |doc|\n')
    f.write('doc.pull_images "nginx"\n')
    f.write('doc.pull_images "mysql"\n')
    f.write('doc.run "mysql"\n')
    f.write('doc.run "nginx", args: "-p 80:80"\n')
    f.write('end\n')
    f.write('end\n')

docker1 = (1,{
  "Id" : 1,
  "Name":"docker1",
  "Os": "ubuntu/xenial64"
})

MyNet = [docker1]

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

def html_to_vagrantfile(Network):
    VagrantFile = open("VagrantfileDOCKER", "w")

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
    #Network = MyNet #RICAMBIALA CON NEWNET

    BeginVagrantFile(VagrantFile,docker1)

    VagrantFile.close()


main()
