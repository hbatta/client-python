from hapiclient import hapi

server = 'http://hapi-server.org/servers/TestData2.0/hapi'
dataset = 'dataset1'
parameters = 'vector'
start = '1971-01-01T00:00:00'
stop = '1971-01-01T00:00:02'

from hapiclient.test.readcompare import equal

def compare(data1, data2, meta1, meta2, title1, title2):
    print('%s %5.2f ms %8.4f s' % (title1, 1000.*meta1['x_readTime'], meta1['x_downloadTime']))
    print('%s %5.2f ms %8.4f s' % (title2, 1000.*meta2['x_readTime'], meta2['x_downloadTime']))
    assert equal(data1, data2)

opts = {'usecache': False, 'parallel': False, 'n_splits': 0, 'logging': True}
data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)
#print(data1)

print("---")

opts = {'usecache': False, 'parallel': False, 'n_splits': 1, 'logging': True}
data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

print("---")

compare(data1, data2, meta1, meta2,
        'usecache=False, parallel=False, n_splits=0',
        'usecache=False, parallel=False, n_splits=1')

opts = {'usecache': False, 'parallel': False, 'n_splits': 2, 'logging': True}
data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

print("---")

compare(data1, data2, meta1, meta2,
        'usecache=False, parallel=False, n_splits=0',
        'usecache=False, parallel=False, n_splits=5')
