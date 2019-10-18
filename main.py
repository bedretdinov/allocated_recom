from rserver import RServers



servers = RServers([
    ("0.0.0.0", 6000),
    ("0.0.0.0", 6001),
])

servers.addCode('''
import numpy as np

def datafiles(x):
    x = np.array(x)
    return x.std()

''')






results = servers.mapReduce('datafiles',list(range(1000000)))

print(results)