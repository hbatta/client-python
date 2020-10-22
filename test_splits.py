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
    server     = 'http://hapi-server.org/servers-dev/SSCWeb/hapi';
    dataset    = 'active';
    parameters = 'X_TOD'; 
    start      = '1989-09-29T00:00:00.000Z';
    stop       = '1989-10-01T00:00:00.000Z';
    opts = {
        'logging': False,
        'usecache': False,
        'parallel': False,
        'cache': True,
        'usecache': False,
        'n_chunks': 1,
        'dt_chunk': 'infer',
    }

#if n_chunks is not None and dt_chunk is not None:
#    error('one may be not None')
    
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {
        'logging': False,
        'usecache': False,
        'parallel': False,
        'cache': True,
        'usecache': False,
        'n_chunks': 0
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2,
            'usecache=False, parallel=False, dt_chunk=infer',
            'usecache=False, parallel=False, n_chunks=0')

    server     = 'http://hapi-server.org/servers-dev/SSCWeb/hapi';
    dataset    = 'active';
    parameters = 'X_TOD'; 
    start      = '1989-272T00:00:00.000Z';
    stop       = '1989-274T00:00:00.000Z';
    opts = {
        'logging': False,
        'usecache': False,
        'parallel': False,
        'cache': True,
        'usecache': False,
        'n_chunks': 1,
        'dt_chunk': 'infer',
    }

    data3, meta3 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data3, meta1, meta3,
            'usecache=False, parallel=False, dt_chunk=infer',
            'usecache=False, parallel=False, n_chunks=0')

print("---")

server = 'http://hapi-server.org/servers/TestData2.0/hapi'
dataset = 'dataset1'
parameters = 'scalar'

if False:
	start = '1970-001T00:00:00'
	stop  = '1970-001T12:00:00'

	opts = {
		'logging': False,
	    'usecache': False,
	    'parallel': False,
	    'cache': True,
	    'usecache': False,
	    'n_chunks': 1,
	    'dt_chunk': 'infer',
	}

	data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

print("---")





if False:
	start = '1971-06-30T01:50:00'
	stop = '1971-07-01T06:50:00'

	print("---")
	opts = {
	    'usecache': False,
	    'parallel': False,
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
