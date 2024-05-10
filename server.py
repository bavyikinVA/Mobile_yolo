import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.0.12", 7000))
server.listen()

client_socket, client_address = server.accept()

with open('image.jpg', mode='wb') as file:  # Открываем файл в двоичном режиме
    while True:
        data = client_socket.recv(2048)
        if not data:
            break
        file.write(data)

client_socket.close()
