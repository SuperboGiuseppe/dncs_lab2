import sys, os
from PyQt5 import QtGui, QtWidgets, QtCore, uic, QtWebEngineWidgets
from pyvis.network import Network
import matplotlib.image as mpimg
import numpy, html_fix
import network_core


class network_design_window(QtWidgets.QMainWindow):
    """
    Class from which it is possible to instantiate the main window. 
    This window contains the design network canvas and all the functionalities related to it.

    """
    def __init__(self):
        """Default method that initializes the instance of the main_window.

              Parameters:
                - self: current instance of the class.

        """
        super(network_design_window, self).__init__()
        self.initialize_window()

    def initialize_window(self):
        """Method that initializes all the components of the main window.

              Parameters:
                - self: current instance of the class.
        """
        self.current_network = Network()
        self.current_network_name = "Test"
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle("Virtual Network automated deployment via Vagrant")
        self.main_toolbar()
        self.statusbar()
        self.setWindowIcon(QtGui.QIcon("./Images/network.png"))
        self.canvas_html()
        self.network_wizard = new_network_wizard(self)
        self.editor_window = editor_components(self)


    def center(self):
        """Method that centers the main window depending on the user resolution.

              Parameters:
                - self: current instance of the class.

        """
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def main_toolbar(self):
        """Method that defines the toolbar with all the corresponding button/actions.

              Parameters:
                - self: current instance of the class.

        """       
        main_toolbar = QtWidgets.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, main_toolbar)
        main_toolbar.setIconSize(QtCore.QSize(64,64))
        main_toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        button_router = QtWidgets.QAction(QtGui.QIcon("./Images/router.png"), "Label", self)
        button_router.setStatusTip("Add a router to the network")
        button_router.setIconText("Router")
        
        button_switch = QtWidgets.QAction(QtGui.QIcon("./Images/switch.png"), "Label", self)
        button_switch.setStatusTip("Add a switch to the network")
        button_switch.setIconText("Switch")

        button_host = QtWidgets.QAction(QtGui.QIcon("./Images/host.png"), "Label", self)
        button_host.setStatusTip("Add a host to the network")
        button_host.setIconText("Host")

        button_editor = QtWidgets.QAction(QtGui.QIcon("./Images/tool.png"), "Label", self)
        button_editor.setStatusTip("Edit virtual network devices")
        button_editor.setIconText("Edit configuration")
        button_editor.triggered.connect(lambda: self.editor_window.show())

        button_new = QtWidgets.QAction(QtGui.QIcon("./Images/newfile.png"), "Label", self)
        button_new.setStatusTip("Create a new network")
        button_new.setIconText("New Network")
        button_new.triggered.connect(lambda: self.network_wizard.show())

        button_save = QtWidgets.QAction(QtGui.QIcon("./Images/save.png"), "Label", self)
        button_save.setStatusTip("Save the current network")
        button_save.setIconText("Save Network")

        button_open = QtWidgets.QAction(QtGui.QIcon("./Images/openfile.png"), "Label", self)
        button_open.setStatusTip("Open an existent network")
        button_open.setIconText("Open Network")
        button_open.triggered.connect(lambda: self.open_file_window())

        button_vagrant = QtWidgets.QAction(QtGui.QIcon("./Images/vagrant.png"), "Label", self)
        button_vagrant.setStatusTip("Deploy the virtual network via vagrant")
        button_vagrant.setIconText("Deploy network")

        button_dashboard = QtWidgets.QAction(QtGui.QIcon("./Images/dashboard.png"), "Label", self)
        button_dashboard.setStatusTip("Open the statistics and control dashboard of the deployed network")
        button_dashboard.setIconText("Control dashboard")
           
        main_toolbar.addAction(button_new)
        main_toolbar.addAction(button_save)
        main_toolbar.addAction(button_open)
        main_toolbar.addSeparator()
        main_toolbar.addAction(button_router)
        main_toolbar.addAction(button_switch)
        main_toolbar.addAction(button_host)
        main_toolbar.addAction(button_editor)
        main_toolbar.addSeparator()
        main_toolbar.addAction(button_vagrant)
        main_toolbar.addAction(button_dashboard)


    def statusbar(self):
        """Method that defines the statusbar at the bottom of the main window. This status bar is used to prompt hints or low priority messages from the application.

              Parameters:
                - self: current instance of the class.

        """
        self.statusBar().showMessage("No deployed network")


    def canvas_html(self):
        """Method that defines the canvas where the network is prompted.

              Parameters:
                - self: current instance of the class.

        """
        self.canvas_frame = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.canvas_frame)
    
    def update_canvas_html(self, html_path):
        """Method that updates the content of the canvas with a different html network file.

              Parameters:
                - self: current instance of the class;
                - html_path: absolute path of the html network file.
        """
        self.canvas_frame.load(QtCore.QUrl.fromLocalFile(html_path))
    
    def open_file_window(self):
        """Method that prompt an explorer window for opening a new html network file.

              Parameters:
                - self: current instance of the class.
        """
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile')
        self.update_canvas_html(file_path[0])
        self.current_network = network_core.open_network(file_path[0])
        self.editor_window = editor_components(self)
    
        

class new_network_wizard(QtWidgets.QWizard):
    """
    Class from which it is possible to instantiate the wizard window. 
    From this wizard it is possible to create a new network from scratch or from an existing template.

    """

    def __init__(self, main_window):
        """Default method that initializes the instance of the main_window.

              Parameters:
                - self: current instance of the class;
                - main_window: reference of the main window calling instance.

        """
        super(new_network_wizard, self).__init__()
        self.main_window_object = main_window
        self.templates_directory_path = os.path.abspath("./NetworkGraphs/Template")
        self.page_start, self.group_buttons = self.page_network_source()
        self.setWindowIcon(QtGui.QIcon("./Images/plus.png"))
        self.addPage(self.page_start)
        self.scratch_page = self.page_network_scratch()
        self.scratch_page.setFinalPage(True)
        self.scratch_id = self.addPage(self.scratch_page)
        self.template_page = self.page_network_template()
        self.template_id = self.addPage(self.template_page)
        self.currentIdChanged.connect(self.hide_next)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.onFinish)
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        self.setWindowTitle("New virtual network")
        self.resize(640,540)

    def hide_next(self):
        """Method that hides the default next button on a specific wizard page.

              Parameters:
                - self: current instance of the class.

        """
        if self.currentPage() == self.scratch_page:
            self.button(QtWidgets.QWizard.NextButton).hide()

    def nextId(self):
        """Method that retrieves the next wizard page ID. This method is crucial for the tree structure of the wizard.

              Parameters:
                - self: current instance of the class.

        """
        choice = self.group_buttons.checkedButton().text()
        if self.currentPage() == self.page_start:
            if "Create" in choice:
                return self.scratch_id
            return self.template_id
        return QtWidgets.QWizard.nextId(self)        
            
    def page_network_source(self):
        """Method that initializes the wizard page from which it is possible to choose the source of the new network.

              Parameters:
                - self: current instance of the class.

        """
        page = QtWidgets.QWizardPage(self)
        page.setTitle("Choose your starting point")
        label = QtWidgets.QLabel("Select if you want to start from a template network or from scratch:")
        group_radiobutton = QtWidgets.QButtonGroup(page)
        radiobutton_option1 = QtWidgets.QRadioButton("Create a new network from scratch")
        group_radiobutton.addButton(radiobutton_option1)
        radiobutton_option1.setChecked(True)
        radiobutton_option2 = QtWidgets.QRadioButton("Import a network from a template")
        radiobutton_option2.setChecked(False)
        group_radiobutton.addButton(radiobutton_option2)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(radiobutton_option1)
        layout.addWidget(radiobutton_option2)
        page.setLayout(layout)
        return page, group_radiobutton

    def page_network_scratch(self):
        """Method that initializes the wizard page from which it is possible to create a network from scratch by inputting the new network name.

              Parameters:
                - self: current instance of the class.

        """
        page = QtWidgets.QWizardPage(self)
        page.setTitle("New network from scratch")
        label = QtWidgets.QLabel("Insert the following details of your new virtual network:")
        layout = QtWidgets.QFormLayout(page)
        textbox_label = QtWidgets.QLabel("Insert the network name:")
        textbox_name = QtWidgets.QLineEdit(page)
        textbox_layout = QtWidgets.QHBoxLayout()
        textbox_layout.addWidget(textbox_label)
        textbox_layout.addWidget(textbox_name)
        layout.addRow(label)
        layout.addRow(textbox_layout)
        page.registerField("network_name_scratch", textbox_name)
        return page

    def page_network_template(self):
        """Method that initializes the wizard page from which it is possible to create a network from template by inputting the new network name and choosing a network template.

              Parameters:
                - self: current instance of the class.

        """ 
        page = QtWidgets.QWizardPage(self)
        page.setTitle("New network from template")
        templates_list = [ f for f in os.listdir(self.templates_directory_path) if os.path.isfile(os.path.join(self.templates_directory_path,f)) ]
        label = QtWidgets.QLabel("Select the starting template for your new virtuale network:")
        textbox_label = QtWidgets.QLabel("Insert the network name:")
        textbox_name = QtWidgets.QLineEdit(page)
        templates_combobox = QtWidgets.QComboBox(page)
        for template in templates_list:
            templates_combobox.addItem(template)
        preview_frame = QtWebEngineWidgets.QWebEngineView(page)
        preview_frame.load(QtCore.QUrl.fromLocalFile(self.templates_directory_path + "/" + str(templates_combobox.currentText())))
        preview_frame.setFixedSize(600,350)
        preview_frame.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)
        preview_frame.setZoomFactor(0.65)
        preview_frame.page().runJavaScript("window.scrollTo(100,100)")
        templates_combobox.activated[str].connect(lambda: preview_frame.load(QtCore.QUrl.fromLocalFile(self.templates_directory_path + "/" + str(templates_combobox.currentText()))))
        layout = QtWidgets.QFormLayout(page)
        layout.addRow(label)
        layout.addRow(templates_combobox)
        textbox_layout = QtWidgets.QHBoxLayout()
        textbox_layout.addWidget(textbox_label)
        textbox_layout.addWidget(textbox_name)
        layout.addRow(textbox_layout)
        layout.addRow(preview_frame)
        page.registerField("network_name", textbox_name)
        page.registerField("network_path", templates_combobox, "currentText")
        return page
    
    def onFinish(self):
        """Method called when the finish button of the wizard is pushed. It creates a new network based on the user choices and makes it available on the main editor.

              Parameters:
                - self: current instance of the class.

        """
        if self.currentId() == self.template_id:
            self.main_window_object.update_canvas_html(self.templates_directory_path + "/" + self.template_page.field("network_path"))
            self.main_window_object.current_network = network_core.open_network(self.templates_directory_path + "/" + self.template_page.field("network_path"))
            self.main_window_object.editor_window = editor_components(self.main_window_object)
            self.main_window_object.current_network_name = self.template_page.field("network_path")
        else:
            print(self.scratch_page.field("network_name_scratch"))
            self.main_window_object.current_network_name = self.template_page.field("network_path")

class editor_components(QtWidgets.QMainWindow):
    """
    Class from which it is possible to instantiate the device editor window. 
    This window contains all the details of each component that can be changed in order to create a new configuration.

    """
    def __init__(self, main_window):
        """Default method that initializes the instance of the device editor window.

              Parameters:
                - self: current instance of the class;
                - main_window: reference of the main window calling instance.

        """        
        super(editor_components, self).__init__()
        self.main_window_object = main_window
        self.temporary_network = self.main_window_object.current_network
        self.resize(1024, 768)
        self.setWindowTitle("Editor virtual devices configuration")
        self.setWindowIcon(QtGui.QIcon("./Images/network.png"))
        self.tabs = QtWidgets.QTabWidget()
        self.router_tab = self.editor_form("Router")
        self.switch_tab = self.editor_form("Switch")
        self.host_tab = self.editor_form("Host")
        self.tabs.resize(1000,700)
        self.tabs.addTab(self.router_tab, "Routers")
        self.tabs.addTab(self.switch_tab, "Switches")
        self.tabs.addTab(self.host_tab, "Hosts")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.button_frame = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setAlignment(QtCore.Qt.AlignRight)
        self.button_save = QtWidgets.QPushButton("Save")
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        self.button_layout.addWidget(self.button_save)
        self.button_layout.addWidget(self.button_cancel)
        self.button_frame.setLayout(self.button_layout)
        self.layout.addWidget(self.button_frame)
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)
    
    def editor_form(self, type):
        """Method that initializes a form which contains all the widgets from which it is possible to change the device configuration.

              Parameters:
                - self: current instance of the class;
                - type: type of the devices to be edit.
            
              Returns:
                - tab: QTab widget object that contains the initialized form of all the devices of the specific type.

        """
        tab = QtWidgets.QWidget()
        devices = network_core.nodes_search_type(self.temporary_network, type.lower())
        edit_lines = {}
        if len(devices) > 0:
            window_layout = QtWidgets.QVBoxLayout(tab)
            form = QtWidgets.QGroupBox(type + " configuration")
            form.setFixedSize(1000, 700)
            form_layout = QtWidgets.QGridLayout(self)
            form.setLayout(form_layout)
            form.setAlignment(QtCore.Qt.AlignTop)
            devices_label = QtWidgets.QLabel("Select the device to be configured:")
            devices_combobox =  QtWidgets.QComboBox()
            for device in devices:
                devices_combobox.addItem(device["label"])
            
            devices_combobox.setItemText
            form_0_0 = QtWidgets.QWidget()
            form_0_0_layout = QtWidgets.QHBoxLayout()
            form_0_0.setLayout(form_0_0_layout)
            edit_lines["device_name_box"] = QtWidgets.QLineEdit()
            edit_lines["device_name_box"].textChanged[str].connect(lambda: (self.temporary_edits("label", edit_lines["device_name_box"].text(), devices, devices_combobox.currentIndex()), devices_combobox.setItemText(devices_combobox.currentIndex(), edit_lines["device_name_box"].text())))
            
            form_0_0_layout.addWidget(QtWidgets.QLabel("Device name:"))
            form_0_0_layout.addWidget(edit_lines["device_name_box"])
    
            form_0_1 = QtWidgets.QWidget()
            form_0_1_layout = QtWidgets.QHBoxLayout()
            form_0_1.setLayout(form_0_1_layout)
            edit_lines["vm_image"] = QtWidgets.QLineEdit()
            edit_lines["vm_image"].textChanged[str].connect(lambda: (self.temporary_edits("vm_image", edit_lines["vm_image"].text(), devices, devices_combobox.currentIndex())))
            form_0_1_layout.addWidget(QtWidgets.QLabel("Image OS:         "))
            form_0_1_layout.addWidget(edit_lines["vm_image"])
    
                   
            form_layout.addWidget(form_0_0, 0, 0)
            form_layout.addWidget(form_0_1, 0, 1)
    
    
            form_1_0 = QtWidgets.QWidget()
            form_1_0_layout = QtWidgets.QHBoxLayout()
            form_1_0.setLayout(form_1_0_layout)
            edit_lines["ram"] = QtWidgets.QLineEdit()
            edit_lines["ram"].textChanged[str].connect(lambda: (self.temporary_edits("ram", edit_lines["ram"].text(), devices, devices_combobox.currentIndex())))
            form_1_0_layout.addWidget(QtWidgets.QLabel("RAM (MB):    "))
            form_1_0_layout.addWidget(edit_lines["ram"])
    
            form_1_1 = QtWidgets.QWidget()
            form_1_1_layout = QtWidgets.QHBoxLayout()
            form_1_1.setLayout(form_1_1_layout)
            edit_lines["number_cpus"] = QtWidgets.QLineEdit()
            edit_lines["number_cpus"].textChanged[str].connect(lambda: (self.temporary_edits("n_cpus", edit_lines["number_cpus"].text(), devices, devices_combobox.currentIndex())))           
            form_1_1_layout.addWidget(QtWidgets.QLabel("Number of CPUs:"))
            form_1_1_layout.addWidget(edit_lines["number_cpus"])
    
            form_layout.addWidget(form_1_0, 1, 0)
            form_layout.addWidget(form_1_1, 1, 1)
    
            form_layout.addWidget(QtWidgets.QLabel("Network configuration:"), 2, 0)
    
            network_configuration_table = QtWidgets.QTableWidget()
            network_configuration_table.setColumnCount(3)
            network_configuration_table_header = network_configuration_table.horizontalHeader()
            network_configuration_table_header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            network_configuration_table.setHorizontalHeaderLabels(["Ip Address", "Netmask", "Interface"])
            network_configuration_table.verticalHeader().hide()
            form_layout.addWidget(network_configuration_table, 3, 0, 1, 2)

            self.set_qlines_text(edit_lines, devices, devices_combobox.currentIndex())
            self.set_network_table_content(network_configuration_table, devices, devices_combobox.currentIndex())
            network_configuration_table.cellChanged.connect(lambda: self.table_edits(network_configuration_table, devices, devices_combobox.currentIndex())) 
            devices_combobox.activated[str].connect(lambda: (self.set_qlines_text(edit_lines, devices, devices_combobox.currentIndex()), self.set_network_table_content(network_configuration_table, devices, devices_combobox.currentIndex())))

            window_layout.addWidget(devices_label)
            window_layout.addWidget(devices_combobox)
            window_layout.addWidget(form)
        else:
            tab_layout = QtWidgets.QVBoxLayout(tab)
            tab_layout.addWidget(QtWidgets.QLabel("No " + type.lower() + " devices available in the network"))
        return tab

    def set_qlines_text(self, edit_lines, devices, index):
        """Method that applies all the current configuration values in the specific form.

              Parameters:
                - self: current instance of the class;
                - edit_lines: all the textboxes that contains the input from the user;
                - devices: temporary dictionary;
                - index: current device index.

        """
        edit_lines["device_name_box"].setText(devices[index]["label"])
        edit_lines["vm_image"].setText(devices[index]["vm_image"])
        edit_lines["ram"].setText(devices[index]["ram"])
        edit_lines["number_cpus"].setText(str(devices[index]["n_cpus"]))
    
    def set_network_table_content(self, table, devices, index):
        """Method that applies all the current configuration values in the specific network configuration table.

              Parameters:
                - self: current instance of the class;
                - table: table that contains all the network interfaces configured in the current device;
                - devices: temporary dictionary;
                - index: current device index.

        """
        network_row_count = len(devices[index]["network_interfaces"])
        table.setRowCount(network_row_count)
        network_column_count = len(devices[index]["network_interfaces"][0])
            
        for row in range(network_row_count):
            for column in range(network_column_count):
                item = (list(devices[index]["network_interfaces"][row].values())[column])
                table.setItem(row, column, QtWidgets.QTableWidgetItem(item))
    
    def temporary_edits(self, key, new_value, devices, index):
        """Method called whenever a textbox content is modified. Every change is directly applied also to the temporary reference dictionary.

              Parameters:
                - self: current instance of the class;
                - key: characteristic that has been modified;
                - new_value: modified value;
                - devices: temporary dictionary;
                - index: current device index.

        """
        if key == "n_cpus":
            if new_value == "":
                devices[index][key] = 0
            else:
                devices[index][key] = int(new_value)
        else:
            devices[index][key] = new_value
    
    def table_edits(self, table, devices, index):
        """Method called whenever a cell of the network table is modified. Every change is directly applied also to the temporary reference dictionary.

              Parameters:
                - self: current instance of the class;
                - table: table where the change has been made;
                - devices: temporary dictionary;
                - index: current device index.

        """
        if (type(table.currentItem()) != type(None)):
            if (table.currentItem().column()==0):
                devices[index]["network_interfaces"][table.currentItem().row()]["ip_address"] = table.currentItem().text()
            if (table.currentItem().column()==1):
                devices[index]["network_interfaces"][table.currentItem().row()]["netmask"] = table.currentItem().text()
            if (table.currentItem().column()==2):
                devices[index]["network_interfaces"][table.currentItem().row()]["name_interface"] = table.currentItem().text()

def main_application():
    application = QtWidgets.QApplication(sys.argv)
    user_interface = network_design_window()
    user_interface.show()
    sys.exit(application.exec_())

