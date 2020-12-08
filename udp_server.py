import socket 
from _thread import start_new_thread
from datetime import datetime

def print_log(logs):
    now = datetime.now().isoformat()
    print(f'[{now}] {logs}')

def server_log(data, client_ip, client_port): 
    try:
        if not data:
            print_log(f'Disconnected [{client_ip}:{client_port}]')
            return
        data = data.decode()
        print_log(f'Received [{client_ip}:{client_port}] {data}')
    except ConnectionResetError as e:
        print_log(e)
        print_log(f'Disconnected [{client_ip}:{client_port}]')
        return

HOST = '0.0.0.0'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
Buffer_size = 1024
print_log(f'UDP Server start Now! [{HOST}:{PORT}], Buffer size : {Buffer_size}')

first_loop = True
while True:
    data, client = server_socket.recvfrom(Buffer_size) 
    client_ip, client_port = client[0], client[1]
    if first_loop:
        print_log(f'Connected [{client_ip}:{client_port}]')
        first_loop = False
    start_new_thread(server_log, (data, client_ip, client_port)) 
