import argparse 
from multiprocessing import Process
from _thread import start_new_thread
import socket 
from datetime import datetime

HOST = '0.0.0.0'

def print_log(logs):
    '''print time stamp'''
    now = datetime.now().isoformat()
    print(f'[{now}] {logs}')

def server_log(data, client_ip, client_port): 
    '''print server's log'''
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

def tcp_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port)) 
    sock.listen(5)
    buffer_size = 1024
    print_log(f'TCP Server start Now! [{HOST}:{port}], \
    Buffer size : {buffer_size}')

    conn, client = sock.accept()
    client_ip, client_port = client[0], client[1]
    print_log(f'Connected [{client_ip}:{client_port}]')

    while True: 
        data = conn.recv(buffer_size)
        if len(data) == 0:
            break
        start_new_thread(server_log, (data, client_ip, client_port))
        conn.send(data)
    print_log(f'TCP Server Disconnected by {client_ip}:{client_port}')
    conn.close()
    sock.close()
    tcp_server(port) # client 에서 close 되더라도 서버 재실행

def udp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, port)) 
    Buffer_size = 1024
    print_log(f'UDP Server start Now! [{HOST}:{port}], \
    Buffer size : {Buffer_size}')

    first_loop = True
    while True:
        data, client = server_socket.recvfrom(Buffer_size) 
        server_socket.sendto(data, client)
        client_ip, client_port = client[0], client[1]
        if first_loop:
            print_log(f'Connected [{client_ip}:{client_port}]')
            first_loop = False
        start_new_thread(server_log, (data, client_ip, client_port))

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='TCP, UDP 서버 실행')
        parser.add_argument('tcp', help='tcp port', default=10000)
        parser.add_argument('udp', help='udp port', default=10001)
        args = parser.parse_args()
        tcp = args.tcp
        udp = args.udp
    except Exception as e:
        print(e)
        tcp = 10000
        udp = 10001

    if tcp == udp:
        print_log('TCP, UDP서버의 Port가 같습니다. 다시 확인해주세요.\
            \n TCP : {}, UDP : {}'.format(tcp, udp))
    else:
        tcp_server_process = Process(target=tcp_server, args=(int(tcp), ))
        udp_server_process = Process(target=udp_server, args=(int(udp), ))

        tcp_server_process.start()
        udp_server_process.start()

        tcp_server_process.join()
        udp_server_process.join()
