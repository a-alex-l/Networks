from socket import *
from time import time
from datetime import datetime
from server import CONST_SERVER_PORT


def main():
    client = socket(AF_INET, SOCK_DGRAM)
    client.connect(('', CONST_SERVER_PORT))
    client.settimeout(1)

    for i in range(0, 10):
        content = f'\nPing {i + 1} {datetime.now().time()}'
        print(content)
        start = time()
        client.send(content.encode())
        try:
            _ = client.recv(2**10)
            print('RTT={0:0.3f} ms'.format(1000 * (time() - start)))
        except:
            print('Request timed out')


if __name__ == '__main__':
    main()
