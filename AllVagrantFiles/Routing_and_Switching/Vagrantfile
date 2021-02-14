# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box_check_update = true
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--usb", "on"]
    vb.customize ["modifyvm", :id, "--usbehci", "off"]
    vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    vb.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
    vb.customize ["modifyvm", :id, "--nicpromisc4", "allow-all"]
    vb.customize ["modifyvm", :id, "--nicpromisc5", "allow-all"]
    vb.cpus = 1
  end
  config.vm.define "router-1" do |router1|
    router1.vm.box = "bento/ubuntu-16.04"
    router1.vm.hostname = "router-1"
    router1.vm.network "private_network", ip: "172.16.3.5", netmask: "255.255.255.240", virtualbox__intnet: "broadcast_router-south-1", auto_config: true
    router1.vm.network "private_network", ip: "172.16.4.9",netmask: "255.255.255.252", virtualbox__intnet: "broadcast_router-inter", auto_config: true
    router1.vm.provision "shell", run: "always", inline: <<-SHELL
	echo "Static Routig configuration Started"
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.4.10 dev eth2
	sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.3.2 dev eth1
	sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.3.2 dev eth1
	echo "Configuration END"
	echo "Router--1 is ready to Use"	
	SHELL
    router1.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end
  config.vm.define "router-2" do |router2|
    router2.vm.box = "bento/ubuntu-16.04"
    router2.vm.hostname = "router-2"
    router2.vm.network "private_network", ip: "172.16.2.10", netmask: "255.255.255.0", virtualbox__intnet: "broadcast_router-south-2", auto_config: true
    router2.vm.network "private_network", ip: "172.16.4.10", netmask: "255.255.255.252", virtualbox__intnet: "broadcast_router-inter", auto_config: true
    router2.vm.provision "shell", run: "always", inline: <<-SHELL
	echo "Static Routig configuration Started"
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.4.9 dev eth2
    sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.4.9 dev eth2
    sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.4.9 dev eth2
	echo "Configuration END"
	echo "Router--2 is ready to Use"	
	SHELL
	router2.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end
  config.vm.define "switch" do |switch|
    switch.vm.box = "bento/ubuntu-16.04"
    switch.vm.hostname = "switch"
    switch.vm.network "private_network", virtualbox__intnet: "broadcast_router-south-1", auto_config: false
    switch.vm.network "private_network", virtualbox__intnet: "broadcast_host_a", auto_config: false
    switch.vm.network "private_network", virtualbox__intnet: "broadcast_host_b", auto_config: false
    switch.vm.provision "shell", inline: <<-SHELL
	echo "OpenVSwitch Installation is started"
	apt-get update
	apt-get install -y tcpdump
	apt-get install -y openvswitch-common openvswitch-switch apt-transport-https ca-certificates curl software-properties-common
	echo "OpenVSwitch Bridge Configuration Started"
	sudo ovs-vsctl add-br SW1
	sudo ovs-vsctl add-br HA
	sudo ovs-vsctl add-br HB
	sudo ovs-vsctl add-port SW1 eth1
	sudo ovs-vsctl add-port HA eth2
	sudo ovs-vsctl add-port HB eth3
	echo "Bridge configuration END"
	SHELL
	switch.vm.provision "shell", run: "always", inline: <<-SHELL
	echo "OpenVSwitch Ip addressing is started"
	sudo ifconfig SW1 172.16.3.2/28
	sudo ifconfig HA 172.16.8.10/22
	sudo ifconfig HB 172.16.12.10/22
	sudo ifconfig SW1 up
	sudo ifconfig HA up
	sudo ifconfig HB up
	sudo ifconfig eth1 up
	sudo ifconfig eth2 up
	sudo ifconfig eth3 up
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.3.5 dev SW1
	sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.3.5 dev SW1
	echo "Configuration END"
	echo "Switch is ready to Use"	
	SHELL
	 switch.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end
  config.vm.define "host-a" do |hosta|
    hosta.vm.box = "bento/ubuntu-16.04"
    hosta.vm.hostname = "host-a"
    hosta.vm.network "private_network", ip: "172.16.8.5", netmask: "255.255.252.0", virtualbox__intnet: "broadcast_host_a", auto_config: true
    #hosta.vm.provision "shell", inline: <<-SHELL
	#echo "Installation of Lynx Text-Based Browser to access the Web-Server via terminal on Host--A"
	#sudo apt-get update
	#sudo apt-get install -y lynx
	#echo "Lynx-Browser is installed"
	#SHELL		
	hosta.vm.provision "shell", run: "always", inline: <<-SHELL
	echo "Static Routig configuration Started for Host--A"
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.8.10 dev eth1
    sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.8.10 dev eth1
    sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.8.10 dev eth1
    sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.8.10 dev eth1
	echo "Configuration END"
	echo "Host--A is ready to Use"	
	SHELL
	hosta.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end
  config.vm.define "host-b" do |hostb|
    hostb.vm.box = "bento/ubuntu-16.04"
    hostb.vm.hostname = "host-b"
    hostb.vm.network "private_network", ip: "172.16.12.5", netmask: "255.255.252.0", virtualbox__intnet: "broadcast_host_b", auto_config: true
    #hostb.vm.provision "shell", inline: <<-SHELL
	#echo "Installation of Lynx Text-Based Browser to access the Web-Server via terminal on Host-B"
	#sudo apt-get update
	#sudo apt-get install -y lynx
	#echo "Lynx-Browser is installed"
	#SHELL	
	hostb.vm.provision "shell", run: "always", inline: <<-SHELL
	echo "Static Routig configuration Started for Host--B"
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.12.10 dev eth1
    sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.12.10 dev eth1
    sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.12.10 dev eth1
    sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.12.10 dev eth1
	echo "Configuration END"
	echo "Host--B is ready to Use"	
	SHELL
	hostb.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end
  config.vm.define "host-c" do |hostc|
    hostc.vm.box = "bento/ubuntu-16.04"
    hostc.vm.hostname = "host-c"
    hostc.vm.network "private_network", ip: "172.16.2.5", netmask: "255.255.255.0", virtualbox__intnet: "broadcast_router-south-2", auto_config: true
    hostc.vm.provision "shell", run: "always", inline: <<-SHELL
	echo "Static Routig configuration Started"
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.2.10 dev eth1
	sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.2.10 dev eth1
    sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.2.10 dev eth1
    sudo route add -net 172.16.8.0 netmask 255.255.252.0 gw 172.16.2.10 dev eth1
    sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.2.10 dev eth1
	echo "Configuration END"
	echo "Host--C is ready to Use"	
	SHELL
	hostc.vm.provision "shell", inline: <<-SHELL
	echo "Installation of Web-Server"
	sudo apt-get update
	sudo apt-get install -y apache2
	echo "Web-ServerServer is installed and Runing"
	SHELL
	 hostc.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end
end
