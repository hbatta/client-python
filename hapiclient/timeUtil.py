
# 
# the number of days in each month.
# 
DAYS_IN_MONTH = [ [ 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 0 ],
    [ 0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 0 ] ]


# 
# the number of days to the first of each month.
# 
DAY_OFFSET = [ [ 0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365 ],
    [ 0, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366 ] ]

def is_leap_year( year ):
    if year<1582 or year>2400:
        raise Exception("year must be between 1582 and 2400")
    return (year % 4) == 0 and (year % 400 == 0 or year % 100 != 0)  
        
# 
# return the doy of year of the month and day for the year. For example, in
# @param year the year
# @param month the month, from 1 to 12.
# @param day the day in the month.
# @return the day of year.
# 
def day_of_year( year, month, day) :
    if (month == 1) :
        return day
    
    if (month < 1) :
        raise Exception("month must be greater than 0.")
    
    if (month > 12) :
        raise Exception("month must be less than 12.")
    
    if (day > 366) :
        raise Exception("day (" + day + ") must be less than 366.")
    
    if is_leap_year(year):
        return DAY_OFFSET[1][month] + day
    else:
        return DAY_OFFSET[0][month] + day


# 
# normalize the decomposed time by expressing day of year and month and day
# of month, and moving hour="24" into the next day. This also handles day
# increment or decrements, by:<ul>
# <li>handle day=0 by decrementing month and adding the days in the new
# month.
# <li>handle day=32 by incrementing month.
# <li>handle negative components by borrowing from the next significant.
# </ul>
# Note that [Y,1,dayOfYear,...] is accepted, but the result will be Y,m,d.
# @param time the seven-component time Y,m,d,H,M,S,nanoseconds
# 
def normalize_time(time) :
    #logger.entering( "TimeUtil", "normalizeTime" )
    while (time[3] >= 24) :
        time[2] += 1
        time[3] -= 24
    
    if (time[6] < 0) :
        time[5] -= 1
        time[6] += 1000000000
    
    if (time[5] < 0) :
        time[4] -= 1; # take a minute
        time[5] += 60; # add 60 seconds.
    
    if (time[4] < 0) :
        time[3] -= 1; # take an hour
        time[4] += 60; # add 60 minutes
    
    if (time[3] < 0) :
        time[2] -= 1; # take a day
        time[3] += 24; # add 24 hours
    
    if (time[2] < 1) :
        time[1] -= 1; # take a month
        leap= isLeapYear(time[0])
        if ( time[1]==0 ):
            extraDays= 31
        else:
            extraDays= DAYS_IN_MONTH[ leap ][ time[1] ]
        daysInMonth =  daysInMonth + extraDays
        time[2] += daysInMonth; # add 24 hours
    
    if (time[1] < 1) :
        time[0] = time[0] - 1; # take a year
        time[1] = time[1] + 12; # add 12 months
    
    if (time[3] > 24) :
        raise Exception("time[3] is greater than 24 (hours)")
    
    if (time[1] > 12) :
        time[0]= time[0] + 1
        time[1]= time[1] - 12
    
    if (time[1] == 12 and time[2]>31 and time[2]<62 ) :
        time[0] = time[0] + 1
        time[1] = 1
        time[2] = time[2]-31
        logger.exiting( "TimeUtil", "normalizeTime" )
        return
    
    if ( is_leap_year(time[0]) ):
        leap= 1
    else:
        leap= 0
    
    if (time[2] == 0) :
        time[1] = time[1] - 1
        if (time[1] == 0) :
            time[0] = time[0] - 1
            time[1] = 12
        
        time[2] = DAYS_IN_MONTH[leap][time[1]]
    
    d = DAYS_IN_MONTH[leap][time[1]]
    while (time[2] > d) :
        time[1] = time[1] + 1
        time[2] -= d
        d = DAYS_IN_MONTH[leap][time[1]]
        if (time[1] > 12) :
            raise Exception("time[2] is too big")
    
    #logger.exiting( "TimeUtil", "normalizeTime" )



# 
# return $Y-$m-$dT$H:$M:$S.$(subsec,places=9)Z
# 
# @param time any isoTime format string.
# @return the time in standard form.
# 
def normalize_time_string(time) :
    nn = iso_time_to_array(time)
    normalize_time(nn)
    return "%d-%02d-%02dT%02d:%02d:%02d.%09dZ" % ( nn[0], nn[1], nn[2], nn[3], nn[4], nn[5], nn[6] )


# 
# Rewrite the time using the format of the example time. For example,
# <pre>
# :@code
    # from org.hapiserver.TimeUtil import *
    # print rewriteIsoTime( '2020-01-01T00:00Z', '2020-112Z' ) # ->  '2020-04-21T00:00Z'
    # 
# </pre>
# This allows direct comparisons of times for sorting.
# TODO: there's an optimization here, where if input and output are both $Y-$j or
# both $Y-$m-$d, then we need not break apart and recombine the time
# (isoTimeToArray call can be avoided).
# 
# @param exampleForm isoTime string.
# @param time the time in any allowed isoTime format
# @return same time but in the same form as exampleForm.
# 
def reformat_iso_time( exampleForm, time):
    c = exampleForm[8]
    nn = iso_time_to_array( normalize_time_string(time) )
    if c=='T':
        # $Y-$jT
        nn[2] = day_of_year(nn[0], nn[1], nn[2])
        nn[1] = 1
        time = "%d-%03dT%02d:%02d:%02d.%09dZ" % ( nn[0], nn[2], nn[3], nn[4], nn[5], nn[6] )
    elif c=='Z':
        nn[2] = day_of_year(nn[0], nn[1], nn[2])
        nn[1] = 1
        time = "%d-%03dZ" % ( nn[0], nn[2] )
    else:
        if ( len(exampleForm) == 10) :
            c = 'Z'
        else :
            c = exampleForm[10]
        
        if (c == 'T') :
            # $Y-$jT
            time = "%d-%02d-%02dT%02d:%02d:%02d.%09dZ" % ( nn[0], nn[1], nn[2], nn[3], nn[4], nn[5], nn[6])
        elif (c == 'Z') :
            time = "%d-%02d-%02dZ" % ( nn[0], nn[1], nn[2])
            
    if (exampleForm.endswith("Z")) :
        return time[ 0:len(exampleForm)- 1 ] + "Z"
    else :
        return time[ 0:len(exampleForm) ]

# return the current time
def now():
    from datetime import datetime
    n= datetime.utcnow()
    return [ n.year, n.month, n.day, n.hour, n.minute, n.second, n.microsecond*1000 ]
    
# return array [ year, months, days, hours, minutes, seconds, nanoseconds ]
# preserving the day of year notation if this was used. See the class
# documentation for allowed time formats, which are a subset of ISO8601
# times.  This also supports "now", "now-P1D", and other simple extensions.
# The following are valid inputs:<ul>
# <li>2021
# <li>2020-01-01
# <li>2020-01-01Z
# <li>2020-01-01T00Z
# <li>2020-01-01T00:00Z
# <li>now
# <li>now-P1D
# <li>lastday-P1D
# <li>lasthour-PT1H
# </ul>
# 
# @param time isoTime to decompose
# @return the decomposed time
# @throws IllegalArgumentException when the time cannot be parsed.
# @see #isoTimeFromArray(int[])
# 
def iso_time_to_array( time ) :
    time= time.strip()
    if (len(time) == 4) :
        result = [ int(time), 1, 1, 0, 0, 0, 0 ]
    elif ( time.startswith("now") or time.startswith("last") ) :
        remainder= None
        if ( time.startswith("now") ) :
            n= now()
            remainder= time[3:]
        else :
            import re
            p= re.compile("last([a-z]+)([\\+|\\-]P.*)?")
            m= p.match(time)
            if m!=None:
                n= now()
                unit= m.group(1)
                remainder= m.group(2)
                if unit=="year":
                    idigit= 1
                elif unit=="month":
                    idigit= 2
                elif unit=="day":
                    idigit= 3
                elif unit=="hour":
                    idigit= 4
                elif unit=="minute":
                    idigit= 5
                elif unit=="second":
                    idigit= 6
                else:
                    raise exception("unsupported unit: "+unit)
                
                if idigit>1: istart=idigit 
                else: istart=1
                for id in xrange( istart, 3 ):
                    n[id]= 1
                
                if idigit>3: istart=idigit
                else: istart=3
                for id in xrange( istart, 7 ):
                    n[id]= 0
                
            else :
                raise exception("expected lastday+P1D, etc")
            
        
        if remainder==None or len(remainder)==0 :
            return n
        elif remainder[0]=='-' :
            return subtract( n, parse_iso8601_duration(remainder[1:]) )
            
        elif remainder[0]=='+' :
            return add( n,  parse_iso8601_duration(remainder[1:]) )
        
        return now()
        
    else :
        if len(time) < 7 :
            raise Exception("time must have 4 or greater than 7 elements")
        
        # first, parse YMD part, and leave remaining components in time.
        if len(time)==7 :
            result = [ int(time.substring[0:4]), int(time[5:7]), 1, # days
                0, 0, 0, 0 ]
            time = ""
        elif len(time) == 8 :
            result = [ int(time[0:4]), 1, int(time[5,8]), # days
                0, 0, 0, 0 ]
            time = ""
        elif time[8] == 'T':
            result = [ int(time[0:4]), 1, int(time[5:8]), # days
                0, 0, 0, 0 ]
            time = time[9:]
        elif (time[8] == 'Z') :
            result =  [ int(time[0:4]), 1, int(time[5:8]), # days
                0, 0, 0, 0 ]
            time = time[9:]
        else :
            result = [ int(time[0:4]), int(time[5:7]), int(time[8:10]), 0, 0, 0, 0 ]
            if len(time) == 10 :
                time = ""
            else :
                time = time[11:]
            
        
        # second, parse HMS part.
        if time.endswith("Z") :
            time = time[0:-1]
        
        if len(time) >= 2 :
            result[3] = int(time[0:2])
        
        if len(time) >= 5 :
            result[4] = int(time[3:5])
        
        if len(time) >= 8 :
            result[5] = int(time[6:8])
        
        if len(time) > 9 :
            import math
            result[6] = int( (math.pow(10, 18 - len(time))) * int(time[9:]) )
        
        normalize_time(result)
    
    return result

#parse the int or return the default value
def parse_int( s, deft ):
    if (s == None):
        return deft;
    else:
        return int(s);

def parse_double( d, deft ):
    if (d == None):
        return deft;
    else:
        return float(s);
    
import re
iso8601_duration = "P((\\d+)Y)?((\\d+)M)?((\\d+)D)?(T((\\d+)H)?((\\d+)M)?((" + "\\d?\\.?\\d+" + ")S)?)?"
iso8601_duration_pattern = re.compile(iso8601_duration)

# 
# returns a 7 element array with [year,mon,day,hour,min,sec,nanos]. Note
# this does not allow fractional day, hours or minutes! Examples
# include:<ul>
# <li>P1D - one day
# <li>PT1M - one minute
# <li>PT0.5S - 0.5 seconds
# </ul>
# TODO: there exists more complete code elsewhere.
# 
# @param stringIn theISO8601 duration.
# @return 7-element array with [year,mon,day,hour,min,sec,nanos]
# @throws ParseException if the string does not appear to be valid.
# @see #iso8601duration
# 
# 
def parse_iso8601_duration(stringIn):
    m = iso8601_duration_pattern.match(stringIn)
    if m!=None :
        dsec = parse_double(m.group(13),0)
        sec = int(dsec)
        nanosec = int((dsec - sec) * 1e9)
        return [ parse_int(m.group(2), 0), parse_int(m.group(4), 0), parse_int(m.group(6), 0),
            parse_int(m.group(9), 0), parse_int(m.group(11), 0), sec, nanosec ]
    else :
        if (stringIn.contains("P") and stringIn.contains("S") and not stringIn.contains("T")) :
            raise Exception("ISO8601 duration expected but not found.  Was the T missing before S?")
        else :
            raise Exception("ISO8601 duration expected but not found.")


# 
# parse the ISO8601 time range, like "1998-01-02/1998-01-17", into
# start and stop times, returned in a 14 element array of ints.
# @param stringIn
# @return the time start and stop [ Y,m,d,H,M,S,N, Y,m,d,H,M,S,N ]
# @throws ParseException
# 
def parse_iso8601_timerange( stringIn ):
    ss = stringIn.split("/")
    if len(ss)!=2 :
        raise Exception("expected one slash (/) splitting start and stop times.")
    
    if ( len(ss[0])==0 or not ( ss[0][0].isDigit() or ss[0][0]=='P' or ss[0].startswith("now") ) ) :
        raise Exception("first time/duration is misformatted.  Should be ISO8601 time or duration like P1D.")
    
    if ( len(ss[1])==0 or not ( ss[1][0].isDigit() or ss[1][0]=='P' or ss[1].startswith("now") ) ) :
        raise Exception("second time/duration is misformatted.  Should be ISO8601 time or duration like P1D.")
    
    result= [None]*14
    if ( ss[0].startswith("P") ) :
        duration= parse_iso8601_duration(ss[0])
        time= iso_time_to_array(ss[1])
        for i in xrange(0,7):
            result[i]= time[i]-duration[i]
        for i in xrange(7,14):
            result[i]= time[i-7]
        return result
    elif ( ss[1].startswith("P") ) :
        time= iso_time_to_array(ss[0])
        duration= parse_iso8601_duration(ss[1])
        for i in xrange(0,7):
            result[i]= time[i]
        for i in xrange(7,14):
            result[i]= time[i-7]+duration[i-7]
        return result
    else :
        starttime= iso_time_to_array(ss[0])
        stoptime=  iso_time_to_array(ss[1])
        for i in xrange(0,7):
            result[i]= starttime[i]
        for i in xrange(7,14):
            result[i]= stoptime[i-7]
        return result
    

#print iso_time_to_array( '2030-04-05T00:11Z' )
#print reformat_iso_time('2030-003T00:00Z','2030-04-05T00:11Z')
print iso_time_to_array('now')
print iso_time_to_array('lasthour-PT1H')
