import re
import math
from datetime import datetime

iso8601_duration = "P((\\d+)Y)?((\\d+)M)?((\\d+)D)?(T((\\d+)H)?((\\d+)M)?((" + "\\d?\\.?\\d+" + ")S)?)?"
iso8601_duration_pattern = re.compile(iso8601_duration)

# the number of days in each month.
DAYS_IN_MONTH = [[0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 0],
                 [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 0]]

# the number of days to the first of each month.
DAY_OFFSET = [[0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365],
              [0, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]]


def is_leap_year(year):
    """Determine if a given year is a leap year.

    Parameters
    ----------
    year: int or float
        year >= 1582 and year <= 2400

    Returns
    -------
    bool:
        True for a leap year, False otherwise.

    """

    if year < 1582 or year > 2400:
        raise ValueError("year must be > 1582 and < 2400")

    return (year % 4) == 0 and (year % 400 == 0 or year % 100 != 0)


def day_of_year(year, month, day):
    """Compute day-of-year given year, month, and day.

    Parameters
    ----------
    year: int
        The year.
    month: int
        The month, from 1 to 12.
    day: int
        The day in the month.

    Returns
    -------
    int:
        The day of year.
    """

    if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
        raise ValueError("Year, Month, Day must be int. Given year={}, month={}, day={}.".format(year, month, day))

    if month == 1:
        return day

    if month < 1:
        raise ValueError("month must be greater than 0. Given: " + month)

    if month > 12:
        raise ValueError("month must be less than 13. Given: " + month)

    if day > 366:
        raise ValueError("day must be less than 367. Given: " + day)

    if is_leap_year(year):
        return DAY_OFFSET[1][month] + day
    else:
        return DAY_OFFSET[0][month] + day


def normalize_time(time):
    """Normalize time by expressing day of year and month and day of month, and moving hour="24" into the next day.

    Notes
    -----
    This also handles day increment or decrements, by:
        1. handle day=0 by decrementing month and adding the days in the new
            month.
        2. handle day=32 by incrementing month.
        3. handle negative components by borrowing from the next significant.
    Note that [Y,1,dayOfYear,...] is accepted, but the result will be Y,m,d.

    Parameters
    ----------
    time: list
        The seven-component time Y, m, d, H, M, S, nanoseconds.

    Examples
    --------
    >>> from hapiclient.timeUtil import normalize_time
    >>> time = [1997, 1, 140, 0, 0, 0, 0]
    >>> time
    [1997, 5, 20, 0, 0, 0, 0]
    """

    while time[3] >= 24:
        time[2] += 1
        time[3] -= 24

    if time[6] < 0:
        time[5] -= 1
        time[6] += 1000000000

    if time[5] < 0:
        time[4] -= 1  # take a minute
        time[5] += 60  # add 60 seconds.

    if time[4] < 0:
        time[3] -= 1  # take an hour
        time[4] += 60  # add 60 minutes

    if time[3] < 0:
        time[2] -= 1  # take a day
        time[3] += 24  # add 24 hours

    if time[2] < 1:
        time[1] -= 1  # take a month
        leap = is_leap_year(time[0])
        if time[1] == 0:
            extraDays = 31
        else:
            extraDays = DAYS_IN_MONTH[leap][time[1]]
        daysInMonth = DAYS_IN_MONTH + extraDays
        time[2] += daysInMonth  # add 24 hours

    if time[1] < 1:
        time[0] = time[0] - 1  # take a year
        time[1] = time[1] + 12  # add 12 months

    if time[3] > 24:
        raise ValueError("time[3] (hour) is greater than 24.")

    if time[1] > 12:
        time[0] = time[0] + 1
        time[1] = time[1] - 12

    if time[1] == 12 and 31 < time[2] < 62:
        time[0] = time[0] + 1
        time[1] = 1
        time[2] = time[2] - 31
        return

    if is_leap_year(time[0]):
        leap = 1
    else:
        leap = 0

    if time[2] == 0:
        time[1] = time[1] - 1
        if time[1] == 0:
            time[0] = time[0] - 1
            time[1] = 12

        time[2] = DAYS_IN_MONTH[leap][time[1]]

    d = DAYS_IN_MONTH[leap][time[1]]
    while time[2] > d:
        time[1] = time[1] + 1
        time[2] -= d
        d = DAYS_IN_MONTH[leap][time[1]]
        if time[1] > 12:
            raise ValueError("time[2] (month) is greater than 12.")


def normalize_time_string(time):
    """Normalizes time by expressing day of year and month and day of month, and moving hour="24" into the next day.

    Notes
    -----
    This also handles day increment or decrements, by:
        1. handle day=0 by decrementing month and adding the days in the new month.
        2. handle day=32 by incrementing month.
        3. handle negative components by borrowing from the next significant.
    Note that [Y,1,dayOfYear,...] is accepted, but the result will be Y,m,d.

    Parameters
    ----------
    time: str
        Any isoTime format string.

    Returns
    -------
    str
        The time in standard form. $Y-$m-$dT$H:$M:$S.$(subsec,places=9)Z

    Examples
    --------
    All of the following return
        '1969-07-20T00:00:00.000000000Z'

    >>> from hapiclient.timeUtil import normalize_time_string
    >>> normalize_time_string("1969-07-20")
    >>> normalize_time_string("1969-06-50")
    >>> normalize_time_string("1969-07-20T00")
    >>> normalize_time_string("1969-07-20T00:00")
    >>> normalize_time_string("1969-07-20T00:00:00")
    >>> normalize_time_string("1969-07-20T00:00:00.0")
    """

    nn = iso_time_to_array(time)
    normalize_time(nn)
    return "%d-%02d-%02dT%02d:%02d:%02d.%09dZ" % (nn[0], nn[1], nn[2], nn[3], nn[4], nn[5], nn[6])


def reformat_iso_time(exampleForm, time):
    """Rewrite a time string in the format of an example time.

    Notes
    -----
    This allows direct comparisons of times for sorting.
    TODO: there's an optimization here, where if input and output are both $Y-$j or
    both $Y-$m-$d, then we need not break apart and recombine the time
    (iso_time_to_array call can be avoided).

    Parameters
    ----------
    exampleForm: str
        ISO8601 time string.
    time: str
        The time in any allowed ISO8601 time format.
    Returns
    -------
    str
        Same time but in the same form as exampleForm.

    Examples
    --------
    >>> from hapiclient.timeUtil import reformat_iso_time
    >>> reformat_iso_time( '2020-01-01T00:00Z', '2020-112Z' )
    '2020-04-21T00:00Z'
    >>> reformat_iso_time( '2020-01-01T00:00:00Z', '2020-01-01T00:10Z' )
    '2020-04-21T00:10:00Z'
    >>> reformat_iso_time( '2020-01-01T00:00:00.00Z', '2020-01-01T00:10:11Z' )
    '2020-04-21T00:10:11.00Z'

    """

    c = exampleForm[8]
    nn = iso_time_to_array(normalize_time_string(time))
    if c == 'T':
        # $Y-$jT
        nn[2] = day_of_year(nn[0], nn[1], nn[2])
        nn[1] = 1
        time = "%d-%03dT%02d:%02d:%02d.%09dZ" % (nn[0], nn[2], nn[3], nn[4], nn[5], nn[6])
    elif c == 'Z':
        nn[2] = day_of_year(nn[0], nn[1], nn[2])
        nn[1] = 1
        time = "%d-%03dZ" % (nn[0], nn[2])
    else:
        if len(exampleForm) == 10:
            c = 'Z'
        else:
            c = exampleForm[10]

        if c == 'T':
            # $Y-$jT
            time = "%d-%02d-%02dT%02d:%02d:%02d.%09dZ" % (nn[0], nn[1], nn[2], nn[3], nn[4], nn[5], nn[6])
        elif c == 'Z':
            time = "%d-%02d-%02dZ" % (nn[0], nn[1], nn[2])

    if exampleForm.endswith("Z"):
        return time[0:len(exampleForm) - 1] + "Z"
    else:
        return time[0:len(exampleForm)]


def now():
    """Returns the current time as a list of integers.
    """
    n = datetime.utcnow()
    return [n.year, n.month, n.day, n.hour, n.minute, n.second, n.microsecond * 1000]


def iso_time_to_array(time):
    """ Convert iso time to array [ year, months, days, hours, minutes, seconds, nanoseconds ].

    Notes
    -----
    preserving the day of year notation if this was used. See the class documentation for allowed time formats, which
    are a subset of ISO8601 times.  This also supports "now", "now-P1D", and other simple extensions.
    The following are valid inputs:
        1. 2021
        2. 2021-01
        3. 2020-01-01
        4. 2020-01-01Z
        5. 2020-01-01T00Z
        6. 2020-01-01T00:00Z
        7. now
        8. now-P1D
        9. lastday-P1D
        10. lasthour-PT1H

    Parameters
    ----------
    time: str
        ISO8601 time to decompose

    Returns
    -------
    list
        The decomposed time array [ year, months, days, hours, minutes, seconds, nanoseconds ]

    Examples
    --------
    >>> from hapiclient.timeUtil import iso_time_to_array
    >>> iso_time_to_array("1969-06-20")
    [1969, 6, 20, 0, 0, 0, 0]

    >>> iso_time_to_array("1969-06-20T01")
    [1969, 6, 20, 1, 0, 0, 0]
    """

    time = time.strip()
    if len(time) == 4:
        result = [int(time), 1, 1, 0, 0, 0, 0]
    elif len(time) == 5 and time.endswith('Z'):
        time = time.strip('Z')
        result = [int(time), 1, 1, 0, 0, 0, 0]
    elif time.startswith("now") or time.startswith("last"):
        remainder = None
        if time.startswith("now"):
            n = now()
            remainder = time[3:]
        else:
            p = re.compile("last([a-z]+)([\\+|\\-]P.*)?")
            m = p.match(time)
            if m is not None:
                n = now()
                unit = m.group(1)
                remainder = m.group(2)
                if unit == "year":
                    idigit = 1
                elif unit == "month":
                    idigit = 2
                elif unit == "day":
                    idigit = 3
                elif unit == "hour":
                    idigit = 4
                elif unit == "minute":
                    idigit = 5
                elif unit == "second":
                    idigit = 6
                else:
                    raise Exception("unsupported unit: " + unit)

                if idigit > 1:
                    istart = idigit
                else:
                    istart = 1
                for id in range(istart, 3):
                    n[id] = 1

                if idigit > 3:
                    istart = idigit
                else:
                    istart = 3
                for id in range(istart, 7):
                    n[id] = 0

            else:
                raise Exception("expected lastday+P1D, etc")

        if remainder is None or len(remainder) == 0:
            return n
        elif remainder[0] == '-':
            return subtract(n, parse_iso8601_duration(remainder[1:]))

        elif remainder[0] == '+':
            return add(n, parse_iso8601_duration(remainder[1:]))

        return now()

    else:
        if len(time) < 7:
            raise Exception("time must have 4 or greater than 7 elements")

        # first, parse YMD part, and leave remaining components in time.
        if len(time) == 8 and time.endswith('Z'):
            time = time.strip('Z')
        if len(time) == 7:
            result = [int(time[0:4]), int(time[5:7]), 1,  # days
                      0, 0, 0, 0]
            time = ""
        elif len(time) == 8:
            result = [int(time[0:4]), 1, int(time[5:8]),  # days
                      0, 0, 0, 0]
            time = ""
        elif time[8] == 'T':
            result = [int(time[0:4]), 1, int(time[5:8]),  # days
                      0, 0, 0, 0]
            time = time[9:]
        elif time[8] == 'Z':
            result = [int(time[0:4]), 1, int(time[5:8]),  # days
                      0, 0, 0, 0]
            time = time[9:]
        else:
            result = [int(time[0:4]), int(time[5:7]), int(time[8:10]), 0, 0, 0, 0]
            if len(time) == 10:
                time = ""
            else:
                time = time[11:]

        # second, parse HMS part.
        if time.endswith("Z"):
            time = time[0:-1]

        if len(time) >= 2:
            result[3] = int(time[0:2])

        if len(time) >= 5:
            result[4] = int(time[3:5])

        if len(time) >= 8:
            result[5] = int(time[6:8])

        if len(time) > 9:
            result[6] = int((math.pow(10, 18 - len(time))) * int(time[9:]))

        normalize_time(result)

    return result


def parse_iso8601_duration(stringIn):
    """Parse ISO8601 duration into a list [year,mon,day,hour,min,sec,nanos].

    Notes
    -----
    This does not allow fractional day, hours or minutes! Examples include:
        1. P1D - one day
        2. PT1M - one minute
        3. PT0.5S - 0.5 seconds

    TODO: there exists more complete code elsewhere.
    Parameters
    ----------
    stringIn: str
        The ISO8601 duration.

    Returns
    -------
    list
        A 7 element array with [year,mon,day,hour,min,sec,nanos].


    Examples
    --------
    >>> from hapiclient.timeUtil import parse_iso8601_duration
    >>> parse_iso8601_duration('P1Y')
    [1, 0, 0, 0, 0, 0, 0]

    >>> parse_iso8601_duration('P1M')
    [0, 1, 0, 0, 0, 0, 0]

    >>> parse_iso8601_duration('P1D')
    [0, 0, 1, 0, 0, 0, 0]

    >>> parse_iso8601_duration('PT1H')
    [0, 0, 0, 1, 0, 0, 0]

    >>> parse_iso8601_duration('PT1M')
    [0, 0, 0, 0, 1, 0, 0]

    >>> parse_iso8601_duration('PT1S')
    [0, 0, 0, 0, 0, 1, 0]

    >>> parse_iso8601_duration('P3Y6M4DT12H30M5S')
    [3, 6, 4, 12, 30, 5, 0]

    """

    def parse_int(s, deft):
        """ Parse the int or return the default value
        """
        if s is None:
            return deft
        else:
            return int(s)


    def parse_double(d, deft):
        """ Parse the double or return the default value
        """
        if d is None:
            return deft
        else:
            return float(d)


    m = iso8601_duration_pattern.match(stringIn)
    if m is not None:
        dsec = parse_double(m.group(13), 0)
        sec = int(dsec)
        nanosec = int((dsec - sec) * 1e9)
        return [parse_int(m.group(2), 0), parse_int(m.group(4), 0), parse_int(m.group(6), 0),
                parse_int(m.group(9), 0), parse_int(m.group(11), 0), sec, nanosec]
    else:
        if "P" in stringIn and "S" in stringIn and not "T" in stringIn:
            raise Exception("ISO8601 duration expected but not found.  Was the T missing before S?")
        else:
            raise Exception("ISO8601 duration expected but not found.")


def parse_iso8601_timerange(stringIn):
    """Parse the ISO8601 time range into start and stop times.

    Parameters
    ----------
    stringIn: str
        ISO8601 time range

    Returns
    -------
    list
        The time start and stop [ Y,m,d,H,M,S,N, Y,m,d,H,M,S,N ]

    Examples
    --------
    >>> from hapiclient.timeUtil import parse_iso8601_timerange

    >>> parse_iso8601_timerange("1998-01-02/1998-01-17")
    [1998, 1, 2, 0, 0, 0, 0, 1998, 1, 17, 0, 0, 0, 0]

    >>> parse_iso8601_timerange("1998-002/1998-017")
    [1998, 1, 2, 0, 0, 0, 0, 1998, 1, 17, 0, 0, 0, 0]
    """

    ss = stringIn.split("/")
    if len(ss) != 2:
        raise Exception("expected one slash (/) splitting start and stop times.")

    if len(ss[0]) == 0 or not (ss[0][0].isdigit() or ss[0][0] == 'P' or ss[0].startswith("now")):
        raise Exception("first time/duration is misformatted.  Should be ISO8601 time or duration like P1D.")

    if len(ss[1]) == 0 or not (ss[1][0].isdigit() or ss[1][0] == 'P' or ss[1].startswith("now")):
        raise Exception("second time/duration is misformatted.  Should be ISO8601 time or duration like P1D.")

    result = [None] * 14
    if ss[0].startswith("P"):
        duration = parse_iso8601_duration(ss[0])
        time = iso_time_to_array(ss[1])
        for i in range(0, 7):
            result[i] = time[i] - duration[i]
        for i in range(7, 14):
            result[i] = time[i - 7]
        return result
    elif ss[1].startswith("P"):
        time = iso_time_to_array(ss[0])
        duration = parse_iso8601_duration(ss[1])
        for i in range(0, 7):
            result[i] = time[i]
        for i in range(7, 14):
            result[i] = time[i - 7] + duration[i - 7]
        return result
    else:
        starttime = iso_time_to_array(ss[0])
        stoptime = iso_time_to_array(ss[1])
        for i in range(0, 7):
            result[i] = starttime[i]
        for i in range(7, 14):
            result[i] = stoptime[i - 7]
        return result


def subtract(base, offset):
    """Subtract the offset from the base time.

    Parameters
    ----------
    base:
        A time
    offset:
        offset in each component.

    Returns
    -------
        A time.
    """

    result = [None] * 7
    for i in range(0, 7):
        result[i] = base[i] - offset[i]
    if result[0] > 400:
        normalize_time(result)

    return result


def add(base, offset):
    """Add the offset to the base time.

    This should not be used to combine two offsets, because the code has not been verified for this use.

    Parameters
    ----------
    base:
        a time
    offset:
        offset in each component.

    Returns
    -------
        A time.
    """
    result = [None] * 7
    for i in range(0, 7):
        result[i] = base[i] + offset[i]

    normalize_time(result)
    return result


# Hari's additions start here

def array_to_iso_time(dt, dt_format):
    """Converts a 7-element list with [year, mon, day, hour, min, sec, nanos] to the given format.

    The following are valid inputs for dt_format:
        1. 'yyyy'
        2. 'yyyy-mm'
        3. 'yyyy-mm-dd'
        4. 'yyyy-mm-ddThh'
        5. 'yyyy-mm-ddThh:mm'
        6. 'yyyy-mm-ddThh:mm:ss'
        7. 'yyyy-mm-ddThh:mm:ss.{1-9}'
        8. 'yyyy-doy'
        9. 'yyyy-doyThh'
        10. 'yyyy-doyThh:mm'
        11. 'yyyy-doyThh:mm:ss'
        12. 'yyyy-doyThh:mm:ss.{1-9}'

    Parameters
    ----------
    dt: list
        A 7-element list with [year, mon, day, hour, min, sec, nanos].

    dt_format: str


    Returns
    -------
    str
        Time in given format.

    Examples
    --------

        >>> from hapiclient.timeUtil import array_to_iso_time

        >>> array_to_iso_time([1998, 1, 2, 0, 0, 0, 0], 'yyyy')
        1998

        >>> array_to_iso_time([1998, 1, 2, 0, 0, 0, 0], 'yyyy-mm-dd')
        1998-01-02

        >>> array_to_iso_time([1998, 1, 2, 0, 0, 0, 1234], 'yyyy-mm-ddThh:mm:ss.9')
        1998-01-02T00:00:00.123400000

        >>> array_to_iso_time([1998, 1, 2, 0, 0, 0, 1], 'yyyy-mm-ddThh:mm:ss.5')
        1998-01-02T00:00:00.10000

        >>> array_to_iso_time([1998, 1, 2, 0, 0, 0, 156], 'yyyy-mm-ddThh:mm:ss.6')
        1998-01-02T00:00:00.156000
    """

    if dt_format == 'yyyy':
        return '{}'.format(dt[0])
    if dt_format == 'yyyy-mm':
        return '{}-{:02}'.format(dt[0], dt[1])
    if dt_format == 'yyyy-mm-dd':
        return '{}-{:02}-{:02}'.format(dt[0], dt[1], dt[2])
    if dt_format == 'yyyy-mm-ddThh':
        return '{}-{:02}-{:02}T{:02}'.format(dt[0], dt[1], dt[2], dt[3])
    if dt_format == 'yyyy-mm-ddThh:mm':
        return '{}-{:02}-{:02}T{:02}:{:02}'.format(dt[0], dt[1], dt[2], dt[3], dt[4])
    if dt_format == 'yyyy-mm-ddThh:mm:ss':
        return '{}-{:02}-{:02}T{:02}:{:02}:{:02}'.format(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])

    if '.' in dt_format and dt_format.split('.')[0] == 'yyyy-mm-ddThh:mm:ss':
        width = int(dt_format.split('.')[-1])
        return '{}-{:02}-{:02}T{:02}:{:02}:{:02}.{:0<{width}}'\
            .format(
                dt[0], dt[1], dt[2],               # Year, Month, Day
                dt[3], dt[4], dt[5],               # Hour, Minute, Second
                dt[6],                             # Nanosecond
                width=width
            )

    if dt_format == 'yyyy-doy':
        return '{}-{:03}'.format(dt[0], day_of_year(dt[0], dt[1], dt[2]))
    if dt_format == 'yyyy-doyThh':
        return '{}-{:03}T{:02}'.format(dt[0], day_of_year(dt[0], dt[1], dt[2]), dt[3])
    if dt_format == 'yyyy-doyThh:mm':
        return '{}-{:03}T{:02}:{:02}'.format(dt[0], day_of_year(dt[0], dt[1], dt[2]), dt[3], dt[4])
    if dt_format == 'yyyy-doyThh:mm:ss':
        return '{}-{:03}T{:02}:{:02}:{:02}'.format(dt[0], day_of_year(dt[0], dt[1], dt[2]), dt[3], dt[4], dt[5])

    if '.' in dt_format and dt_format.split('.')[0] == 'yyyy-doyThh:mm:ss':
        width = int(dt_format.split('.')[-1])
        return '{}-{:03}T{:02}:{:02}:{:02}.{:0<{width}}'\
            .format(
                dt[0],                             # year
                day_of_year(dt[0], dt[1], dt[2]),  # day of year
                dt[3], dt[4], dt[5],               # Hour, Minute, Second
                dt[6],                             # nanosecond
                width=width
            )


def get_dt_format(dateTimeString):
    """Get the format of a time string.

    The format of the given time string can be one of the following:
        1. 'yyyy'
        2. 'yyyy-mm'
        3. 'yyyy-mm-dd'
        4. 'yyyy-mm-ddThh'
        5. 'yyyy-mm-ddThh:mm'
        6. 'yyyy-mm-ddThh:mm:ss'
        7. 'yyyy-mm-ddThh:mm:ss.{1-9}'

        8. 'yyyy-doy'
        9. 'yyyy-doyThh'
        10. 'yyyy-doyThh:mm'
        11. 'yyyy-doyThh:mm:ss'
        12. 'yyyy-doyThh:mm:ss.{1-9}'


    Parameters
    ----------
    dateTimeString: str

    Returns
    -------
    format: str

    """

    y_re = lambda x: re.match(r'^([12]\d{3})$', x)
    ym_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2]))$', x)
    ymd_re = lambda x: re.match(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$', x)
    ydoy_re = lambda x: re.match(r'^([12]\d{3}-[0123]\d{2})$', x)

    h_re = lambda x: re.match(r'^([01]\d|2[0-3])$', x)
    hm_re = lambda x: re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', x)
    hms_re = lambda x: re.match(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$', x)
    hmsns_re = lambda x: re.match(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d|60).(\d{1,9})$', x)

    dateTimeString = dateTimeString.replace('Z', '')
    dateTimeType = ''

    time = None
    date = dateTimeString
    if 'T' in dateTimeString:
        date, time = dateTimeString.split('T')

    if y_re(date):
        dateTimeType += 'yyyy'
    elif ym_re(date):
        dateTimeType += 'yyyy-mm'
    elif ymd_re(date):
        dateTimeType += 'yyyy-mm-dd'
    elif ydoy_re(date):
        dateTimeType += 'yyyy-doy'

    if time:
        dateTimeType += 'T'

        if h_re(time):
            dateTimeType += 'hh'
        elif hm_re(time):
            dateTimeType += 'hh:mm'
        elif hms_re(time):
            dateTimeType += 'hh:mm:ss'
        elif hmsns_re(time):
            dateTimeType += 'hh:mm:ss.{}'.format(len(time.split('.')[-1]))

    return dateTimeType


def reformat_iso_time_alt(form_to_match, given_form):
    """Converts the given time string to the form of a reference time string.

    Parameters
    ----------
    form_to_match: str
    given_form: str

    Returns
    -------
    str
        Given time string converted to the form of reference time string.

    Examples
    --------
    >>> from hapiclient.timeUtil import reformat_iso_time_alt
    >>> reformat_iso_time_alt('2020-01-01T00:00Z', '2020-112Z')
    2020-04-21T00:00Z

    >>> reformat_iso_time_alt('2020-01-01T00:00:00Z', '2020-01-01T00:10Z')
    2020-04-21T00:10:00Z

    >>> reformat_iso_time_alt('2020-01-01T00:00:00.00Z', '2020-01-01T00:10:11Z')
    2020-04-21T00:10:11.00Z

    Notes
    -----
    Differences between `reformat_iso_time()` and `reformat_iso_time_alt()`.

    `reformat_iso_time()`
        1. Always assumes there is a Z at the end in `form_to_match`.
        2. Always returns a time string with a Z at the end.
        3. Failed to convert from yyyy-doy to yyyy
        4. Failed to convert from yyyy-doy to yyyy-mm

    """

    form_to_match_format = get_dt_format(form_to_match)
    dt = iso_time_to_array(given_form)
    res = array_to_iso_time(dt, form_to_match_format)

    if 'Z' in form_to_match and 'Z' not in res:
        res += 'Z'

    return res
