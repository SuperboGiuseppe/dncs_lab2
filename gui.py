from tkinter import *
from tkinter import ttk
from PIL import Image
import vagrantDB

selected_os = ""
selected_version = ""
current_oscombobox = 0
current_versioncombobox = 0
current_step = 0
selected_CPUs = 0
current_CPUs = 0
current_vmname = ""
selected_RAM = 0
current_RAM = 0
selected_VRAM = 0
current_VRAM = 0
selected_DE=""
current_DE=0



def main_window():
    global selected_os
    global current_oscombobox
    global current_versioncombobox
    global selected_version
    global current_vmname
    global selected_RAM
    global current_RAM
    global selected_VRAM
    global current_VRAM
    global selected_CPUs
    global current_CPUs
    global flag



    def os_step():

        global selected_os
        global current_oscombobox
        global current_versioncombobox
        global selected_version

        def oscombobox_changed(event):
            global selected_os
            global current_oscombobox
            versions_list.clear()
            description_list.clear()
            for version in vagrantDB.retrieve_versionsOS(os_combobox.get()):
                versions_list.append(version[0])
                description_list.append(version[1])
            versions_combobox['values'] = versions_list
            versions_combobox.current(0)
            description_label['text'] = description_list[0]
            selected_os = os_combobox.get()
            current_oscombobox = os_combobox.current()

        def versioncombobox_changed(event):
            global current_versioncombobox
            global selected_version
            selected_version = versions_combobox.get()
            current_versioncombobox = versions_combobox.current()
            description_label['text'] = description_list[versions_combobox.current()]
            description_label['justify'] = 'left'

        main_container.geometry("1010x465")

        # Title label
        Label(content_frame, text="Linux Distribution Choice", font=("Helvetica", "14", "bold")).grid(row=0, column=0,
                                                                                                      sticky=NW,
                                                                                                      columnspan=2)

        image_background = PhotoImage(file='images/linuxbar.png')
        image_canvas.config(width=191, height=462)
        image_canvas.itemconfig(image_on_canvas, image=image_background)
        image_canvas.image = image_background

        # Combobox distribution
        os_combobox = ttk.Combobox(content_frame, values=["ubuntu", "debian", "centos"])
        os_combobox.bind("<<ComboboxSelected>>", oscombobox_changed)
        os_combobox.current(0)
        selected_os = os_combobox.get()
        current_oscombobox = os_combobox.current()
        os_combobox.grid(row=2, column=0, sticky=W)

        # Combobox version
        versions_list = []
        description_list = []
        for version in vagrantDB.retrieve_versionsOS(os_combobox.get()):
            versions_list.append(version[0])
            description_list.append(version[1])
        versions_combobox = ttk.Combobox(content_frame, values=versions_list)
        versions_combobox.current(0)
        selected_version = versions_combobox.get()
        current_versioncombobox = versions_combobox.current()
        versions_combobox.bind("<<ComboboxSelected>>", versioncombobox_changed)
        description = description_list[0]
        versions_combobox.grid(row=4, column=0, sticky=NW)

        # Description label
        Label(content_frame, text="Description:").grid(row=5, column=0, sticky=NW, pady=(15, 0))
        description_label = Label(content_frame, text=description, borderwidth=2, relief="groove", width="100",
                                  anchor="w")
        description_label.grid(row=6, column=0, sticky=NW, columnspan=2)

        # Button configuration
        button_previous['state'] = DISABLED

        # Label widget
        Label(content_frame, text="Select a Linux distribution:").grid(row=1, column=0, sticky=NW)
        Label(content_frame, text="Select a version of the previous distribution:").grid(row=3, column=0, sticky=NW,
                                                                                         pady=(15, 0))

        content_frame.grid_rowconfigure(0, weight=1)

    def vm_step():
        global selected_RAM
        global current_RAM
        global selected_VRAM
        global current_VRAM
        global selected_CPUs
        global current_CPUs
        global current_vmname
        global selected_DE

        def CPUscombobox_changed(event):
            global current_CPUs
            global selected_CPUs
            selected_CPUs = CPUs_combobox.get()
            current_CPUs = CPUs_combobox.current()

        def RAMcombobox_changed(event):
            global current_RAM
            global selected_RAM
            selected_RAM = RAM_combobox.get()
            current_RAM = RAM_combobox.current()

        def VRAMcombobox_changed(event):
            global current_VRAM
            global selected_VRAM
            selected_VRAM = VRAM_combobox.get()
            current_VRAM = VRAM_combobox.current()

        def vmtextentrychange(*args):
            global current_vmname
            current_vmname = vmname_entry_content.get()

        main_container.geometry("1010x465")

        image_background = PhotoImage(file='images/linuxbar.png')
        image_canvas.config(width=191, height=462)
        image_canvas.itemconfig(image_on_canvas, image=image_background)
        image_canvas.image = image_background

        # Title label
        Label(content_frame, text="Virtual Machine Configuration", font=("Helvetica", "14", "bold")).grid(row=0,column=0,sticky=NW)
        Label(content_frame, width=59).grid(row=1, column=1, padx=1)

        # Label widgets
        Label(content_frame, text="Insert virtual machine name:").grid(row=1, column=0, sticky=NW, pady=(15, 0))
        Label(content_frame, text="Select number of CPUs:").grid(row=3, column=0, sticky=NW, pady=(15, 0))
        Label(content_frame, text="Select amount of RAM (MBytes):").grid(row=5, column=0, sticky=NW, pady=(15, 0))
        Label(content_frame, text="Select amount of VRAM (MBytes):").grid(row=7, column=0, sticky=NW, pady=(15, 0))

        # Text area
        vmname_entry_content = StringVar()
        vmname_entry_content.set(current_vmname)
        vmname_entry_content.trace("w", vmtextentrychange)
        vmname_entry = Entry(content_frame, textvariable=vmname_entry_content, width=40)
        vmname_entry.grid(row=2, column=0, sticky=NW)

        # Combobox CPUs number
        if(current_DE == 1):
            CPUs_combobox = ttk.Combobox(content_frame, values=["2", "3", "4", "5", "6", "7", "8"])
        else:
            CPUs_combobox = ttk.Combobox(content_frame, values=["1", "2", "3", "4", "5", "6", "7", "8"])
        CPUs_combobox.current(current_CPUs)
        selected_CPUs = CPUs_combobox.get()
        current_CPUs = CPUs_combobox.current()
        CPUs_combobox.bind("<<ComboboxSelected>>", CPUscombobox_changed)
        CPUs_combobox.grid(row=4, column=0, sticky=NW)

        # Combobox RAM amount
        if(current_DE==0):
            RAM_combobox = ttk.Combobox(content_frame, values=["128", "256", "512", "1024", "2048", "4096"])
        elif(current_DE == 1 or current_DE==2):
            RAM_combobox = ttk.Combobox(content_frame, values=["2048", "4096"])
        elif(current_DE == 3):
            RAM_combobox = ttk.Combobox(content_frame, values=["1024", "2048", "4096"])
        else:
            RAM_combobox = ttk.Combobox(content_frame, values=["512", "1024", "2048", "4096"])
        RAM_combobox.current(current_RAM)
        selected_RAM = RAM_combobox.get()
        current_RAM = RAM_combobox.current()
        RAM_combobox.bind("<<ComboboxSelected>>", RAMcombobox_changed)
        RAM_combobox.grid(row=6, column=0, sticky=NW)

        # Combobox VRAM amount
        if(current_DE==0 or current_DE==4):
            VRAM_combobox = ttk.Combobox(content_frame, values=["0","16", "32", "64", "128", "256", "512"])
        elif(current_DE == 3):
            VRAM_combobox = ttk.Combobox(content_frame, values=["64", "128", "256", "512"])
        elif(current_DE == 2):
            VRAM_combobox = ttk.Combobox(content_frame, values=["128", "256", "512"])
        elif(current_DE == 1):
            VRAM_combobox = ttk.Combobox(content_frame, values=["256", "512"])
        VRAM_combobox.current(current_RAM)
        selected_VRAM = VRAM_combobox.get()
        current_VRAM = VRAM_combobox.current()
        VRAM_combobox.bind("<<ComboboxSelected>>", VRAMcombobox_changed)
        VRAM_combobox.grid(row=8, column=0, sticky=NW)

        button_next.grid_remove()
        button_finish.grid(row=0, column=2)


    def de_step():
        global selected_DE
        global current_DE

        def DEcombobox_changed(event):
            global current_DE
            global selected_DE
            selected_DE = DE_combobox.get()
            current_DE = DE_combobox.current()
            set_image(selected_DE, selected_os)

        def set_image(desktop_environment,distribution):
            if(desktop_environment=="No Desktop Environment"):
                desktop_environment = "nogui"
            file_path = "images/" + distribution + "/" + desktop_environment + ".png"
            image_background_desktop = PhotoImage(file=file_path)
            image_canvas_desktop.itemconfig(image_on_canvas_desktop, image=image_background_desktop)
            image_canvas_desktop.image = image_background_desktop

        main_container.geometry("1010x665")

        # Button configuration
        if(button_finish.winfo_exists()):
            button_finish.grid_remove()
            button_next.grid(row=0, column=2)
        button_previous['state'] = ACTIVE

        # Title Label
        Label(content_frame, text="Desktop Environment Choice", font=("Helvetica", "14", "bold")).grid(row=0, column=0,sticky=NW)
        Label(content_frame, width=68).grid(row=0, column=1)

        # Side Bar Configuration
        image_background = PhotoImage(file='images/linuxbarextended.png')
        image_canvas.config(width=191, height=660)
        image_canvas.itemconfig(image_on_canvas, image = image_background)
        image_canvas.image = image_background

        Label(content_frame, text="Select a desktop environment:").grid(row=1, column=0, sticky=NW, pady=(15, 0))
        desktop_environments = ["No Desktop Environment", "Gnome", "KDE", "Mate", "XFCE"]
        DE_combobox = ttk.Combobox(content_frame, values=desktop_environments)
        DE_combobox.current(current_DE)
        selected_DE = DE_combobox.get()
        current_DE = DE_combobox.current()
        DE_combobox.bind("<<ComboboxSelected>>", DEcombobox_changed)
        DE_combobox.grid(row=2, column=0, sticky=W)
        image_canvas_desktop = Canvas(content_frame, width=750, height=520)
        image_background_desktop = PhotoImage(file='images/centOS/nogui.png')
        image_on_canvas_desktop = image_canvas_desktop.create_image(0,0,image=image_background_desktop, anchor=NW)
        image_canvas_desktop.image = image_background_desktop
        image_canvas_desktop.grid(row=3, column=0, rowspan=2, columnspan=2, pady=(10,0))

        set_image(selected_DE, selected_os)

    def prev_action():
        global current_step
        current_step -= 1
        step_choice(current_step)

    def next_action():
        global current_step
        current_step += 1
        step_choice(current_step)

    def step_choice(selected_step):
        for widget in content_frame.winfo_children():
            widget.grid_forget()
        if (selected_step == 0):
            os_step()
        if (selected_step == 1):
            de_step()
        if (selected_step == 2):
            vm_step()

    def finish_action():
        main_container.destroy()


    def cancel_action():
        exit()

    # Window settings
    main_container = Tk()
    main_container.title("Linux virtual machine configurator")
    main_container.geometry("1010x465")
    main_container.resizable(False, False)

    # Frames for widgets
    image_frame = ttk.Frame(master=main_container)
    content_frame = ttk.Frame(master=main_container)
    button_frame = ttk.Frame(master=main_container)

    # Background canvas
    image_canvas = Canvas(width=191, height=462)
    image_background = PhotoImage(file='images/linuxbar.png')
    image_on_canvas = image_canvas.create_image(0, 0, image=image_background, anchor=NW)
    image_canvas.grid(row=0, column=0, rowspan=2)

    # Button widgets
    button_previous = Button(master=button_frame, text="Previous", command=prev_action)
    button_next = Button(master=button_frame, text="Next", command=next_action)
    button_cancel = Button(master=button_frame, text="Cancel", command=cancel_action)
    button_finish = Button(master=button_frame, text="Finish", command=finish_action)
    button_cancel.grid(row=0, column=0)
    button_previous.grid(row=0, column=1)
    button_next.grid(row=0, column=2)

    # Frames packing
    content_frame.grid(row=0, column=1, sticky=W + E + S + N, ipadx=100, padx=5, pady=5, columnspan=2)
    button_frame.grid(row=1, column=2, sticky=S)

    # Activate main window
    os_step()
    main_container.mainloop()


def gui():
    main_window()
    results = [selected_version, selected_DE, selected_CPUs, selected_RAM, selected_VRAM, current_vmname]
    return results

if __name__ == '__main__':
    gui()
