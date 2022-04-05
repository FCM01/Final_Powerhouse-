from ast import arg
from pickle import FALSE
import socket
import threading
import time
from tracemalloc import start 

HEADER =64 
PORT = 5050
SERVER  = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    try:
        print(f"[New Connection] {addr} connected")

        connected = True
        while connected :
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length :
                msg_length = int(msg_length)
                msg  = conn.recv(msg_length).decode(FORMAT)
                if  msg  == DISCONNECT_MESSAGE :
                    connected  = FALSE
                print(f"[{addr}] {msg}" )
                conn.send("Recieved".encode (FORMAT))
        conn.close()
            
    except Exception as e :
        print("ERROR",e)
def start():
    server.listen()
    print(f"[Listening] the server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[Acctive Connections]= {threading.active_count()-1}")


print("[Starting]sever is starting...")
start()
