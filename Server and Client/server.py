import socket 
import threading

#those imports where added by luca
from matplotlib import pyplot as plt 
import os
from os import path
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys 


HEADER = 64 # It's header length, it can be change.
PORT = 5050 # port number where the server is going to talk (run).
SERVER = "192.168.53.133"  # this is ip of server, it can be change according to the server IP address.
#SERVER = socket.gethostbyname(socket.gethostname()) # this another way to give the iP address by host name.
ADDR = (SERVER, PORT) # here we have bind the server and port.
FORMAT = 'utf-8' # it's formate for the message
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Here we can create different kind of socket to get different kind of data. (socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) # here we have bound that with ADDR.

def handle_client(conn, addr): # funcation to handel the clients that are going to connect with server.
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # receiving information for the client.
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start(): # its just start the socket server for us.
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True: # it will keep listening until server crash or stop.
        conn, addr = server.accept() # for new connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#this function is to plot the TCP data given an array of value for X axis and another array of values of the same size for the Y axis
#the plot is an image file that can be found in the "/plot" directory
#this is just "standard" plot, not the cool-looking one with pyqt5
#this function was added by Luca
def save_plot(X,Y):
    if not path.exists("/plots"):
        os.system("mkdir plots")

    plt.title("TCP data")
    plt.xlabel("X values")
    plt.ylabel("Y values")

    plt.plot(X,Y) 
    plt.savefig("plots/TCPplot.png")
    plt.clf()

#this function is to plot the TCP data given using "X" and "Y" as arrays for the x and y axis
#this is just is supposed to be the cool-looking graph with pyqt5 :)
#the name of the function is create_plot() the class is used as a support it should not be used standalone
#this function was added by Luca
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.graphWidget.setTitle("TCP data")
        self.graphWidget.setLabel('left', 'Y axis label ')
        self.graphWidget.setLabel('bottom', 'X axis label')
        self.graphWidget.showGrid(x=True, y=True)

        #here self.x and self.y should be the arrays with data of x and y axis
        #now it's just random generated data, substitite it with the actually arrays
        self.x = list(range(100))  
        self.y = [randint(0,100) for _ in range(100)] 

        self.data_line = self.graphWidget.plot(self.x, self.y) #X,Y

        #stuff for updating 
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)

        #this is the function that need to be called to update the plot of the graph
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def update_plot_data(self):

        self.x = self.x[1:]  
        self.x.append(self.x[-1] + 1)  

        self.y = self.y[1:]  

        new_value = randint(0,10) #place-holder value, it should be the updated value for the y axis whene new data comes
        self.y.append(new_value)  

        self.data_line.setData(self.x, self.y).


def create_plot():
    app = QtWidgets.QApplication(sys.argv)
    plt = MainWindow()
    plt.show()
    sys.exit(app.exec_())


print("[STARTING] server is starting...")
start()
