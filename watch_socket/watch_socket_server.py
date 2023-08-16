import socket
import redis

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
server_socket.bind(server_address)

server_socket.listen(1)

# 接受客戶端連接
client_socket, client_address = server_socket.accept()
red_server = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 接收和傳送資料
while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break
    red_server.set('is_shoot_time', True)


client_socket.close()
server_socket.close()
