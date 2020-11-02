import os


def create_vagrantfile(configuration):
    directory = configuration[5] + "/Vagrantfile"
    f = open(directory, "w+")
    f.write("# -*- mode: ruby -*- \n# vi: set ft=ruby :\n\n")

    #Desktop environment script
    if(configuration[1]!="No Desktop Environment"):
        f.write("$script = <<-SCRIPT\n")
        if(configuration[0][0] == "u"):
            f.write("sudo apt update\n")
            if(configuration[1] == "Gnome"):
                f.write("sudo apt -y install gnome-session\n")
            if(configuration[1] == "KDE"):
                f.write("sudo apt -y install kubuntu-desktop\n")
            if(configuration[1] == "XFCE"):
                f.write("sudo apt -y install xubuntu-desktop\n")
            if(configuration[1] == "Mate"):
                f.write("sudo apt -y install ubuntu-mate-desktop\n")
            f.write("sudo reboot\n")
        if(configuration[0][0] == "d"):
            f.write("sudo apt-get update\n")
            if (configuration[1] == "Gnome"):
                f.write("sudo apt-get -y install task-gnome-desktop\n")
            if (configuration[1] == "KDE"):
                f.write("sudo apt-get -y install task-kde-desktop\n")
            if (configuration[1] == "XFCE"):
                f.write("sudo apt-get -y install task-xfce-desktop\n")
            if (configuration[1] == "Mate"):
                f.write("sudo apt-get -y install task-mate-desktop\n")
            f.write("sudo reboot\n")
        if(configuration[0][0] == "c"):
            if (configuration[1] == "Gnome"):
                f.write("yum -y groups install \"GNOME Desktop\"\n")
                f.write("echo \"exec gnome-session\" >> ~/.xinitrc\n")
            if (configuration[1] == "KDE"):
                f.write("yum -y groups install \"KDE Plasma Workspaces\"\n")
                f.write("echo \"exec startkde\" >> ~/.xinitrc\n")
            if (configuration[1] == "XFCE"):
                f.write("yum --enablerepo=epel -y groups install \"Xfce\"\n")
                f.write("echo \"exec /usr/bin/xfce4-session\" >> ~/.xinitrc\n")
            if (configuration[1] == "Mate"):
                f.write("yum --enablerepo=epel -y groups install \"MATE Desktop\"\n")
                f.write("echo \"exec /usr/bin/mate-session\" >> ~/.xinitrc\n")
            f.write("startx\n")
        f.write("SCRIPT\n\n")

    #Virtual machine configuration
    f.write("Vagrant.configure(\"2\") do |config|\n")
    f.write("\tconfig.vm.box = \"" + configuration[0] + "\"\n")
    f.write("\tconfig.vm.host_name = \"" + configuration[5] + "\"\n")
    f.write("\tconfig.vm.provider \"virtualbox\" do |vb|\n")
    f.write("\t\tvb.gui = true\n")
    f.write("\t\tvb.memory = " + configuration[3] + "\n")
    f.write("\t\tvb.cpus = " + configuration[2] + "\n")
    if(configuration[4] != "0"):
        f.write("\t\tvb.customize [\"modifyvm\", :id, \"--vram\", \"" + configuration[4] + "\"]\n")
    f.write("\tend\n")
    if (configuration[1] != "No Desktop Environment"):
        f.write("\tconfig.vm.provision \"shell\", inline: $script\n")
    f.write("end\n")

    f.close()

def create_folder(vm_name):
    directory = vm_name
    if not os.path.exists(directory):
        os.makedirs(directory)