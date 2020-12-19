from pyvis.network import Network
import json
import os

def create_network(network_name):
    G = Network()
    return G

def open_network(network_path):
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

    return G
    
def dictionary_to_nodes(dictionary, network):
    for node in dictionary:
        network.add_node(node["id"], image=node["image"], label=node["label"], shape=node["shape"], type=node["type"], network_interfaces=node["network_interfaces"], vm_image=node["vm_image"], ram=node["ram"], n_cpus=node["n_cpus"])

def dictionary_to_edges(dictionary, network):
    for edge in dictionary:
        network.add_edge(edge["from"],edge["to"])

def nodes_search_type(network, search_type):
    nodes = network.nodes
    result = []
    for node in nodes:
        if node["type"] == search_type:
            result.append(node)
    return result
    
    
