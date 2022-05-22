import sys
import base64
import socket
import ssl


def send_message(email_to, email_from, password, content_type, message):
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Created')
    try:
        new_socket = ssl.wrap_socket(new_socket, ssl_version=ssl.PROTOCOL_SSLv23)
        new_socket.connect(('smtp.gmail.com', 465))
        print('Connected')
        new_socket.send(f'EHLO {email_from.split("@")[0]}\r\n'.encode())
        print('Hello:', new_socket.recv(1024).decode())
        new_socket.send('AUTH PLAIN '.encode() +
                        base64.b64encode(f'\x00{email_from}\x00{password}'.encode()) +
                        '\r\n'.encode())
        print('Login:', new_socket.recv(1024).decode())
        new_socket.send(f'MAIL FROM:<{email_from}>\r\n'.encode())
        print('From:', new_socket.recv(1024))
        new_socket.send(f'RCPT TO:<{email_to}>\r\n'.encode())
        print('To:', new_socket.recv(1024).decode())
        new_socket.send('DATA\r\n'.encode())
        print('Data sending:', new_socket.recv(1024).decode())
        new_socket.send(
            f'From: {email_from}\r\n'
            f'To: {email_to}\r\n'
            f'Subject: From bot.\r\n'
            f'Content-Type: {content_type}\r\n'
            f'Content-Transfer-Encoding: base64\r\n'.encode())
        print('Headers sent:', new_socket.recv(1024).decode())
        new_socket.send(base64.b64encode(message) + '\r\n'.encode())
        new_socket.send('.\r\n'.encode())
        print('Message sent:', new_socket.recv(1024).decode())
        new_socket.send('QUIT\r\n'.encode())
        print('Everything sent:', new_socket.recv(1024).decode())
    finally:
        new_socket.close()


def get_type_and_message(message_file_name):
    file_type = message_file_name.split('.')[-1]
    with open(message_file_name, 'rb') as file:
        if file_type == 'html':
            return 'text/html', file.read()
        elif file_type == 'txt':
            return 'text/plain', file.read()
        else:
            return f'image/{file_type}; name={message_file_name}', file.read()


def main():
    email_to = sys.argv[1]
    message_file_name = sys.argv[2]
    content_type, message = get_type_and_message(message_file_name)
    email_from = 'NetworksLab5FakeAddress@gmail.com'
    password = 'NoPassword'
    print('Data mined')
    send_message(email_to, email_from, password, content_type, message)


if __name__ == '__main__':
    main()