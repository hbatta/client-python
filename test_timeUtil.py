from timeUtil import *


def test_reformat_iso_time():
    """Test of reformat_iso_time.
    """
    # print("reformat_iso_time")
    expResult = "2020-04-21T00:00Z"
    result = reformat_iso_time("2020-01-01T00:00Z", "2020-112Z")
    assert expResult == result


def test_normalize_time_string():
    """Test of normalize_time_string.
    """
    # print("normalize_time_string")
    time = "2020-09-25"
    expResult = "2020-09-25T00:00:00.000000000Z"
    result = normalize_time_string(time)
    assert expResult == result


def test_iso_time_to_array():
    """ Test of iso_time_to_array.
    """
    # print("iso_time_to_array")

    time = "2020-09-25T01:02Z"
    expResult = [2020, 9, 25, 1, 2, 0, 0]
    result = iso_time_to_array(time)
    assert expResult == result

    time = "2020-033"
    expResult = [2020, 2, 2, 0, 0, 0, 0]
    result = iso_time_to_array(time)
    assert expResult == result

    time = "2020-02-02"
    expResult = [2020, 2, 2, 0, 0, 0, 0]
    result = iso_time_to_array(time)
    assert expResult == result

    time = "2020-02-02Z"
    expResult = [2020, 2, 2, 0, 0, 0, 0]
    result = iso_time_to_array(time)
    assert expResult == result

    time = "2020-02-02T01:02:03.0406"
    expResult = [2020, 2, 2, 1, 2, 3, 40600000]
    result = iso_time_to_array(time)
    assert expResult == result


def test_array_to_iso_time():
    """Test of array_to_iso_time.
    """
    # print("array_to_iso_time")

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy'
    expResult = "1990"
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-mm'
    expResult = "1990-04"
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-mm-dd'
    expResult = "1990-04-24"
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-mm-ddThh'
    expResult = "1990-04-24T00"
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-mm-ddThh:mm'
    expResult = "1990-04-24T00:00"
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-mm-ddThh:mm:ss'
    expResult = "1990-04-24T00:00:00"
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    for i in range(1, 10):
        dt_format = 'yyyy-mm-ddThh:mm:ss.{}'.format(i)
        expResult = "1990-04-24T00:00:00.{:0{width}}".format(0, width=i)
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-doy'
    expResult = '1990-114'
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-doyThh'
    expResult = '1990-114T00'
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-doyThh:mm'
    expResult = '1990-114T00:00'
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    dt_format = 'yyyy-doyThh:mm:ss'
    expResult = '1990-114T00:00:00'
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult

    dt = [1990, 4, 24, 0, 0, 0, 0]
    for i in range(1, 10):
        dt_format = 'yyyy-doyThh:mm:ss.{}'.format(i)
        expResult = '1990-114T00:00:00.{:0{width}}'.format(0, width=i)
    result = array_to_iso_time(dt, dt_format)
    assert result == expResult


def test_get_dt_format():
    """ Test of get_dt_format.
    """
    # print("get_dt_format")

    time = '1990'
    expResult = 'yyyy'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-04'
    expResult = 'yyyy-mm'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-04-24'
    expResult = 'yyyy-mm-dd'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-04-24T00'
    expResult = 'yyyy-mm-ddThh'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-04-24T00:00'
    expResult = 'yyyy-mm-ddThh:mm'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-04-24T00:00:00'
    expResult = 'yyyy-mm-ddThh:mm:ss'
    result = get_dt_format(time)
    assert result == expResult

    for i in range(1, 10):
        time = '1990-04-24T00:00:00.{:0{width}}'.format(0, width=i)
        expResult = 'yyyy-mm-ddThh:mm:ss.{}'.format(i)
        result = get_dt_format(time)
        assert result == expResult

    time = '1990-114'
    expResult = 'yyyy-doy'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-114T00'
    expResult = 'yyyy-doyThh'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-114T00:00'
    expResult = 'yyyy-doyThh:mm'
    result = get_dt_format(time)
    assert result == expResult

    time = '1990-114T00:00:00'
    expResult = 'yyyy-doyThh:mm:ss'
    result = get_dt_format(time)
    assert result == expResult

    for i in range(1, 10):
        time = '1990-114T00:00:00.{:0{width}}'.format(0, width=i)
        expResult = 'yyyy-doyThh:mm:ss.{}'.format(i)
        result = get_dt_format(time)
        assert result == expResult


def test_day_of_year():
    """Test of day_of_year.
    """
    # print("day_of_year")
    year = 2000
    month = 5
    day = 29
    expResult = 150
    result = day_of_year(year, month, day)
    assert expResult == result


def test_reformat_iso_time_alt(logging=False):

    from hapiclient.hapi import hapitime2datetime
    import random

    y_re = lambda x: re.match(r'^([12]\d{3})$', x)
    ym_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2]))$', x)
    ymd_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$', x)
    ydoy_re = lambda x: re.match(r'^([12]\d{3}-[0123]\d{2})$', x)
    padz = lambda x: x if 'Z' in x else x + 'Z'

    for _ in range(10):

        random.seed(10)

        # conversion

        # y -> ydoy
        form_to_match = '1997-318'
        given_form = '{}'.format(random.randint(1800, 2020))
        given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
        # given_form_modified = reformat_iso_time(form_to_match, given_form)

        if hapitime2datetime(padz(given_form_modified)) != hapitime2datetime(padz(given_form)):
            print("Mismatch: ", 
                given_form_modified, 
                given_form, 
                hapitime2datetime(padz(given_form_modified)), 
                hapitime2datetime(padz(given_form)))
            assert False

        assert bool(ydoy_re(given_form_modified))

        # ym -> ydoy
        form_to_match = '1997-318'
        given_form = '{}-{:02}'.format(random.randint(1800, 2020), random.randint(1, 12))
        given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
        # given_form_modified = reformat_iso_time(form_to_match, given_form)
        assert hapitime2datetime(padz(given_form_modified)) == hapitime2datetime(padz(given_form))
        assert bool(ydoy_re(given_form_modified))

        # ymd -> ydoy
        form_to_match = '1997-318'
        given_form = '{}-{:02}-{:02}'.format(random.randint(1800, 2020), random.randint(1, 12), random.randint(1, 28))
        given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
        # given_form_modified = reformat_iso_time(form_to_match, given_form)
        assert hapitime2datetime(padz(given_form_modified)) == hapitime2datetime(padz(given_form))
        assert bool(ydoy_re(given_form_modified))

        # ydoy -> y
        form_to_match = '1997'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
        # given_form_modified = reformat_iso_time(form_to_match, given_form) # fails
        assert hapitime2datetime(padz(given_form_modified)) == hapitime2datetime(padz(given_form.split('-')[0]))
        assert bool(y_re(given_form_modified))

        # ydoy -> ym
        form_to_match = '1997-11'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
        # given_form_modified = reformat_iso_time(form_to_match, given_form) # fails
        hdt = hapitime2datetime(padz(given_form))[0]
        assert hapitime2datetime(padz(given_form_modified)) == hapitime2datetime(padz('{}-{:02}'.format(hdt.year, hdt.month)))
        assert bool(ym_re(given_form_modified))

        # ydoy -> ymd
        form_to_match = '1997-11-14'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
        # given_form_modified = reformat_iso_time(form_to_match, given_form)

        hdt = hapitime2datetime(padz(given_form))[0]
        assert hapitime2datetime(padz(given_form_modified)) == hapitime2datetime(padz('{}-{:02}-{:02}'.format(hdt.year, hdt.month, hdt.day)))
        assert bool(ymd_re(given_form_modified))

    dts = [
        "1989",
        "1989-01",
        "1989-01-01",
        "1989-01-01T00",
        "1989-01-01T00:00",
        "1989-01-01T00:00:00",
        "1989-01-01T00:00:00.",
        "1989-01-01T00:00:00.0",
        "1989-01-01T00:00:00.00",
        "1989-01-01T00:00:00.000",
        "1989-01-01T00:00:00.0000",
        "1989-01-01T00:00:00.00000",
        "1989-01-01T00:00:00.000000",
        "1989-01-01T00:00:00.0000000",
        "1989-01-01T00:00:00.00000000",
        "1989-01-01T00:00:00.000000000"
    ]

    for i in range(len(dts)):
        dts.append(dts[i] + "Z")

    for i in range(len(dts)):
        if "T" in dts[i]:
            dts.append("1989-001T" + dts[i].split("T")[1])

    # truncating
    for i in range(len(dts)):
        form_to_match = dts[i]
        for j in range(i + 1, len(dts)):
            given_form = dts[j]
            given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
            # given_form_modified = reformat_iso_time(form_to_match, given_form)
            assert hapitime2datetime(padz(given_form_modified)) == hapitime2datetime(padz(form_to_match))
            assert given_form_modified == form_to_match

    # padding
    dts = list(reversed(dts))
    for i in range(len(dts)):
        form_to_match = dts[i]
        for j in range(i + 1, len(dts)):
            given_form = dts[j]
            given_form_modified = reformat_iso_time_alt(form_to_match, given_form)
            # given_form_modified = reformat_iso_time(form_to_match, given_form)
            assert hapitime2datetime(padz(given_form_modified)) == hapitime2datetime(padz(form_to_match))
            assert given_form_modified == form_to_match


if __name__ == '__main__':

    '''
    # %f - Microsecond as a decimal number, zero-padded on the left.
    # datetime objects don't support anything more fine than microseconds. As pointed out by Mike Pennington in
    # the comments, this is likely because computer hardware clocks aren't nearly that precise

    # code snippet 1
    from hapiclient.hapi import hapitime2datetime
    padz = lambda x: x if 'Z' in x else x + 'Z'
    time = '1989-001T00:00:00.000000000'
    _ = hapitime2datetime(padz(time))

    # code snippet 2
    import pytz
    tzinfo = pytz.UTC
    t = ['1989-001T00:00:00.000000000Z']
    fmt = '%Y-%jT%H:%M:%S.%fZ'
    _ = datetime.strptime(t[0], fmt).replace(tzinfo=tzinfo)
    '''

    logging = True
    test_reformat_iso_time_alt(logging)

    if False:
        tests = [test_reformat_iso_time, test_normalize_time_string, test_iso_time_to_array, test_day_of_year,
                 test_array_to_iso_time, test_get_dt_format, test_reformat_iso_time_alt]
        for test in tests:
            if logging:
                print("Calling " + test.__name__)
            test()
