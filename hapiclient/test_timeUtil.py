from hapiclient.timeUtil import *


def test_reformat_iso_time():
    """Test of reformatIsoTime method, of class TimeUtil.
    """
    print("reformat_iso_time")
    expResult = "2020-04-21T00:00Z"
    result = reformat_iso_time("2020-01-01T00:00Z", "2020-112Z")
    assert expResult == result


def test_normalize_time_string():
    """Test of normalizeTimeString method, of class TimeUtil.
    """
    print("normalize_time_string")
    time = "2020-09-25";
    expResult = "2020-09-25T00:00:00.000000000Z"
    result = normalize_time_string(time)
    assert expResult == result


def test_iso_time_to_array():
    """ Test of isoTimeToArray method, of class TimeUtil.
    """
    print("iso_time_to_array")

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
    """Test array_to_iso_time.
    """
    print("array_to_iso_time")

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
    """ Test get_dt_format.
    """
    print("get_dt_format")

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
    """Test of dayOfYear method, of class TimeUtil.
    """
    print("day_of_year")
    year = 2000
    month = 5
    day = 29
    expResult = 150
    result = day_of_year(year, month, day)
    assert expResult == result


def test_convert_dt_string1(logging=False):
    from hapiclient.hapi import hapitime2datetime
    import random

    y_re = lambda x: re.match(r'^([12]\d{3})$', x)
    ym_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2]))$', x)
    ymd_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$', x)
    ydoy_re = lambda x: re.match(r'^([12]\d{3}-[0123]\d{2})$', x)

    for _ in range(10):

        random.seed(10)
        padz = lambda x: x if 'Z' in x else x + 'Z'

        # conversion

        # y -> ydoy
        form_to_match = '1997-318'
        given_form = '{}'.format(random.randint(1800, 2020))
        given_form_modifed = convert_dt_string(form_to_match, given_form)

        if hapitime2datetime(padz(given_form_modifed)) != hapitime2datetime(padz(given_form)):
            print("Mismatch: ", given_form_modifed, given_form, hapitime2datetime(padz(given_form_modifed)), hapitime2datetime(padz(given_form)))
            assert False

        assert bool(ydoy_re(given_form_modifed))

        # ym -> ydoy
        form_to_match = '1997-318'
        given_form = '{}-{:02}'.format(random.randint(1800, 2020), random.randint(1, 12))
        given_form_modifed = convert_dt_string(form_to_match, given_form)
        assert hapitime2datetime(padz(given_form_modifed)) == hapitime2datetime(padz(given_form))
        assert bool(ydoy_re(given_form_modifed))

        # ymd -> ydoy
        form_to_match = '1997-318'
        given_form = '{}-{:02}-{:02}'.format(random.randint(1800, 2020), random.randint(1, 12), random.randint(1, 28))
        given_form_modifed = convert_dt_string(form_to_match, given_form)
        assert hapitime2datetime(padz(given_form_modifed)) == hapitime2datetime(padz(given_form))
        assert bool(ydoy_re(given_form_modifed))

        # ydoy -> y
        form_to_match = '1997'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modifed = convert_dt_string(form_to_match, given_form)
        assert hapitime2datetime(padz(given_form_modifed)) == hapitime2datetime(padz(given_form.split('-')[0]))
        assert bool(y_re(given_form_modifed))

        # ydoy -> ym
        form_to_match = '1997-11'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modifed = convert_dt_string(form_to_match, given_form)

        hdt = hapitime2datetime(padz(given_form))[0]
        assert hapitime2datetime(padz(given_form_modifed)) == hapitime2datetime(padz('{}-{:02}'.format(hdt.year, hdt.month)))
        assert bool(ym_re(given_form_modifed))

        # ydoy -> ymd
        form_to_match = '1997-11-14'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modifed = convert_dt_string(form_to_match, given_form)

        hdt = hapitime2datetime(padz(given_form))[0]
        assert hapitime2datetime(padz(given_form_modifed)) == hapitime2datetime(padz('{}-{:02}-{:02}'.format(hdt.year, hdt.month, hdt.day)))
        assert bool(ymd_re(given_form_modifed))

    dts = [
        "1989",
        "1989-01",
        "1989-01-01",
        "1989-01-01T00",
        "1989-01-01T00:00",
        "1989-01-01T00:00:00",
        "1989-01-01T00:00:00.0",
        "1989-01-01T00:00:00.00",
        "1989-01-01T00:00:00.000",
        "1989-01-01T00:00:00.0000",
        "1989-01-01T00:00:00.00000",
        "1989-01-01T00:00:00.000000"
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
            given_form_modifed = convert_dt_string(form_to_match, given_form)
            assert hapitime2datetime(padz(given_form_modifed)) == hapitime2datetime(padz(form_to_match))
            assert given_form_modifed == form_to_match

    # padding
    dts = list(reversed(dts))
    for i in range(len(dts)):
        form_to_match = dts[i]
        for j in range(i + 1, len(dts)):
            given_form = dts[j]
            given_form_modifed = convert_dt_string(form_to_match, given_form)
            assert hapitime2datetime(padz(given_form_modifed)) == hapitime2datetime(padz(form_to_match))
            assert given_form_modifed == form_to_match


def test_convert_dt_string2(logging=False):
    padz = lambda x: x if 'Z' in x else x + 'Z'

    dts = [
            "1989",
            "1989-01",
            "1989-01-01",
            "1989-09-29T00",
            "1989-09-29T01",
            "1989-09-29T23",
            "1989-09-29T00:00",
            "1989-09-29T00:01",
            "1989-09-29T00:59",
            "1989-09-29T00:00:00",
            "1989-09-29T00:00:01",
            "1989-09-29T00:00:59",
            "1989-09-29T00:00:00.0",
            "1989-09-29T00:00:00.1",
            "1989-09-29T00:00:00.9",
            "1989-09-29T00:00:00.00",
            "1989-09-29T00:00:00.01",
            "1989-09-29T00:00:00.99",
            "1989-09-29T00:00:00.000",
            "1989-09-29T00:00:00.001",
            "1989-09-29T00:00:00.999",
            "1989-09-29T00:00:00.0000",
            "1989-09-29T00:00:00.0001",
            "1989-09-29T00:00:00.9999",
            "1989-09-29T00:00:00.00000",
            "1989-09-29T00:00:00.00001",
            "1989-09-29T00:00:00.99999",
            "1989-09-29T00:00:00.000000",
            "1989-09-29T00:00:00.000001",
            "1989-09-29T00:00:00.999999"
        ]

    for i in range(len(dts)):
        dts.append(dts[i] + "Z")

    for i in range(len(dts)):
        if "T" in dts[i]:
            dts.append("1989-009T" + dts[i].split("T")[1])

    def xprint(start, data, converted):
        print("START           ", start)
        print("Data            ", data)
        print("START Converted ", converted)
        print("-" * 80)

    from hapiclient import hapitime2datetime
    try:
        # Python 2
        import pytz
        tzinfo = pytz.UTC
    except:
        tzinfo = datetime.timezone.utc

    for i in range(len(dts)):
        for j in range(len(dts)):
            try:
                data = dts[i]
                start = dts[j]
                converted_datetime = convert_dt_string(data, start)
                if len(converted_datetime) != len(data):
                    assert False, "Conversion failure. Lengths do not match."
                    if logging:
                        xprint(start, data, converted_datetime)

                dt1 = hapitime2datetime(padz(start))[0]
                dt2 = hapitime2datetime(padz(converted_datetime))[0]
                if start[-1] != 'Z':
                    # hapitime2datetime() requires input to end with 'Z' and output will
                    # always have tzinfo=<UTC>. If `start` does not end with 'Z'
                    # then dt1 will not have a timezone and equality check against
                    # dt2 will fail.
                    dt1 = dt1.replace(tzinfo=tzinfo)
                    dt2 = dt2.replace(tzinfo=tzinfo)
                if dt1 != dt2:
                    if logging:
                        xprint(dts[j], dts[i], convert_dt_string(data, start))
                    if converted_datetime[-1] == "Z" and dts[j][-1] == "Z":
                        assert False, "Conversion failure. Times are not equal."
            except Exception as e:
                print("Exception caused by:")
                xprint(dts[j], dts[i], convert_dt_string(data, start))
                print(e)


if __name__ == '__main__':
    '''
    The test_convert_dt_string1() will not create any check that is not checked by test_convert_dt_string2(). 
    test_convert_dt_string1() is more specific than test_convert_dt_string2(). It is written so that it will be easy to 
    debug looking at where it's failing while adding new features in the future.
    '''

    tests = [test_reformat_iso_time, test_normalize_time_string, test_iso_time_to_array, test_day_of_year,
             test_array_to_iso_time, test_get_dt_format]
    for test in tests:
        test()

    # logging = True
    # if logging:
    #     print("Calling test_convert_dt_string1().")
    # test_convert_dt_string1(logging=logging)
