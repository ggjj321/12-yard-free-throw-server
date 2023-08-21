import socket
import redis
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("0.0.0.0", 2222)
server_socket.bind(server_address)

server_socket.listen(1)

# 接受客戶端連接

red_server = redis.Redis(host='redis', port=6379, decode_responses=True)

print("socket start")

def handle_watch_message(watch_socket):
    while True:
        data = watch_socket.recv(1024).decode('utf-8')
        print(data)
        try:
            if data == "start shoot":
                red_server.set('is_shoot_time', "True")
                watch_socket.send("success".encode('utf-8'))
                
        except socket.error:
            watch_socket.close()

while True:
    try:
        watch_socket, watch_address = server_socket.accept()
        receive_socket_thread = threading.Thread(target=handle_watch_message, args=(watch_socket,), daemon=True)
        receive_socket_thread.start()
    except socket.error:
        server_socket.close()
server_socket.close()