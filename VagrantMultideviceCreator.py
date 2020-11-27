
#this function writes the beginning of the VagrantFile
def BeginVagrantFile(f,Network):
    print("writing the beginning of the VagrantFile")
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


#this function write in the vagrant file a new PC host
def writeHost(f,Host):

    #extrapolate each attribute from the touples
    Name = Host[1]["Name"]
    CPU = Host[1]["Cpu"]
    Ram = Host[1]["Ram"]
    Os  = Host[1]["Os"]
    Ip  = Host[1]["Ip"]

    print("the Name is " + Name)
    print("the CPU is " + CPU)
    print("the Ram is " + Ram)
    print("the Os is " + Os)
    print("the Ip is " + Ip)
    print("adding an host to the vagrant file")

    f.write("config.vm.define \" " + Name + "\" do |" + Name + "|\n")
    f.write("hosta.vm.box = \" " + Os + " \"\n")
    f.write("hosta.vm.hostname = \" " + Name + " \"\n")
    f.write("hosta.vm.network \"private_network\", ip: \" " + Ip +" \", netmask: \"255.255.252.0\", virtualbox__intnet: \"broadcast_host_a\", auto_config: true\n")
    f.write("hosta.vm.provision \"shell\", run: \"always\", inline: <<-SHELL\n")
    f.write("echo \"Static Routig configuration Started for " + Name + " \"\n")
    f.write("sudo sysctl -w net.ipv4.ip_forward=1\n")
    f.write("sudo route add -net 172.16.3.0 netmask 255.255.255.240 gw 172.16.8.10 dev eth1\n")
    f.write("sudo route add -net 172.16.12.0 netmask 255.255.252.0 gw 172.16.8.10 dev eth1\n")
    f.write("sudo route add -net 172.16.4.8 netmask 255.255.255.252 gw 172.16.8.10 dev eth1\n")
    f.write("sudo route add -net 172.16.2.0 netmask 255.255.255.0 gw 172.16.8.10 dev eth1\n")
    f.write("echo \"Configuration END\"\n")
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    f.write("vb.memory = " + Ram + " \n")
    f.write("end\n")
    f.write("end\n")



#this function write in the vagrant file a new switch
def writeSwitch(f,Switch):

    #extrapolate each attribute from the touples
    Name = Switch[1]["Name"]
    CPU = Switch[1]["Cpu"]
    Ram = Switch[1]["Ram"]
    Os  = Switch[1]["Os"]

    print("the Switch is " + CPU)
    print("the CPU is " + CPU)
    print("the Ram is " + Ram)
    print("the Os is " + Os)
    print("adding a switch to the vagrant file")

    f.write("config.vm.define \"" + Name + "\" do |" + Name +"|\n")
    f.write("switch.vm.box = \"" + Os + "\"\n")
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
    f.write("echo \"" + Name + " is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    # User can select the desired menmory for the machine. we must allow them
    f.write("vb.memory = " + Ram +"\n")
    f.write("end\n")
    f.write("end\n")



#this function write in the vagrant file a new Router
def writeRouter(f,Router):

    #extrapolate each attribute from the touples
    Name = Router[1]["Name"]
    CPU = Router[1]["Cpu"]
    Ram = Router[1]["Ram"]
    Os  = Router[1]["Os"]
    Ip  = Router[1]["Ip"]

    print("the CPU is " + CPU)
    print("the Ram is " + Ram)
    print("the Os is " + Os)
    print("the Ip is " + Ip)
    print("adding a router to the vagrant file")

    #vm = input("Enter your VM name:")
    #f.write("config.vm.define" " " + vm)
    f.write("config.vm.define \"" + Name + "\" do |" + Name + "|\n")
    f.write("router1.vm.box = \" " + Os + " \"\n")
    f.write("router1.vm.hostname = \"" + Name + "\"\n")
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
    f.write("echo \""+ Name +" is ready to Use\"\n")
    f.write("SHELL\n")
    f.write(Name + ".vm.provider \"virtualbox\" do |vb|\n")
    # User can select the desired menmory for the machine. based on the application usage.
    f.write("vb.memory = " + Ram + "\n")
    f.write("end\n")
    f.write("end\n")


#ATTRIBUTE FOR EACH DEVICE !!!
#FOR THE HOST   :CPU/RAM/OS/IP ADDRESS/NAME
#FOR THE SWITCH :
#FOR THE ROUTER :

#the following is a fake graph that i used for testing
dev1 = (1,{
  "Name":"host_a",
  "Type": "Host",
  "Cpu": "gamingCPU",
  "Ram": "512MB",
  "Os": "linux64",
  "Ip": "10.0.20.13"
})
dev2 = (2,{
  "Name":"aaaaaaa",
  "Type": "Switch",
  "Cpu": "aaaaaa",
  "Ram": "bbbbb",
  "Os": "ccccccc",
  "Ip": "ddddddd"
})
dev3 = (3,{
  "Name":"mozzarella",
  "Type": "Router",
  "Cpu": "pizza",
  "Ram": "pasta",
  "Os": "mandolino",
  "Ip": "berlusconi"
})
fakeNet = [dev1,dev2,dev3]

def main():
    VagrantFile = open("VagrantFromScript.txt", "w")

    #read the data structure from input
    #Network = G.nodes.data():
    Network = fakeNet

    #first, let's write the beginnig of the VagrantFile
    BeginVagrantFile(VagrantFile,Network)


    #second, let's write each device with his feature
    for device in Network:
        #call the respective function to "populate" the vagrant file
        typeOfDevice = device[1]["Type"]
        print("the device is a " + typeOfDevice)

        if typeOfDevice is "Host":
            writeHost(VagrantFile,device)

        if typeOfDevice is "Switch":
            writeSwitch(VagrantFile,device)

        if typeOfDevice is "Router":
            writeRouter(VagrantFile,device)

    VagrantFile.close()
    f = open("VagrantFromScript.txt", "r")
    print(f.read())

main()
