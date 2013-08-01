import random
import time
def mydate(format=None,start=None,end=None):
	import datetime, sys
	if format is None:
		format="%m/%d/%Y"
	if start is None:
		start="01/01/1970"
	if end is None:
		now = datetime.datetime.now()
		end=now.strftime("%m/%d/%Y")
	
	return randomDate(start, end, format, random.random())	

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, format, prop):
    return strTimeProp(start, end, format, prop)


def myint(start=None,end=None):
	if start is None:
		start=0
	if end is None:
		end=10

	return random.randint(start,end)

def mybool():
	return bool(random.getrandbits(1))

def mystring(listOfStrings):
	from random import choice
	return choice(listOfStrings)
