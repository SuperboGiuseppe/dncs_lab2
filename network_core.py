""" _____________________________________________________________

    Description: Network entity manager code
    Author: Giuseppe Superbo (giuseppe.superbo@studenti.unitn.it)
    Date: Winter 2020-2021
    Course: Design of Networks and Communication Systems
    _____________________________________________________________
"""

from pyvis.network import Network
import json
import os


def create_network():
    """Function that creates an empty network.

        Parameters:
            - network_name: name of the network
        
        Returns:
            - G: network object

    """
    G = Network()
    return G

def open_network(network_path):
    """Function that imports a network from an html file.

        Parameters:
            - network_path: path of the network to be imported
        
        Returns:
            - G: network object

    """
    G = Network()
    html = open(network_path, "r")
    lines_html = html.readlines()
    nodes = ""
    edges = ""

    for line in lines_html:
        if "nodes = new" in line:
            nodes = json.loads(line.split('(')[1].split(')')[0])
        if "edges = new" in line:
            edges = json.loads(line.split('(')[1].split(')')[0])
    
    dictionary_to_nodes(nodes, G)
    dictionary_to_edges(edges, G)

    G.save_graph("./NetworkGraphs/Temp_Network/temp_network.html")

    html_fix(os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html"))

    return G
    

def dictionary_to_nodes(dictionary, network):
    """Procedure that adds new nodes to a network by parsing a dictionary

        Parameters:
            - dictionary: dictionary that contains the new nodes;
            - network: network to be updated.

    """
    for node in dictionary:
        network.add_node(node["id"], image=node["image"], label=node["label"], shape=node["shape"], type=node["type"], network_interfaces=node["network_interfaces"], vm_image=node["vm_image"], ram=node["ram"], n_cpus=node["n_cpus"], custom_script=node["custom_script"])


def dictionary_to_edges(dictionary, network):
    """Procedure that adds new edges to a network by parsing a dictionary

        Parameters:
            - dictionary: dictionary that contains the new edges;
            - network: network to be updated.

    """
    for edge in dictionary:
        network.add_edge(edge["from"],edge["to"], bandwidth_up=edge["bandwidth_up"], bandwidth_down=edge["bandwidth_down"])

def nodes_search_type(network, search_type):
    """Function that returns only a specific type of nodes of a network

        Parameters:
            - search_type: type of nodes that should be returned;
            - network: network as source.

        Returns:
            - result: dictionary that contains the result of the search.
    """
    nodes = network.nodes
    result = []
    for node in nodes:
        if search_type == "others":
            if node["type"] not in ["router", "host", "switch"]:
                result.append(node)
        elif node["type"] == search_type:
            result.append(node)
    return result
    

def html_fix(html_path):
    """Procedure that fixes the css style of the network graph visualization

        Parameters:
            - html_path: absolute path of the html to be fixed
    """
    old_html = open(os.path.abspath(html_path), "r")
    lines = old_html.readlines()
    old_html_data = old_html.read()
    old_html.close()
    new_html = open(os.path.abspath(html_path), "w")
    for line in lines:
        if line.strip("\n") != "<center>" and line.strip("\n") != "<h1>None</h1>" and line.strip("\n") != "</center>":
            if line.strip("\n") == "            width: 500px;":
                new_html.write('            width: 990px;\n')
                continue
            if line.strip("\n") == "            height: 500px;":
                new_html.write('            height: 600px;\n')
                continue
            if line.strip("\n") == "            position: relative;":
                new_html.write('            position: center;\n')
                continue
            if line.strip("\n") == "            border: 1px solid lightgray;":
                new_html.write("            border: 0px solid lightgray;\n")
                continue
            new_html.write(line)
    new_html.close()
