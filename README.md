# dncs_lab2
Design of Networks and Communication Systems Project A.Y. 2020-21 - University of Trento

Automating the deployment of network setups using vagrant

- To build a scripting/visual interface to pre-configure and run a network of VMs/containers and OpenVSwitches
- User interface could be a script that it converted in a Vagrantfile for running the network, or an HTTP interface
- Suggested software: Vagrant, OpenVSwitch, docker
- Proposer: Fabrizio Granelli (fabrizio.granelli@unitn.it)

# Modification By Uzair
- Two files are added namely "Vagrant" and "VagrantScriptCreatorInTextFormat".
- Two more files added namely "OSPFRoutingVag" and "OSPF Routing". One file contains a Python script to create the Vagrant file, the other file is just a JPG topology of the network.

# Modification By Giuseppe
- Files related to the UI ("gui.py", "html_fix.py") have been added. The first one contains the GUI definition, meanwhile "html_fix.py" fixes the network output of pyvis module.
- Files related to the network entity (A graph in this case) is managed by network_core.py which is under development.
- "Templates.py" contains an example on how the network is defined by the interface. This network is then converted in
an html file (The same example can be found "OSPF_Routing_Template.html" in the directory NetworkGraphs/Template)
N.B. The GUI retrieves data from the HTML file, so it is really crucial to interface the vagrant file generator script with the html file syntax.

# Modification By Luca
- I created two files "VagrantTopologyOSPF.py" and "VagrantTopologySwitch.py" to generate vagrant files of two default networks
- Using the comand "vagrant up" with the files generated, i will build the network with the parameters that are parametrized
