from random import randint
import json


class Router:
    def __init__(self, ip, neighbors):
        self.ip = ip
        self.neighbors = neighbors
        self.distances = {router: (1, router) for router in neighbors}

    def get_distance(self, ip):
        if ip in self.distances:
            return self.distances[ip][0]
        return None

    def update_distances(self, ip, new_value, next_hop):
        if new_value is not None and (ip not in self.distances or new_value + 1 < self.distances[ip][0]):
            self.distances[ip] = (new_value + 1, next_hop)
            return True
        return False

    def show_statistics(self):
        print(f'{"[Source IP]":15} {"[Destination IP]":20} {"[Next Hop]":15} {"Metric":15}')
        for dest_router in self.distances:
            print(f'{self.ip:15} {dest_router:20} {self.distances[dest_router][1]:15} '
                  f'{str(self.distances[dest_router][0]):15}')


class Network:
    def __init__(self, routers):
        self.routers = routers

    def show_rip(self):
        step = 0
        flag = True
        while flag:
            step += 1
            flag = False
            for source_router in self.routers:
                for destination_router in self.routers:
                    if source_router.ip == destination_router.ip:
                        continue
                    for next_ip in source_router.neighbors:
                        if (source_router.update_distances(
                                destination_router.ip,
                                destination_router.get_distance(next_ip),
                                next_ip)):
                            flag = True
                print(f'Simulation step {step} of router {source_router.ip}:')
                source_router.show_statistics()
                print()
            print()
            for router in self.routers:
                print(f'Final state of router {router.ip}:')
                router.show_statistics()
                print()
            print()


def get_ips(n=4):
    router_ips = set()
    while len(router_ips) < n:
        router_ips.add('{}.{}.{}.{}'.format(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)))
    return list(router_ips)


def get_net(config, routers):
    network = []
    for i in range(len(config)):
        network.append(Router(routers[i], [routers[j] for j in config[i]]))
    return network


def main():
    config = json.load(open('config.json'))
    network = get_net(config, get_ips(len(config)))
    Network(network).show_rip()


if __name__ == '__main__':
    main()
