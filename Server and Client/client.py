import socket

import psutil #this import was added by luca
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = "192.168.53.133"
SERVER = "127.0.1.1" #Luca: "i added this line to make it work on my pc, commenting the one above"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

#this function return the percentage of RAM in use by the machine
def Ram_data_perc():
    return (int(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))

#this function return the percentage of CPU in use by the machine
def Cpu_data_perc():
    return (int(psutil.cpu_percent()))  


try:
    while(1):
        #send(str(Ram_data_perc()))
        send(str(Cpu_data_perc()))
        time.sleep(1)
except:
    send(DISCONNECT_MESSAGE)

#send(str(Ram_data_perc()))
#input()
#send(str(Cpu_data_perc()))
#input()
#send("Hello uzair!")

