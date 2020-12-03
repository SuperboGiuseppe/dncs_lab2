import gui
import vagrantfilecreator as vagrant
import os

def main():
    #Retrieve vm configuration from the UI
    gui.main_application()

    #Create folder for the vagrant VM
    #vagrant.create_folder(configuration[5])
    #vagrant.create_vagrantfile(configuration)

    #Run vagrant inside the VM folder
    #print(configuration)
    #os.chdir(configuration[5])
    #os.system("vagrant up")

if __name__ == '__main__':
    main()