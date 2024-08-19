import socket

server_ip = 'localhost'
server_port_image = 7000
server_port_voice = 5000

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((server_ip, server_port_image))

with open("image.png", 'rb') as file:
    data1 = file.read()
print(cs.send(data1))
cs.close()

# send voice
cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((server_ip, server_port_voice))

with open("voice.wav", 'rb') as file:
    data2 = file.read()

print(cs.send(data2))
cs.close()
