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
- Web server and database setup with Vagrant multi-machine using Docker
-	Traditional web server and database setup
-	web server (nginx and PHP) on one machine and our database server (MySQL) on another
-	Our Vagrant file only step up the environment. The other configuration user can make according to their desire of the user.


# Modification By Giuseppe
- Files related to the UI ("gui.py" ) has been added.
- Files related to the network entity (A graph in this case) is managed by network_core.py which is under development.
- Documentation of the previously introduced scripts.
N.B. The GUI retrieves data from the HTML file, so it is really crucial to interface the vagrant file generator script with the html file syntax.

# Modification By Luca
- I created two files "VagrantTopologyOSPF.py" and "VagrantTopologySwitch.py" to generate vagrant files of two default networks
- Using the comand "vagrant up" with the files generated, i will build the network with the parameters that are parametrized
- updated both scripts
