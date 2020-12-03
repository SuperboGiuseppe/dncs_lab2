import sys, os
from PyQt5 import QtGui, QtWidgets, QtCore, uic, QtWebEngineWidgets
from pyvis.network import Network
import matplotlib.image as mpimg
import numpy, html_fix

#Class in order to instantiate the main window. This window contains the design network canvas and all the functionalities related to it.
class network_design_window(QtWidgets.QMainWindow):

    def __init__(self):
        super(network_design_window, self).__init__()
        self.initialize_window()

    def initialize_window(self):
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle("Virtual Network automated deployment via Vagrant")
        self.main_toolbar()
        self.statusbar()
        self.setWindowIcon(QtGui.QIcon("./Images/network.png"))
        self.canvas_html()

    #Method that centers the window depending on the user resolution
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #Method that defines the toolbar with all the corresponding buttons
    def main_toolbar(self):
        new_network = new_network_wizard()

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

        button_new = QtWidgets.QAction(QtGui.QIcon("./Images/newfile.png"), "Label", self)
        button_new.setStatusTip("Create a new network")
        button_new.setIconText("New Network")
        button_new.triggered.connect(lambda: new_network.show())

        button_open = QtWidgets.QAction(QtGui.QIcon("./Images/openfile.png"), "Label", self)
        button_open.setStatusTip("Open an existent network")
        button_open.setIconText("Open Network")

        button_vagrant = QtWidgets.QAction(QtGui.QIcon("./Images/vagrant.png"), "Label", self)
        button_vagrant.setStatusTip("Deploy the virtual network via vagrant")
        button_vagrant.setIconText("Deploy network")

        button_dashboard = QtWidgets.QAction(QtGui.QIcon("./Images/dashboard.png"), "Label", self)
        button_dashboard.setStatusTip("Open the statistics and control dashboard of the deployed network")
        button_dashboard.setIconText("Control dashboard")
        
        
        main_toolbar.addAction(button_new)
        main_toolbar.addAction(button_open)
        main_toolbar.addSeparator()
        main_toolbar.addAction(button_router)
        main_toolbar.addAction(button_switch)
        main_toolbar.addAction(button_host)
        main_toolbar.addSeparator()
        main_toolbar.addAction(button_vagrant)
        main_toolbar.addAction(button_dashboard)

    #Method that defines the statusbar at the bottom of the main window. This status bar is used to prompt hints or low priority messages from the application.
    def statusbar(self):
        self.statusBar().showMessage("No deployed network")

    #Method that defines the canvas to prompt the network visualization
    def canvas_html(self):
        self.canvas_frame = QtWebEngineWidgets.QWebEngineView()
        self.canvas_frame.load(QtCore.QUrl.fromLocalFile(os.path.abspath("test3.html")))
        self.setCentralWidget(self.canvas_frame)

#Class from which it is possible to instatiate the wizard network creation window whenever the button "New Network" is pressed.
class new_network_wizard(QtWidgets.QWizard):

    def __init__(self):
        super(new_network_wizard, self).__init__()
        self.page_start, self.group_buttons = self.page_network_source()
        self.setWindowIcon(QtGui.QIcon("./Images/plus.png"))
        self.addPage(self.page_start)
        self.scratch_page = self.page_network_scratch()
        self.scratch_page.setFinalPage(True)
        self.scratch_id = self.addPage(self.scratch_page)
        self.template_page = self.page_network_template()
        self.template_id = self.addPage(self.template_page)
        self.currentIdChanged.connect(self.hide_next)
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        self.setWindowTitle("New virtual network")
        self.resize(640,480)

    def hide_next(self):
        if self.currentPage() == self.scratch_page:
            self.button(QtWidgets.QWizard.NextButton).hide()
    def nextId(self):
        choice = self.group_buttons.checkedButton().text()
        if self.currentPage() == self.page_start:
            if "Create" in choice:
                return self.scratch_id
            return self.template_id
        return QtWidgets.QWizard.nextId(self)        
            
    def page_network_source(self):
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
        page = QtWidgets.QWizardPage(self)
        page.setTitle("New network from scratch")
        label = QtWidgets.QLabel("Insert the following details of your new virtual network:")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        return page

    def page_network_template(self):
        page = QtWidgets.QWizardPage(self)
        page.setTitle("New network from template")
        label = QtWidgets.QLabel("Select the starting template for your new virtuale network:")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        return page

    

def main_application():
    application = QtWidgets.QApplication(sys.argv)
    user_interface = network_design_window()
    user_interface.show()
    sys.exit(application.exec_())

