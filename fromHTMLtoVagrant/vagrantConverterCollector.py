import VagrantTopologyOSPF, VagrantTopologyDocker, VagrantTopologyMySQL, VagrantTopologySwitch, VagrantTopologyWebServer, VagrantTopology3S2H
import codecs
import yaml


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def extract_network(network_path):
    file = codecs.open(network_path, "r", "utf-8")
    html = file.read()

    if "nodes = new vis.DataSet(" in html:
        nodes = yaml.safe_load(find_between(html, "nodes = new vis.DataSet(" , ")"))
        print(nodes)


    if "edges = new vis.DataSet(" in html:
        edges = yaml.safe_load(find_between(html, "edges = new vis.DataSet(", ")"))
        print(edges)

    return nodes, edges



def converter_selector(network_path, template):
    nodes, edges = extract_network(network_path)
    if(template == "OSPF"):
        VagrantTopologyOSPF.html_to_vagrantfile(nodes, edges)
    if(template == "Docker"):
        VagrantTopologyDocker.html_to_vagrantfile(nodes, edges)
    if(template == "MySQL"):
        VagrantTopologyMySQL.html_to_vagrantfile(nodes, edges)
    if(template == "Switch"):
        VagrantTopologySwitch.html_to_vagrantfile(nodes, edges)
    if(template == "WebServer"):
        VagrantTopologyWebServer.html_to_vagrantfile(nodes, edges)
    if(template == "3S2H"):
        VagrantTopology3S2H.html_to_vagrantfile(nodes, edges)    
