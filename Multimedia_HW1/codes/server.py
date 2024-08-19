import socket
import cv2

server_ip = 'localhost'
server_port_image = 7000
server_port_voice = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port_image))
server_socket.listen()
print("Server: Server is Running")


def read_data(cs: socket, filename):
    data_list = b''
    while data:=cs.recv(1024):
        data_list += data
    with open(filename, "wb") as file:
        file.write(data_list)
    print(len(data_list))
    
client_socket, client_info = server_socket.accept()
read_data(client_socket, "receive_image.png")
print(f"Server: Accepted new Connection on {client_info}")
server_socket.close()

#receive voice
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port_voice))
server_socket.listen()
print("Server: Server is Running")

client_socket, client_info = server_socket.accept()
read_data(client_socket, "receive_voice.wav")
print(f"Server: Accepted new Connection on {client_info}")
server_socket.close()

