from hapiclient import hapi
from hapiclient.test.readcompare import equal


def compare(data1, data2, meta1, meta2, title1, title2):
    print('%s %5.2f ms %8.4f s' % (title1, 1000. * meta1['x_readTime'], meta1['x_downloadTime']))
    print('%s %5.2f ms %8.4f s' % (title2, 1000. * meta2['x_readTime'], meta2['x_downloadTime']))
    assert equal(data1, data2)


server = 'http://hapi-server.org/servers/TestData2.0/hapi'
dataset = 'dataset1'
parameters = 'scalar'


# test_year
if False:
    start = '1971-06-02T01:50:00'
    stop = '1974-08-03T06:50:00'

    opts = {'usecache': True, 'parallel': True, 'cache': True, 'dt_chunk': 'P1Y'}
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {'usecache': False, 'parallel': False, 'cache': False}
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(data1, data2, meta1, meta2, 'split request dt_chunk=P1Y', 'request')

# test_month
if False:
    start = '1971-06-02T01:50:00'
    stop = '1974-08-03T06:50:00'

    opts = {'usecache': True, 'parallel': True, 'cache': True, 'dt_chunk': 'P1M'}
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {'usecache': False, 'parallel': False, 'cache': False}
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(data1, data2, meta1, meta2, 'split request dt_chunk=P1M', 'request')


# test_day
if False:
    start = '1971-06-02T01:50:00.000'
    stop = '1971-06-04T06:50:00.000'

    opts = {'usecache': True, 'parallel': True, 'cache': True, 'dt_chunk': 'P1D'}
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {'usecache': False, 'parallel': False, 'cache': False}
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(data1, data2, meta1, meta2, 'split request dt_chunk=P1D', 'request')


# test_hour
if True:
    start = '1971-06-30T01:50:00.000'
    stop = '1971-07-01T06:50:00.000'

    opts = {'usecache': True, 'parallel': False, 'cache': False, 'dt_chunk': 'PT1H'}
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {'usecache': False, 'parallel': False, 'cache': False}
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(data1, data2, meta1, meta2, 'split request dt_chunk=PT1H', 'request')


# test_half
if True:
    start = '1971-07-01T06:21:00'
    stop = '1971-07-01T06:50:00'
    opts = {'usecache': True, 'parallel': False, 'cache': True, 'dt_chunk': 'infer'}
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {'usecache': True, 'parallel': False, 'cache': True}
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(data1, data2, meta1, meta2, 'split request time range is < 1/2 of chunk size', 'request')

# test_datatypes
if True:
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    opts = {'usecache': True, 'cache': True, 'n_chunks': None, 'dt_chunk': None}
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)
    opts = {'usecache': True, 'cache': True, 'n_chunks': None, 'dt_chunk': 'infer'}

    # 1
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ymd stop:ymd, data:ymd')

    # 2
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ymd stop:ydoy, data:ymd')

    # 3
    start = '1989-272T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ydoy stop:ymd, data:ymd')

    # 4
    start = '1989-272T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ydoy stop:ydoy, data:ymd')

    # ==================================================================================================================
    server = 'http://hapi-server.org/servers-dev/SSCWeb/hapi'
    dataset = 'active'
    parameters = 'X_TOD'
    # ==================================================================================================================

    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    opts = {'usecache': True, 'cache': True, 'n_chunks': None, 'dt_chunk': None}
    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)
    opts = {'usecache': True, 'cache': True, 'n_chunks': None, 'dt_chunk': 'infer'}

    # 1
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ymd stop:ymd, data:ydoy')

    # 2
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ymd stop:ydoy, data:ydoy')

    # 3
    start = '1989-272T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ydoy stop:ymd, data:ydoy')

    # 4
    start = '1989-272T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)
    compare(data1, data2, meta1, meta2, 'request', 'split request, start:ydoy stop:ydoy, data:ydoy')
