from socket import *
from time import time
from server import CONST_SERVER_PORT


def main():
    client = socket(AF_INET, SOCK_DGRAM)
    client.connect(('', CONST_SERVER_PORT))
    client.settimeout(1)
    rtts = []

    steps = 0
    while True:
        steps += 1
        content = "Hey it's a ping bro!"
        start = time()
        client.send(content.encode())
        try:
            _ = client.recv(2**10)
            rtts.append(1000 * (time() - start))
            print(f'Ping {steps}', end='   ')
            print('cur_RTT={0:0.3f} ms'.format(rtts[-1]), end='   ')
            print('min_RTT={0:0.3f} ms'.format(min(rtts)), end='   ')
            print('avr_RTT={0:0.3f} ms'.format(sum(rtts) / len(rtts)), end='   ')
            print('max_RTT={0:0.3f} ms'.format(max(rtts)), end='   ')
            print('loss_percent={0:0.4f}'.format((1 - len(rtts) / steps) * 100))
        except:
            pass


if __name__ == '__main__':
    main()
