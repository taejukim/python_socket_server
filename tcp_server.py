import socket 
from datetime import datetime

HOST = '127.0.0.1'
PORT = 9999

def print_log(logs):
    now = datetime.now().isoformat()
    print(f'[{now}] {logs}')

def server_log(data, client_ip, client_port): 
    try:
        if not data:
            print_log(f'Disconnected [{client_ip}:{client_port}]')
            return False
        data = data.decode()
        print_log(f'Received [{client_ip}:{client_port}] {data}')
        return data
    except ConnectionResetError as e:
        print_log(e)
        print_log(f'Disconnected [{client_ip}:{client_port}]')
        return False

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT)) 
    sock.listen(1)
    buffer_size = 1024
    print_log(f'TCP Server start Now! [{HOST}:{PORT}], Buffer size : {buffer_size}')

    conn, client = sock.accept()
    client_ip, client_port = client[0], client[1]
    print_log(f'Connected [{client_ip}:{client_port}]')

    while True: 
        data = conn.recv(buffer_size) 
        if not server_log(data, client_ip, client_port):
            break
        