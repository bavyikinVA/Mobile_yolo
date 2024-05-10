import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.12", 7000))
with open('image_client.jpg', 'rb') as file:  # Open the file in binary mode
    data = file.read(2048)
    while data:
        client.send(data)
        data = file.read(2048)
client.close()
