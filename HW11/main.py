#!/usr/bin/python

import sys
from time import sleep
from icmplib.sockets import ICMPv4Socket
from icmplib.models import ICMPRequest
from icmplib.exceptions import TimeExceeded
from icmplib.utils import *
from socket import gethostbyaddr


def traceroute(address, count=5, interval=0.1, timeout=1, first_hop=1, max_hops=30):
    id = unique_identifier()
    ttl = first_hop - 1
    host_reached = False
    with ICMPv4Socket(None) as current_socket:
        while ttl <= max_hops:
            ttl += 1
            print(ttl, end=') ')
            dst = None
            for sequence in range(count):
                request = ICMPRequest(destination=address, id=id, sequence=sequence, ttl=ttl)
                try:
                    current_socket.send(request)
                    try:
                        reply = current_socket.receive(request, timeout)
                        print("{0:0.5f}s".format(reply.time - request.time), end='  ')
                        dst = reply.source
                        try:
                            reply.raise_for_status()
                            max_hops = 0
                        except:
                            pass
                    except:
                        print('*.*****s', end='  ')
                except TimeExceeded:
                    sleep(interval)
            if dst:
                print('  Destination =', dst, end='   ')
            else:
                print('  Destination = ************', end='   ')
            try:
                print('Host =', gethostbyaddr(dst)[0])
            except:
                print('Host = ***')


traceroute(sys.argv[1])
