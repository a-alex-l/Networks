import os
import socket
from concurrent.futures import ThreadPoolExecutor
from sys import argv
from urllib.parse import urlparse


def search_file(conn, _):
    print('Start.')
    data = conn.recv(2**10)

    if not data:
        conn.send('HTTP/1.1 500 Bad Request\r\n'.encode())
        conn.close()
        print('End. 500')
        return

    url = data.decode().split('\r\n')[0][:-9]
    query = urlparse(url).query
    query_components = dict(qc.split("=") for qc in query.split("&"))
    file_name = query_components.get('file', None)

    if file_name is not None and os.path.exists(file_name) and os.path.isfile(file_name):
        print(file_name, 'found!')
        with open(file_name, 'br') as file:
            file_content = file.read()
            headers = f'HTTP/1.1 200 OK\r\nContent-Length: {len(file_content)}\r\nConnection: close'
            print(headers.encode('utf8') + file_content)
            conn.send(headers.encode('utf8') + file_content)
        print('End. 200')
    else:
        conn.send('HTTP/1.1 404 Not Found\r\n'.encode())
        print('End. 404')
    conn.close()


def main():
    host = socket.gethostbyname(socket.gethostname())
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.bind((host, 0))
    print(server.getsockname()[0], server.getsockname()[1])
    server.listen(1)
    concurrency_level = 8  # Sorry for snake case. Pycharm likes this one more.
    if len(argv) > 1 and argv[1] is not None:
        concurrency_level = int(argv[1])
    with ThreadPoolExecutor(max_workers=concurrency_level) as pool:
        while 1:
            conn, addr = server.accept()
            pool.submit(search_file, conn, addr)


if __name__ == '__main__':
    main()
