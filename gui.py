""" _____________________________________________________________

    Description: User interface code of the network designer
    Author: Giuseppe Superbo (giuseppe.superbo@studenti.unitn.it)
    Date: Winter 2020-2021
    Course: Design of Networks and Communication Systems
    _____________________________________________________________
"""

import sys, os
from PyQt5 import QtGui, QtWidgets, QtCore, uic, QtWebEngineWidgets
from pyvis.network import Network
import matplotlib.image as mpimg
import numpy
import network_core

"""
Custom Libraries
"""
custom_lib_path = os.path.abspath(os.path.abspath("./fromHTMLtoVagrant"))
sys.path.append(custom_lib_path)
import vagrantConverterCollector

class network_design_window(QtWidgets.QMainWindow):
    """
    Class from which it is possible to instantiate the main window. 
    This window contains the design network canvas and all the functionalities related to it.

    """
    errorSignal = QtCore.pyqtSignal(str)
    outputSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        """Default method that initializes the instance of the main_window.

              Parameters:
                - self: current instance of the class.
            
              Attributes:
                - current_network: network currently active for any edit;
                - current_network_name: name of the current network
                - network_wizard: network wizard window object (Inheritance model)
                - editor_window: editor window object (Inheritance model)

        """
        super(network_design_window, self).__init__()
        self.initialize_window()

    def initialize_window(self):
        """Method that initializes all the components of the main window.

              Parameters:
                - self: current instance of the class.
        """
        self.current_network = network_core.create_network()
        self.current_network_name = ""
        self.current_network_path = ""
        self.current_network_template = ""
        self.current_network_deployed = 0
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle("Virtual Network automated deployment via Vagrant")
        self.main_toolbar()
        self.statusbar()
        self.setWindowIcon(QtGui.QIcon("./Images/network.png"))
        self.main_frame = QtWidgets.QWidget()
        self.main_frame_layout = QtWidgets.QVBoxLayout(self.main_frame)
        self.setCentralWidget(self.main_frame)
        self.canvas_html()
        self.debug_console()
        self.network_wizard = new_network_wizard(self)
        self.editor_window = editor_components(self)
        self.dashboard_window = dashboard_vms(self)
        self.edge_window = edge_editors(self)
        self.vagrant_process = QtCore.QProcess(self)
        self.vagrant_process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.vagrant_process.readyReadStandardError.connect(self.onReadyReadStandardError)


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
        self.main_toolbar = QtWidgets.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.main_toolbar)
        self.main_toolbar.setIconSize(QtCore.QSize(64,64))
        self.main_toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.button_router = QtWidgets.QAction(QtGui.QIcon("./Images/router.png"), "Label", self)
        self.button_router.setStatusTip("Add a router to the network")
        self.button_router.setToolTip("Add a router to the network")
        self.button_router.setIconText("Router")
        self.button_router.setDisabled(True)
        
        self.button_switch = QtWidgets.QAction(QtGui.QIcon("./Images/switch.png"), "Label", self)
        self.button_switch.setStatusTip("Add a switch to the network")
        self.button_switch.setToolTip("Add a switch to the network")
        self.button_switch.setIconText("Switch")
        self.button_switch.setDisabled(True)

        self.button_host = QtWidgets.QAction(QtGui.QIcon("./Images/host.png"), "Label", self)
        self.button_host.setStatusTip("Add a host to the network")
        self.button_host.setToolTip("Add a host to the network")
        self.button_host.setIconText("Host")
        self.button_host.setDisabled(True)

        self.button_editor = QtWidgets.QAction(QtGui.QIcon("./Images/tool.png"), "Label", self)
        self.button_editor.setStatusTip("Edit virtual network devices")
        self.button_editor.setToolTip("Edit virtual network devices")
        self.button_editor.setIconText("Edit configuration")
        self.button_editor.triggered.connect(lambda: self.editor_window.show())
        self.button_editor.setDisabled(True)

        self.button_edge = QtWidgets.QAction(QtGui.QIcon("./Images/edge.png"), "Label", self)
        self.button_edge.setStatusTip("Edit edge/link characteristics")
        self.button_edge.setToolTip("Edit edge/link characteristics")
        self.button_edge.setIconText("Edge configuration")
        self.button_edge.triggered.connect(lambda: self.edge_window.show())
        self.button_edge.setDisabled(True)

        self.button_new = QtWidgets.QAction(QtGui.QIcon("./Images/newfile.png"), "Label", self)
        self.button_new.setStatusTip("Create a new network")
        self.button_new.setToolTip("Create a new network")
        self.button_new.setIconText("New Network")
        self.button_new.triggered.connect(lambda: self.network_wizard.show())

        self.button_save = QtWidgets.QAction(QtGui.QIcon("./Images/save.png"), "Label", self)
        self.button_save.setStatusTip("Save the current network")
        self.button_save.setToolTip("Save the current network")
        self.button_save.setIconText("Save Network")
        self.button_save.triggered.connect(lambda: self.save_file_window())
        self.button_save.setDisabled(True)

        self.button_open = QtWidgets.QAction(QtGui.QIcon("./Images/openfile.png"), "Label", self)
        self.button_open.setStatusTip("Open an existent network")
        self.button_open.setToolTip("Open an existent network")
        self.button_open.setIconText("Open Network")
        self.button_open.triggered.connect(lambda: self.open_file_window())

        self.button_vagrant = QtWidgets.QAction(QtGui.QIcon("./Images/vagrant.png"), "Label", self)
        self.button_vagrant.setStatusTip("Deploy the virtual network via vagrant")
        self.button_vagrant.setToolTip("Deploy the virtual network via vagrant")
        self.button_vagrant.setIconText("Deploy network")
        self.button_vagrant.triggered.connect(lambda: self.vagrant_execution())
        self.button_vagrant.setDisabled(True)

        self.button_dashboard = QtWidgets.QAction(QtGui.QIcon("./Images/dashboard.png"), "Label", self)
        self.button_dashboard.setStatusTip("Open the statistics and control dashboard of the deployed network")
        self.button_dashboard.setToolTip("Open the statistics and control dashboard of the deployed network")
        self.button_dashboard.setIconText("Control dashboard")
        self.button_dashboard.triggered.connect(lambda: self.dashboard_window.show())
        self.button_dashboard.setDisabled(True)

        self.button_terminal = QtWidgets.QAction(QtGui.QIcon("./Images/terminal.png"), "Label", self)
        self.button_terminal.setStatusTip("Open the debug console")
        self.button_terminal.setToolTip("Open the debug console")
        self.button_terminal.setIconText("Debug console")
        self.button_terminal.triggered.connect(lambda: self.debug_console_frame.setVisible(False) if self.debug_console_frame.isVisible() else self.debug_console_frame.setVisible(True))
           
        
        self.main_toolbar.addAction(self.button_new)
        self.main_toolbar.addAction(self.button_save)
        self.main_toolbar.addAction(self.button_open)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.button_router)
        self.main_toolbar.addAction(self.button_switch)
        self.main_toolbar.addAction(self.button_host)
        self.main_toolbar.addAction(self.button_editor)
        self.main_toolbar.addAction(self.button_edge)
        self.main_toolbar.addSeparator()
        self.main_toolbar.addAction(self.button_vagrant)
        self.main_toolbar.addAction(self.button_dashboard)
        self.main_toolbar.addAction(self.button_terminal)


    def statusbar(self):
        """Method that defines the statusbar at the bottom of the main window. This status bar is used to prompt hints or low priority messages from the application.

              Parameters:
                - self: current instance of the class.

        """
        self.statusBar().showMessage("No deployed network")


    def enable_buttons_editing(self):
        self.button_save.setEnabled(True)
        self.button_vagrant.setEnabled(True)
        self.button_editor.setEnabled(True)
        self.button_edge.setEnabled(True)
        
    
    def canvas_html(self):
        """Method that defines the canvas where the network is prompted.

              Parameters:
                - self: current instance of the class.

        """
        QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars=False
        self.canvas_frame = QtWebEngineWidgets.QWebEngineView()
        self.main_frame_layout.addWidget(self.canvas_frame)
        
        
    
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
        if(len(file_path) > 2):
            self.current_network = network_core.open_network(file_path[0])
            self.update_canvas_html(os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html"))
            self.current_network_path = os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html")
            self.editor_window = editor_components(self)
            self.dashboard_window = dashboard_vms(self)
            self.edge_window = edge_editors(self)
            self.enable_buttons_editing()
        
    
    def save_file_window(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, 'SaveFile')
        self.current_network.save_graph(file_path[0])

    def debug_console(self):
        self.debug_console_frame = QtWidgets.QWidget(self.main_frame)
        self.debug_console_layout = QtWidgets.QVBoxLayout()
        self.debug_console_frame.setLayout(self.debug_console_layout)
        self.debug_console_textedit = QtWidgets.QPlainTextEdit()
        self.debug_console_textedit.setReadOnly(True)
        self.debug_console_frame.move(5,430)
        self.debug_console_frame.setMinimumHeight(220)
        self.debug_console_frame.setMinimumWidth(1015)
        self.debug_console_textedit.resize(self.debug_console_textedit.sizeHint().width(), self.debug_console_textedit.minimumHeight())
        self.debug_console_textedit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.debug_console_label = QtWidgets.QLabel("Debug console")
        self.debug_console_layout.addWidget(self.debug_console_label)
        self.debug_console_layout.addWidget(self.debug_console_textedit)
        self.debug_console_frame.hide()

    def vagrant_execution(self):
        os.chdir("./NetworkGraphs")
        os.mkdir(self.current_network_name)
        os.chdir("./" + self.current_network_name)
        print("./" + self.current_network_name)
        print(self.current_network_template)
        vagrantConverterCollector.converter_selector(self.current_network_path, self.current_network_template)
        #self.debug_console_textedit.clear()
        #self.vagrant_process.start('vagrant up')

    
    def onReadyReadStandardOutput(self):
        result = self.vagrant_process.readAllStandardOutput().data().decode()
        self.debug_console_textedit.appendPlainText(result)
        self.outputSignal.emit(result)
    
    def onReadyReadStandardError(self):
        error = self.vagrant_process.readAllStandardError().data().decode()
        self.debug_console_textedit.appendPlainText(error)
        self.errorSignal.emit(error)
        
        
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
              
              Attributes:
                - main_window_object: reference of the object that has istantiated an object from this class;
                - templates_directory_path: absolute path of the template directory used in the wizard selection;
                - page_start, group_buttons: starting page object of the wizard and its buttons choice;
                - scratch_page: scratch page object where it is possible to insert the details for creating a network from scratch;
                - scratch_id: scratch page id;
                - template_page: template page object where it is possible to insert the details for creating a network from a template;
                - template_id: template page id;

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
            template_path = self.templates_directory_path + "\\" + self.template_page.field("network_path")
            self.main_window_object.current_network_template = template_path.split("\\")[len(template_path.split("\\"))-1].split("_")[0]
            self.main_window_object.current_network = network_core.open_network(template_path)
            self.main_window_object.current_network_name = self.template_page.field("network_name")
            self.main_window_object.update_canvas_html(os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html"))
            self.main_window_object.current_network_path = os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html")
            self.main_window_object.editor_window = editor_components(self.main_window_object)
            self.main_window_object.dashboard_window = dashboard_vms(self.main_window_object)
            self.main_window_object.edge_window = edge_editors(self.main_window_object)
            self.main_window_object.enable_buttons_editing()
        else:
            print(self.scratch_page.field("network_name_scratch"))
            self.main_window_object.current_network_name = self.template_page.field("network_path")


class dashboard_vms(QtWidgets.QMainWindow):

    def __init__(self, main_window):
        super(dashboard_vms, self).__init__()
        self.main_window_object = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("Control dashboard")
        self.setWindowIcon(QtGui.QIcon("./Images/dashboard.png"))
        self.label_combobox = QtWidgets.QLabel("Select the virtual machine:")
        self.vm_combobox = QtWidgets.QComboBox()
        self.vm_names()
        self.graphs_frame = QtWidgets.QWidget()
        self.graphs_frame_layout = QtWidgets.QGridLayout()
        self.images_placeholder()
        self.graphs_frame.setLayout(self.graphs_frame_layout)
        self.button_frame = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setAlignment(QtCore.Qt.AlignRight)
        self.button_ssh = QtWidgets.QPushButton("SSH Connection")
        self.button_ssh.clicked.connect(self.ssh_connection)
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        self.button_layout.addWidget(self.button_ssh)
        self.button_layout.addWidget(self.button_cancel)
        self.button_frame.setLayout(self.button_layout)
        self.layout.addWidget(self.label_combobox)
        self.layout.addWidget(self.vm_combobox)
        self.layout.addWidget(self.graphs_frame)
        self.layout.addWidget(self.button_frame)
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def ssh_connection(self):
        current_vm = self.vm_combobox.currentText()
        command = "start cmd /k vagrant ssh " + current_vm
        os.system(command)
    
    def vm_names(self):
        nodes = self.main_window_object.current_network.nodes
        for node in nodes:
            self.vm_combobox.addItem(node["label"])

    def images_placeholder(self):
        self.label_matrix = []
        self.label_list1 = []
        self.label_list2 = []
        self.pixmap = QtGui.QPixmap('./Images/placeholder.png')
        self.pixmap2 = self.pixmap.scaledToHeight(300)
        for x in range(3):
            label = QtWidgets.QLabel()
            label.setPixmap(self.pixmap2)
            self.label_list1.append(label)
            label = QtWidgets.QLabel()
            label.setPixmap(self.pixmap2)
            self.label_list2.append(label)
        self.label_matrix.append(self.label_list1)
        self.label_matrix.append(self.label_list2)
        for x in range(2):
            for y in range(3):
                self.graphs_frame_layout.addWidget(self.label_matrix[x][y], x, y)


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

              Attributes:
                - main_window_object: reference of the object that has istantiated an object from this class;
                - tabs: tab collection object;
                - routers: list of routers from the current network;
                - swithces: list of switches from the current network;
                - hosts: list of hosts from the current network;
                - router_tab: tab form object where it is possible to edit routers configuration;
                - switch_tab: tab form object where it is possible to edit switches configuration;
                - host_tab: tab form object where it is possible to edit hosts configuration;
                - button_frame: frame object where all the buttons of the editor window are located;
                - button_layout: layout object for the buttons;
                - button_save: button object for saving the configuration;
                - button_cancel: button object for deleting the changes;
                - window: generic widget object that contains all the other widgets.

        """        
        super(editor_components, self).__init__()
        self.main_window_object = main_window
        self.temporary_network = self.main_window_object.current_network
        #print(self.temporary_network.nodes)
        self.resize(1024, 768)
        self.setWindowTitle("Editor virtual devices configuration")
        self.setWindowIcon(QtGui.QIcon("./Images/network.png"))
        self.tabs = QtWidgets.QTabWidget()
        self.routers = network_core.nodes_search_type(self.temporary_network, "router")
        self.switches = network_core.nodes_search_type(self.temporary_network, "switch")
        self.hosts = network_core.nodes_search_type(self.temporary_network, "host")
        self.others = network_core.nodes_search_type(self.temporary_network, "others")
        self.router_tab = self.editor_form("Router", self.routers)
        self.switch_tab = self.editor_form("Switch", self.switches)
        self.host_tab = self.editor_form("Host", self.hosts)
        self.other_tab = self.editor_form("Other", self.others)
        self.tabs.resize(1000,700)
        self.tabs.addTab(self.router_tab, "Routers")
        self.tabs.addTab(self.switch_tab, "Switches")
        self.tabs.addTab(self.host_tab, "Hosts")
        self.tabs.addTab(self.other_tab, "Others")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.button_frame = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setAlignment(QtCore.Qt.AlignRight)
        self.button_save = QtWidgets.QPushButton("Save")
        self.button_save.clicked.connect(self.on_save)
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.on_cancel)
        self.button_layout.addWidget(self.button_save)
        self.button_layout.addWidget(self.button_cancel)
        self.button_frame.setLayout(self.button_layout)
        self.layout.addWidget(self.button_frame)
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)
    
    def editor_form(self, type, devices):
        """Method that initializes a form which contains all the widgets from which it is possible to change the device configuration.

              Parameters:
                - self: current instance of the class;
                - type: type of the devices to be edit.
            
              Returns:
                - tab: QTab widget object that contains the initialized form of all the devices of the specific type.

        """
        tab = QtWidgets.QWidget()
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

            form_layout.addWidget(QtWidgets.QLabel("Custom script:"), 4, 0)
            
            custom_script_textbox = QtWidgets.QTextEdit()
            form_layout.addWidget(custom_script_textbox, 5,0,1,2)
            custom_script_textbox.textChanged.connect(lambda: (self.temporary_edits("custom_script", custom_script_textbox.toPlainText(), devices, devices_combobox.currentIndex())))


            self.set_qlines_text(edit_lines, devices, devices_combobox.currentIndex(), custom_script_textbox)
            self.set_network_table_content(network_configuration_table, devices, devices_combobox.currentIndex())
            network_configuration_table.cellChanged.connect(lambda: self.table_edits(network_configuration_table, devices, devices_combobox.currentIndex())) 
            devices_combobox.activated[str].connect(lambda: (self.set_qlines_text(edit_lines, devices, devices_combobox.currentIndex(), custom_script_textbox), self.set_network_table_content(network_configuration_table, devices, devices_combobox.currentIndex())))

            window_layout.addWidget(devices_label)
            window_layout.addWidget(devices_combobox)
            window_layout.addWidget(form)
        else:
            tab_layout = QtWidgets.QVBoxLayout(tab)
            tab_layout.addWidget(QtWidgets.QLabel("No " + type.lower() + " devices available in the network"))
        return tab

    def set_qlines_text(self, edit_lines, devices, index, custom_script_textbox):
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
        custom_script_textbox.setPlainText(devices[index]["custom_script"])

    
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
            for column in range(network_column_count-1):
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
    
    def on_save(self):
        """Method called when the user presses the save button in the editor configuration. It applies the changes in the temporary network and updates the network graph of the canvas.

              Parameters:
                - self: current instance of the class;

        """        
        G = Network()
        print(self.routers)
        print(self.switches)
        print(self.hosts)
        network_core.dictionary_to_nodes(self.routers, G)
        network_core.dictionary_to_nodes(self.switches, G)
        network_core.dictionary_to_nodes(self.hosts, G)
        network_core.dictionary_to_edges(self.temporary_network.edges, G)
        self.main_window_object.current_network = G
        G.save_graph("./NetworkGraphs/Temp_Network/temp_network.html")
        network_core.html_fix(os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html"))
        self.main_window_object.update_canvas_html(os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html"))
        self.close()
    
    def on_cancel(self):
        self.close()


class edge_editors(QtWidgets.QMainWindow):
    
    def __init__(self, main_window):
        super(edge_editors, self).__init__()
        self.main_window_object = main_window
        self.temporary_network = self.main_window_object.current_network
        self.setWindowIcon(QtGui.QIcon("./Images/edge.png"))
        self.setWindowTitle("Edit edges configuration")
        self.resize(512, 280)
        self.window_layout = QtWidgets.QGridLayout(self)
        self.edge_combobox = QtWidgets.QComboBox()
        self.edge_combobox.activated[str].connect(lambda: self.bandwidth_up_textbox.setText(str(self.edges[self.edge_combobox.currentIndex()]["bandwidth_up"])))
        self.edge_combobox.activated[str].connect(lambda: self.bandwidth_down_textbox.setText(str(self.edges[self.edge_combobox.currentIndex()]["bandwidth_down"])))
        self.collect_edges()
        self.bandwidth_up_textbox = QtWidgets.QLineEdit()
        self.bandwidth_up_textbox.textChanged[str].connect(lambda: (self.bandwidth_changes(self.edges, self.edge_combobox.currentIndex(), "bandwidth_up" , self.bandwidth_up_textbox.text())))
        self.bandwidth_down_textbox = QtWidgets.QLineEdit()
        self.bandwidth_down_textbox.textChanged[str].connect(lambda: (self.bandwidth_changes(self.edges, self.edge_combobox.currentIndex(), "bandwidth_down",self.bandwidth_down_textbox.text())))
        if len(self.edges) > 0:
            self.bandwidth_up_textbox.setText(str(self.edges[self.edge_combobox.currentIndex()]["bandwidth_up"]))
            self.bandwidth_down_textbox.setText(str(self.edges[self.edge_combobox.currentIndex()]["bandwidth_down"]))
        self.button_frame = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setAlignment(QtCore.Qt.AlignRight)
        self.button_save = QtWidgets.QPushButton("Save")
        self.button_save.clicked.connect(self.on_save)
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.on_close)
        self.button_layout.addWidget(self.button_save)
        self.button_layout.addWidget(self.button_cancel)
        self.button_frame.setLayout(self.button_layout)
        self.window_layout.addWidget(QtWidgets.QLabel("Select the edge:"), 0, 0)
        self.window_layout.addWidget(self.edge_combobox, 1, 0, 1, 2)
        self.window_layout.addWidget(QtWidgets.QLabel("Bandwidth uplink (Mbps):"), 2, 0)
        self.window_layout.addWidget(self.bandwidth_up_textbox, 2,1)
        self.window_layout.addWidget(QtWidgets.QLabel("Bandwidth downlink (Mbps):"), 3, 0)
        self.window_layout.addWidget(self.bandwidth_down_textbox, 3,1)
        self.window_layout.addItem(QtWidgets.QSpacerItem(400, 220), 4, 0, 1, 2)
        self.window_layout.addWidget(self.button_frame, 5, 0, 1, 2)
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.window_layout)
        self.setCentralWidget(self.window)

    
    def collect_edges(self):
        self.edges = self.temporary_network.edges
        self.devices = self.temporary_network.nodes
        print(self.edges)
        for edge in self.edges:
            self.edge_combobox.addItem(self.devices[edge["from"]-1]["label"] + " <----> " + self.devices[edge["to"]-1]["label"])
    
    def bandwidth_changes(self, edges, index, direction, new_value):
            if new_value == "":
                edges[index][direction] = 0
            else:
                edges[index][direction] = int(new_value)

    def on_save(self):
        """Method called when the user presses the save button in the editor configuration. It applies the changes in the temporary network and updates the network graph of the canvas.

              Parameters:
                - self: current instance of the class;

        """        
        G = Network()
        network_core.dictionary_to_nodes(self.devices, G)
        network_core.dictionary_to_edges(self.edges, G)
        self.main_window_object.current_network = G
        G.save_graph("./NetworkGraphs/Temp_Network/temp_network.html")
        network_core.html_fix(os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html"))
        self.main_window_object.update_canvas_html(os.path.abspath("./NetworkGraphs/Temp_Network/temp_network.html"))
        self.close()
    
    def on_close(self):
        self.close()




def main_application():
    application = QtWidgets.QApplication(sys.argv)
    user_interface = network_design_window()
    user_interface.show()
    sys.exit(application.exec_())

