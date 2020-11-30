import isodate
from hapiclient.hapi import hapitime2datetime, hapitime_format_str


def reformat_hapitime(form_to_match, given_form):

    print('ref:       {}\ngiven:     {}'.format(form_to_match, given_form))

    if 'T' in given_form:
        dt_given = isodate.parse_datetime(given_form)
    else:
        # Remove trailing Z b/c parse_date does not implement of date with
        # trailing Z, which is valid IS8601.
        dt_given = isodate.parse_date(given_form[0:-1])

    # Get format string, e.g., %Y-%m-%dT%H
    format_ref = hapitime_format_str([form_to_match])
    converted = dt_given.strftime(format_ref)
    
    if len(converted) > len(form_to_match):
        converted = converted[0:len(form_to_match)-1] + "Z"
    print('converted: {}\nref fmt:   {}'.format(converted, format_ref))
    print('----')
    return converted


def test_reformat_hapitime(logging=False):


    dts = [
        "1989Z",

        "1989-01Z",

        "1989-001Z",
        "1989-01-01Z",

        "1989-001T00Z",
        "1989-01-01T00Z",

        "1989-001T00:00Z",
        "1989-01-01T00:00Z",

        "1989-001T00:00:00.Z",
        "1989-01-01T00:00:00.Z",

        "1989-01-01T00:00:00.0Z",
        "1989-001T00:00:00.0Z",

        "1989-01-01T00:00:00.00Z",
        "1989-001T00:00:00.00Z",

        "1989-01-01T00:00:00.000Z",
        "1989-001T00:00:00.000Z",

        "1989-01-01T00:00:00.0000Z",
        "1989-001T00:00:00.0000Z",

        "1989-01-01T00:00:00.00000Z",
        "1989-001T00:00:00.00000Z",

        "1989-01-01T00:00:00.000000Z",
        "1989-001T00:00:00.000000Z"
    ]


    for i in range(len(dts)):
        if "T" in dts[i]:
            dts.append("1989-001T" + dts[i].split("T")[1])

    # truncating
    for i in range(len(dts)):
        form_to_match = dts[i]
        for j in range(i + 1, len(dts)):
            given_form = dts[j]
            given_form_modified = reformat_hapitime(form_to_match, given_form)
            assert hapitime2datetime(given_form_modified) == hapitime2datetime(form_to_match)
            assert given_form_modified == form_to_match
            
    # padding
    dts = list(reversed(dts))
    for i in range(len(dts)):
        form_to_match = dts[i]
        for j in range(i + 1, len(dts)):
            given_form = dts[j]
            given_form_modified = reformat_hapitime(form_to_match, given_form)
            assert hapitime2datetime(given_form_modified) == hapitime2datetime(form_to_match)
            assert given_form_modified == form_to_match

test_reformat_hapitime()
