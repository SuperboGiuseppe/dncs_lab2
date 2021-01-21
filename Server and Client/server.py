import socket 
import threading

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


print("[STARTING] server is starting...")
start()