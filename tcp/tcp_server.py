import socket 
from _thread import start_new_thread
from datetime import datetime

HOST = '0.0.0.0'
PORT = 10002

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

def tcp_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port)) 
    sock.listen(5)
    buffer_size = 1024
    print_log(f'TCP Server start Now! [{HOST}:{port}], Buffer size : {buffer_size}')

    conn, client = sock.accept()
    client_ip, client_port = client[0], client[1]
    print_log(f'Connected [{client_ip}:{client_port}]')

    while True: 
        data = conn.recv(buffer_size)
        if len(data) == 0:
            break
        if not data or data == 'PING'.encode():
            send_data = 'PONG'.encode()
        else:
            send_data = data
        start_new_thread(server_log, (send_data, client_ip, client_port, 'tcp'))
        conn.send(send_data)
    print_log(f'TCP Server Disconnected by {client_ip}:{client_port}')
    conn.close()
    sock.close()
    tcp_server(port) # client 에서 close 되더라도 서버 재실행

if __name__ == "__main__":
    tcp_server(PORT)
