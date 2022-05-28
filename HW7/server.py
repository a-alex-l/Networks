from socket import *
import random


CONST_SERVER_PORT = 12345


def main():
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', 12345))

    while True:
        content, client_address = server_socket.recvfrom(1024)
        if random.randint(0, 4) != 0:
            server_socket.sendto(content.decode().upper().encode(),
                                 client_address)


if __name__ == '__main__':
    main()
