import socket

# 創建一個IPv4的TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 連接伺服器的IP和埠號
server_address = ('localhost', 10000)
client_socket.connect(server_address)

client_socket.send("shoot".encode('utf-8'))