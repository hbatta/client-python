
def pad_time(time, doy=False, length=7):
    """
 
    time is one of
        1A. a tuple of year, [month, [day, [hour, [min, [second, [Z]]]]]]
        1B. a tuple of year, [doy, [hour, [min, [second, [Z]]]]]]
        2.  a HAPI time string (subset of ISO8601) 
        3.  a datetime object

    If 1. or 2. have 'Z' at end, returned string has 'Z' at end.
    If 3. and timezone, returned string has 'Z' at end (and time is converted to GMT).

    pad_time((2000, 1, 1, 2))            # 2000-01-01T02:00:00.000
    pad_time((2000, 1, 1, 2, 3))         # 2000-01-01T02:03:00.000
    pad_time((2000, 1, 1, 2, 3, 4))      # 2000-01-01T02:03:04.000
    pad_time((2000, 1, 1, 2, 3, 4, 567)) # 2000-01-01T02:03:04.567

    pad_time((2000, 1), length=3)        # 2000-01-01
    pad_time((2000, 1, 2), length=4)     # 2000-01-02T00

    pad_time((2000, 1, 2), length=2)     # Error?

    # TODO
    pad_time(2000)                       # 2000-01-01T00:00:00.000
    pad_time((2000))                     # 2000-01-01T00:00:00.000
    pad_time((2000, 1))                  # 2000-01-01T00:00:00.000
    pad_time((2000, 1, 1))               # 2000-01-01T00:00:00.000

    pad_time((2000, 32), doy=True)       # 2000-02-01T00:00:00.000
    pad_time((2000, 32, 4), doy=True)    # 2000-02-01T04:00:00.000
    etc.
    """

    # Not tested
    if type(time) == str:
        time = hapitime2datetime(str)
        return pad_time(time, **kwargs)

    # Not tested
    if type(time) == datetime:
        return pad_time(tuple(time))

    def tpad(time, doy=False, length=7):

        # TODO: Check that time is valid
        time = list(time)

        assert(len(time) > 2)
        
        if len(time) > length:
            time = time[0:length]
        else:
            pad = length - len(time)
            time = time + pad*[0]

        return tuple(time)

    # ISO 8601
    assert(len(time) > 2)

    if length == 7:
        return '%04d-%02d-%02dT%02d:%02d:%02d.%03d' % tpad(time, length=length)
    elif length == 6:
        return '%04d-%02d-%02dT%02d:%02d:%02d' % tpad(time, length=length)        
    elif length == 5:
        return '%04d-%02d-%02dT%02d:%02d' % tpad(time, length=length)        
    elif length == 4:
        return '%04d-%02d-%02dT%02d' % tpad(time, length=length)        
    elif length == 3:
        return '%04d-%02d-%02d' % tpad(time, length=length)        
