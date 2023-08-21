import unittest
import socket
import redis

class TestCalculator(unittest.TestCase):
    def test_socket_send(self):
        red_server = redis.Redis(host='localhost', port=6379)

        red_server.set('is_shoot_time', "False")

        server_ip = '127.0.0.1'
        server_port = 2222

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((server_ip, server_port))

        message = "start shoot"
        client_socket.send(message.encode('utf-8'))

        client_socket.close()

        self.assertEqual(red_server.get('is_shoot_time').decode(), "True")

if __name__ == '__main__':
    unittest.main()