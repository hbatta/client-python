from timeUtil import *

def test_convert_dt_string1(logging=False):

    from hapi import hapitime2datetime
    import random

    y_re = lambda x: re.match(r'^([12]\d{3})$', x)
    ym_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2]))$', x)
    ymd_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$', x)
    ydoy_re = lambda x: re.match(r'^([12]\d{3}-[0123]\d{2})$', x)

    for _ in range(10):

        # conversion

        # TODO: Set random seed so test deterministic
        
        # y -> ydoy
        form_to_match = '1997-318'
        given_form = '{}'.format(random.randint(1800, 2020))
        given_form_modifed = convert_dt_string(form_to_match, given_form)

        if hapitime2datetime(given_form_modifed) != hapitime2datetime(given_form):
            print("Mismatch: ", given_form_modifed, given_form, hapitime2datetime(given_form_modifed), hapitime2datetime(given_form))
            assert False

        assert bool(ydoy_re(given_form_modifed))

        # ym -> ydoy
        form_to_match = '1997-318'
        given_form = '{}-{:02}'.format(random.randint(1800, 2020), random.randint(1, 12))
        given_form_modifed = convert_dt_string(form_to_match, given_form)
        assert hapitime2datetime(given_form_modifed) == hapitime2datetime(given_form)
        assert bool(ydoy_re(given_form_modifed))

        # ymd -> ydoy
        form_to_match = '1997-318'
        given_form = '{}-{:02}-{:02}'.format(random.randint(1800, 2020), random.randint(1, 12), random.randint(1, 28))
        given_form_modifed = convert_dt_string(form_to_match, given_form)
        assert hapitime2datetime(given_form_modifed) == hapitime2datetime(given_form)
        assert bool(ydoy_re(given_form_modifed))

        # ydoy -> y
        form_to_match = '1997'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modifed = convert_dt_string(form_to_match, given_form)
        assert hapitime2datetime(given_form_modifed) == hapitime2datetime(given_form.split('-')[0])
        assert bool(y_re(given_form_modifed))

        # ydoy -> ym
        form_to_match = '1997-11'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modifed = convert_dt_string(form_to_match, given_form)

        hdt = hapitime2datetime(given_form)[0]
        assert hapitime2datetime(given_form_modifed) == hapitime2datetime('{}-{:02}'.format(hdt.year, hdt.month))
        assert bool(ym_re(given_form_modifed))

        # ydoy -> ymd
        form_to_match = '1997-11-14'
        given_form = '{}-{:03}'.format(random.randint(1800, 2020), random.randint(1, 360))
        given_form_modifed = convert_dt_string(form_to_match, given_form)

        hdt = hapitime2datetime(given_form)[0]
        assert hapitime2datetime(given_form_modifed) == hapitime2datetime('{}-{:02}-{:02}'.format(hdt.year, hdt.month, hdt.day))
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
            assert hapitime2datetime(given_form_modifed) == hapitime2datetime(form_to_match)
            assert given_form_modifed == form_to_match

    # padding
    dts = list(reversed(dts))
    for i in range(len(dts)):
        form_to_match = dts[i]
        for j in range(i + 1, len(dts)):
            given_form = dts[j]
            given_form_modifed = convert_dt_string(form_to_match, given_form)
            assert hapitime2datetime(given_form_modifed) == hapitime2datetime(form_to_match)
            assert given_form_modifed == form_to_match


def test_convert_dt_string(logging=False):

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

                dt1 = hapitime2datetime(start)[0]
                dt2 = hapitime2datetime(converted_datetime)[0]
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
    logging = True
    if logging:
        print("Calling test_convert_dt_string().")
    test_convert_dt_string(logging=logging)