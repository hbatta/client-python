from hapiclient import hapi

server = 'http://hapi-server.org/servers/TestData2.0/hapi'
dataset = 'dataset1'
parameters = 'scalar'

from hapiclient.test.readcompare import equal

def compare(data1, data2, meta1, meta2, title1, title2):
    print('%s %5.2f ms %8.4f s' % (title1, 1000.*meta1['x_readTime'], meta1['x_downloadTime']))
    print('%s %5.2f ms %8.4f s' % (title2, 1000.*meta2['x_readTime'], meta2['x_downloadTime']))
    assert equal(data1, data2)

if True:
	start = '1971-06-30T01:50:00'
	stop = '1971-07-01T06:50:00'

	print("---")
	opts = {
	    'usecache': True,
	    'parallel': True,
	    'n_chunks': 5,
	    'cachedir': 'tmp/hapi-data/hour',
	    'cache': True,
	    'dt_chunk': 'PT1H',
	}

	# n_chunks = 30
	data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

print("---")


if False:
	start = '1971-01-01T00:00:00'
	stop = '1971-01-01T00:00:02'

	print("---")
	opts = {
		'usecache': False,
		'parallel': False,
		'n_chunks': 0,
		'logging': True
	}
	data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)


	opts = {
		'usecache': False,
		'parallel': False,
		'n_chunks': 1,
		'logging': True
	}
	data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

	compare(data1, data2, meta1, meta2,
	        'usecache=False, parallel=False, n_chunks=0',
	        'usecache=False, parallel=False, n_chunks=1')
	print("---")


	print("---")
	opts = {
		'usecache': False,
		'parallel': False,
		'n_chunks': 2,
		'logging': True
	}
	data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

	compare(data1, data2, meta1, meta2,
	        'usecache=False, parallel=False, n_chunks=0',
	        'usecache=False, parallel=False, n_chunks=5')
	print("---")
