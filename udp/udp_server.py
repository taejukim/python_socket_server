import socket 
from datetime import datetime

HOST = '0.0.0.0'
PORT = 10001

def print_log(logs):
    now = datetime.now().isoformat()
    print(f'[{now}] {logs}')

def server_log(data, client_ip, client_port, protocol): 
    '''print server's log'''
    try:
        if not data:
            print_log(f'Disconnected [{client_ip}:{client_port}]')
            return
        data = data.decode()
        print_log(f'Received [{client_ip}:{client_port}/{protocol}] {data}')
    except ConnectionResetError as e:
        print_log(e)
        print_log(f'Disconnected [{client_ip}:{client_port}]')
        return

def udp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, port))

    buffer_size = 1024
    print_log(f'UDP Server start Now! [{HOST}:{port}], Buffer size : {buffer_size}')

    # while True:
    data, client = server_socket.recvfrom(buffer_size) 
    client_ip, client_port = client[0], client[1]
    server_log(data, client_ip, client_port, 'udp')
    if not data or data == 'PING'.encode():
        send_data = 'PONG'.encode()
    else:
        send_data = data
    server_socket.sendto(send_data, client)

if __name__ == "__main__":
    udp_server(PORT)
