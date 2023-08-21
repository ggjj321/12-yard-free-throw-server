import socket

# 創建一個IPv4的TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 連接伺服器的IP和埠號
server_address = ('127.0.0.1', 2222)
client_socket.connect(server_address)

client_socket.send("start shoot".encode('utf-8'))
data = client_socket.recv(1024).decode('utf-8')
print(data)