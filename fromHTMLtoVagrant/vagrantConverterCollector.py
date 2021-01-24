import VagrantTopologyOSPF, VagrantTopologyDocker, VagrantTopologyMySQL, VagrantTopologySwitch, VagrantTopologyWebServer
import codecs
import yaml


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def extract_nodes(network_path):
    file = codecs.open(network_path, "r", "utf-8")
    html = file.read()

    if "nodes = new vis.DataSet(" in html:
      listOfDevice = find_between(html, "nodes = new vis.DataSet(" , ")")
      print(listOfDevice)
      listOfDevice = yaml.load(listOfDevice) 

    return listOfDevice

def converter_selector(network_path, template):
    network = extract_nodes(network_path)
    if(template == "OSPF"):
        VagrantTopologyOSPF.html_to_vagrantfile(network)
    if(template == "Docker"):
        VagrantTopologyDocker.html_to_vagrantfile(network)
    if(template == "MySQL"):
        VagrantTopologyMySQL.html_to_vagrantfile(network)
    if(template == "Switch"):
        VagrantTopologySwitch.html_to_vagrantfile(network)
    if(template == "WebServer"):
        VagrantTopologyWebServer.html_to_vagrantfile(network)