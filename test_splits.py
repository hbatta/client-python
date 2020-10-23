from hapiclient import hapi
from hapiclient.test.readcompare import equal


def compare(data1, data2, meta1, meta2, title1, title2):
    print('%s %5.2f ms %8.4f s' % (title1, 1000. * meta1['x_readTime'], meta1['x_downloadTime']))
    print('%s %5.2f ms %8.4f s' % (title2, 1000. * meta2['x_readTime'], meta2['x_downloadTime']))
    assert equal(data1, data2)


def test_year():
    server = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset = 'dataset1'
    parameters = 'scalar'
    start = '1971-06-02T01:50:00'
    stop = '1974-08-03T06:50:00'

    opts = {
        'usecache': True,
        'parallel': True,
        'n_chunks': 5,
        'cachedir': 'tmp/hapi-data/year',
        'cache': True,
        'dt_chunk': 'P1Y',
    }

    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {
        'usecache': False,
        'parallel': False,
        'cachedir': 'tmp/hapi-data/hour',
        'cache': False,
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=P1Y, n_chunks=None',
        'usecache=False, dt_chunk=None, n_chunks=None'
    )


def test_month():
    server = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset = 'dataset1'
    parameters = 'scalar'
    start = '1971-06-02T01:50:00'
    stop = '1974-08-03T06:50:00'

    opts = {
        'usecache': True,
        'parallel': True,
        'n_chunks': 5,
        'cachedir': 'tmp/hapi-data/month',
        'cache': True,
        'dt_chunk': 'P1M',
    }

    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {
        'usecache': False,
        'parallel': False,
        'cachedir': 'tmp/hapi-data/hour',
        'cache': False,
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=P1M, n_chunks=None',
        'usecache=False, dt_chunk=None, n_chunks=None'
    )


def test_day():
    server = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset = 'dataset1'
    parameters = 'scalar'
    start = '1971-06-02T01:50:00.000'
    stop = '1971-06-04T06:50:00.000'

    opts = {
        'usecache': True,
        'parallel': True,
        'cachedir': 'tmp/hapi-data/day',
        'cache': True,
        'dt_chunk': 'P1D',
    }

    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {
        'usecache': False,
        'parallel': False,
        'cachedir': 'tmp/hapi-data/hour',
        'cache': False,
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=P1D, n_chunks=None',
        'usecache=False, dt_chunk=None, n_chunks=None'
    )


def test_hour():
    server = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset = 'dataset1'
    parameters = 'scalar'
    start = '1971-06-30T01:50:00.000'
    stop = '1971-07-01T06:50:00.000'

    opts = {
        'usecache': True,
        'parallel': False,
        'cachedir': 'tmp/hapi-data/hour',
        'cache': False,
        'dt_chunk': 'PT1H',
    }

    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {
        'usecache': False,
        'parallel': False,
        'cachedir': 'tmp/hapi-data/hour',
        'cache': False,
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=False, dt_chunk=PT1H, n_chunks=None',
        'usecache=False, dt_chunk=None, n_chunks=None'
    )


def test_half():
    server = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset = 'dataset1'
    parameters = 'scalar'
    start = '1971-07-01T06:21:00'
    stop = '1971-07-01T06:50:00'

    opts = {
        'usecache': True,
        'parallel': False,
        'cachedir': 'tmp/hapi-data/hour',
        'cache': True,
        'dt_chunk': 'infer'
    }

    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    opts = {
        'usecache': True,
        'parallel': False,
        'cachedir': 'tmp/hapi-data/hour',
        'cache': True,
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )


def test_datetypes():
    server = 'http://hapi-server.org/servers-dev/SSCWeb/hapi'
    dataset = 'active'
    parameters = 'X_TOD'
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'

    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': None,
    }

    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    # 1
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    # 2
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    # 3
    start = '1989-272T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    # 4
    start = '1989-272T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    # ==================================================================================================================

    server = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset = 'dataset1'
    parameters = 'scalar'
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'

    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': None,
    }

    data1, meta1 = hapi(server, dataset, parameters, start, stop, **opts)

    # 1
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    # 2
    start = '1989-09-29T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    # 3
    start = '1989-272T00:00:00.000Z'
    stop = '1989-10-01T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    # 4
    start = '1989-272T00:00:00.000Z'
    stop = '1989-274T00:00:00.000Z'
    opts = {
        'logging': False,
        'usecache': True,
        'cache': True,
        'n_chunks': None,
        'dt_chunk': 'infer',
    }

    data2, meta2 = hapi(server, dataset, parameters, start, stop, **opts)

    compare(
        data1, data2, meta1, meta2,
        'usecache=True, dt_chunk=infer, n_chunks=None',
        'usecache=True, dt_chunk=None, n_chunks=None'
    )

    print()


if __name__ == "__main__":
    # test_half()
    # test_hour()
    # test_day()
    # test_month()
    # test_year()
    test_datetypes()
