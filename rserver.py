import rpyc
from multiprocessing import Pool, Process, Queue, Manager
import math
from multiprocessing import Process


class RServers:

    def __init__(self, servers):

        self.servers = servers
        self.connections = []
        self.dead_servers = []
        for addr in self.servers:
            host, port = addr

            try:
                connect = rpyc.classic.connect(host, port)
                self.connections.append(connect)
            except ConnectionRefusedError:
                self.dead_servers.append((host, port))

        if (self.connections == [] or len(self.dead_servers) == len(self.connections)):
            raise Exception("There are no active servers")

    def addCode(self, code):
        for conn in self.connections:
            conn.execute(code)

    def mapReduce(self, func, values):

        connections_count = len(self.connections)
        values_count = len(values)
        values_size = math.ceil(values_count / connections_count)

        values_chanks = []
        for i in range(0, values_count, values_size):
            values_chanks.append(values[i:i + values_size])

        results = []
        process_list = []

        manager = Manager()
        results = manager.list()

        for i, conn in enumerate(self.connections):
            def f(conn, func, x, results):
                code = '{}({})'.format(func, x)
                results.append(conn.eval(code))

            p = Process(target=f, args=(conn, func, values_chanks[i], results))
            process_list.append(p)
            p.start()

        for item in process_list:
            p.join()

        return list(results)