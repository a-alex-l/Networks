import socket
from sys import argv


def request(h, p, f):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((h, p))
    client.send(f'GET /?file={f} HTTP/1.1\r\nHost: {h}:{p}\r\n'.encode())
    data = client.recv(2**23)
    if not data:
        return
    client.close()
    return data


def main():
    if len(argv) != 4:
        print('Bad args len: ', len(argv))
    else:
        host, port, file = argv[1:]
        response = request(host, int(port), file)
        print(response)


if __name__ == '__main__':
    main()
