#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[24]:


## Our motive is to generate only one single vagrant file.##
## we will try to make a generic file as much as possible. since it's a test-based project/not a production based##
## we will allow our user's limited choices to selects the combinations. So, things will not get complicated either for the user either for us.##
## for example we only allow users to give the IP addresses.##
## VM topologies will already be defined and created you can see the given topology below.

f = open("vagrant.txt", "w")
f.write("# -*- mode: ruby -*- \n# vi: set ft=ruby :\n\n")
f.write("#All Vagrant configuration is done below. The 2 in Vagrant.configure\n#configures the configuration version we support older styles for\n#backwards compatibility. Please don't change it unless you know what\n#you're doing.\n")
f.write("Vagrant.configure(\"2\") do |config|\n")
f.write("config.vm.box_check_update = true\n")
f.write("config.vm.provider \"virtualbox\" do |vb|\n")
f.write("vb.customize [\"modifyvm\", :id, \"--usb\", \"on\"]\n")
f.write("vb.customize [\"modifyvm\", :id, \"--usbehci\", \"off\"]\n")
f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc2\", \"allow-all\"]\n")
f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc3\", \"allow-all\"]\n")
f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc4\", \"allow-all\"]\n")
f.write("vb.customize [\"modifyvm\", :id, \"--nicpromisc5\", \"allow-all\"]\n")
f.write("vb.cpus = 1\n")
f.write("end\n")
#######################################################################################

## we can give the user right to change the Virtual machine name as they wanted. But it's optional, not mandatory.

#vm = input("Enter your VM name:")
#f.write("config.vm.define" " " + vm)
f.write("config.vm.define \"router-1\" do |router1|\n")
f.write("router1.vm.box = \"bento/ubuntu-16.04\"\n")
f.write("router1.vm.hostname = \"router-1\"\n")
# User can selecte the desire IP addresses according to the requirements.
f.write("router1.vm.network \"private_network\", ip: \"172.16.3.5\", netmask: \"255.255.255.240\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: true\n")
f.write("router1.vm.network \"private_network\", ip: \"172.16.4.9\",netmask: \"255.255.255.252\", virtualbox__intnet: \"broadcast_router-inter\", auto_config: true\n")
f.write("router1.vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
f.write("echo \"Static Routig configuration Started\"\n")
f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
# we need to automate IP addressing according to the network/IP selection
f.write("sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.4.10 dev eth2\n")
f.write("sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.3.2 dev eth1\n")
f.write("sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.3.2 dev eth1\n")
f.write("echo \"Configuration END\"\n")
f.write("echo \"Router--1 is ready to Use\"\n")
f.write("SHELL\n")
f.write("router1.vm.provider \"virtualbox\" do |vb|\n")
# User can select the desired menmory for the machine. based on the application usage.
f.write("vb.memory = 1024\n")
f.write("end\n")
f.write("end\n")
f.write("config.vm.define \"router-2\" do |router2|\n")
f.write("router2.vm.box = \"bento/ubuntu-16.04\"\n")
f.write("router2.vm.hostname = \"router-2\"\n")
f.write("router2.vm.network \"private_network\", ip: \"172.16.2.10\", netmask: \"255.255.255.0\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: true\n")
f.write("router2.vm.network \"private_network\", ip: \"172.16.4.10\", netmask: \"255.255.255.252\", virtualbox__intnet: \"broadcast_router-inter\", auto_config: true\n")
f.write("router2.vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
f.write("echo \"Static Routig configuration Started\"\n")
f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
f.write("sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.4.9 dev eth2\n")
f.write("sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.4.9 dev eth2\n")
f.write("sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.4.9 dev eth2\n")
f.write("echo \"Configuration END\"\n")
f.write("echo \"Router--2 is ready to Use\"\n")
f.write("SHELL\n")
f.write("router2.vm.provider \"virtualbox\" do |vb|\n")
# User can select the desired menmory for the machine. we must allow them
f.write("vb.memory = 1024\n")
f.write("end\n")
f.write("end\n")
f.write("config.vm.define \"switch\" do |switch|\n")
f.write("switch.vm.box = \"bento/ubuntu-16.04\"\n")
f.write("switch.vm.hostname = \"switch\"\n")
f.write("switch.vm.network \"private_network\", virtualbox__intnet: \"broadcast_router-south-1\", auto_config: false\n")
f.write("switch.vm.network \"private_network\", virtualbox__intnet: \"broadcast_host_a\", auto_config: false\n")
f.write("switch.vm.network \"private_network\", virtualbox__intnet: \"broadcast_host_b\", auto_config: false\n")
f.write("switch.vm.provision \"shell\", inline: <<-SHELL\n")
f.write("echo \"OpenVSwitch Installation is started\"\n")
f.write("apt-get update\n")
f.write("apt-get install -y tcpdump\n")
f.write("apt-get install -y openvswitch-common openvswitch-switch apt-transport-https ca-certificates curl software-properties-common\n")
f.write("echo \"OpenVSwitch Bridge Configuration Started\"\n")
f.write("sudo ovs-vsctl add-br SW1\n")
f.write("sudo ovs-vsctl add-br HA\n")
f.write("sudo ovs-vsctl add-br HB\n")
f.write("sudo ovs-vsctl add-port SW1 eth1\n")
f.write("sudo ovs-vsctl add-port HA eth2\n")
f.write("sudo ovs-vsctl add-port HB eth3\n")
f.write("echo \"Bridge configuration END\"\n")
f.write("SHELL\n")
f.write("switch.vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
f.write("echo \"OpenVSwitch Ip addressing is started\"\n")
f.write("sudo ifconfig SW1 172.16.3.2/28\n")
f.write("sudo ifconfig HA 172.16.8.10/22\n")
f.write("sudo ifconfig HB 172.16.12.10/22\n")
f.write("sudo ifconfig SW1 up\n")
f.write("sudo ifconfig HA up\n")
f.write("sudo ifconfig HB up\n")
f.write("sudo ifconfig eth1 up\n")
f.write("sudo ifconfig eth2 up\n")
f.write("sudo ifconfig eth3 up\n")
f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
f.write("sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.3.5 dev SW1\n")
f.write("sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.3.5 dev SW1\n")
f.write("echo \"Configuration END\"\n")
f.write("echo \"Switch is ready to Use\"\n")
f.write("SHELL\n")
f.write("switch.vm.provider \"virtualbox\" do |vb|\n")
# User can select the desired menmory for the machine. we must allow them
f.write("vb.memory = 1024\n")
f.write("end\n")
f.write("end\n")

f.write("config.vm.define \"host-a\" do |hosta|\n")
f.write("hosta.vm.box = \"bento/ubuntu-16.04\"\n")
f.write("hosta.vm.hostname = \"host-a\"\n")
f.write("hosta.vm.network \"private_network\", ip: \"172.16.8.5\", netmask: \"255.255.252.0\", virtualbox__intnet: \"broadcast_host_a\", auto_config: true\n")
f.write("#hosta.vm.provision \"shell\", inline: <<-SHELL\n")
f.write("#echo \"Installation of Lynx Text-Based Browser to access the Web-Server via terminal on Host--A\"\n")
f.write("#sudo apt-get update\n")
f.write("#sudo apt-get install -y lynx\n")
f.write("#echo \"Lynx-Browser is installed\"\n")
f.write("#SHELL\n")
f.write("hosta.vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
f.write("echo \"Static Routig configuration Started for Host--A\"\n")
f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
f.write("sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.8.10 dev eth1\n")
f.write("sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.8.10 dev eth1\n")
f.write("sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.8.10 dev eth1\n")
f.write("sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.8.10 dev eth1\n")
f.write("echo \"Configuration END\"\n")
f.write("echo \"Host--A is ready to Use\"\n")
f.write("SHELL\n")
f.write("hosta.vm.provider \"virtualbox\" do |vb|\n")
f.write("vb.memory = 1024\n")
f.write("end\n")
f.write("end\n")
f.write("config.vm.define \"host-b\" do |hostb|\n")
f.write("hostb.vm.box = \"bento/ubuntu-16.04\"\n")
f.write("hostb.vm.hostname = \"host-b\"\n")
f.write("hostb.vm.network \"private_network\", ip: \"172.16.12.5\", netmask: \"255.255.252.0\", virtualbox__intnet: \"broadcast_host_b\", auto_config: true\n")
f.write("#hostb.vm.provision \"shell\", inline: <<-SHELL\n")
f.write("#echo \"Installation of Lynx Text-Based Browser to access the Web-Server via terminal on Host-B\"\n")
f.write("#sudo apt-get update\n")
f.write("#sudo apt-get install -y lynx\n")
f.write("#echo \"Lynx-Browser is installed\"\n")
f.write("#SHELL\n")
f.write("hostb.vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
f.write("echo \"Static Routig configuration Started for Host--B\"\n")
f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
f.write("sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.12.10 dev eth1\n")
f.write("sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.12.10 dev eth1\n")
f.write("sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.12.10 dev eth1\n")
f.write("sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.12.10 dev eth1\n")
f.write("echo \"Configuration END\"\n")
f.write("echo \"Host--B is ready to Use\"\n")
f.write("SHELL\n")
f.write("hostb.vm.provider \"virtualbox\" do |vb|\n")
f.write("vb.memory = 1024\n")
f.write("end\n")
f.write("end\n")
f.write("config.vm.define \"host-c\" do |hostc|\n")
f.write("hostc.vm.box = \"bento/ubuntu-16.04\"\n")
f.write("hostc.vm.hostname = \"host-c\"\n")
f.write("hostc.vm.network \"private_network\", ip: \"172.16.2.5\", netmask: \"255.255.255.0\", virtualbox__intnet: \"broadcast_router-south-2\", auto_config: true\n")
f.write("hostc.vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
f.write("echo \"Static Routig configuration Started\"\n")
f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
f.write("sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.2.10 dev eth1\n")
f.write("sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.2.10 dev eth1\n")
f.write("sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.2.10 dev eth1\n")
f.write("sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.2.10 dev eth1\n")
f.write("sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.2.10 dev eth1\n")
f.write("echo \"Configuration END\"\n")
f.write("echo \"Host--C is ready to Use\"\n")
f.write("SHELL\n")
f.write("hostc.vm.provision \"shell\", inline: <<-SHELL\n")
f.write("echo \"Installation of Web-Server\"\n")
f.write("sudo apt-get update\n")
f.write("sudo apt-get install -y apache2\n")
f.write("echo \"Web-ServerServer is installed and Runing\"\n")
f.write("SHELL\n")
f.write("hostc.vm.provider \"virtualbox\" do |vb|\n")
f.write("vb.memory = 1024\n")
f.write("end\n")
f.write("end\n")
f.write("end\n")
f.close()
#open and read the file after the appending:
f = open("vagrant.txt", "r")
print(f.read())


# In[ ]:





# In[ ]:




