import random
import time
import datetime, sys
def mydate(format=None,start=None,end=None):
	if format is None:
		format="%m/%d/%Y"
	if start is None:
		start="01/01/1970"
	if end is None:
		now = datetime.datetime.now()
		end=now.strftime("%m/%d/%Y")
	
	return randomDate(start, end, format, random.random()).strip("\"")	

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

def myfloat(start=None, end=None):
	if start is None:
		start = 0.0
	if end is None:
		end = 10.0

	return round(random.uniform(start,end),2)

def mybool():
	return bool(random.getrandbits(1))

def mystring(listOfStrings):
	from random import choice
	return choice(listOfStrings)
def myonedate(myDay, months, years,format):
	startMonth=months.split("-")[0]
	endMonth=months.split("-")[1]
	startYear=years.split("-")[0]
	endYear=years.split("-")[1]
	
	myMonth=myint(int(startMonth), int(endMonth))
	myYear=myint(int(startYear), int(endYear))
	import datetime
	mydate=datetime.date(myYear, myMonth, int(myDay))
	return mydate.strftime(format).strip("\"")
	

def dependent(dep_on,funct,values):
	import json
	if (funct == "map"):
		obj = json.loads(str(values))
		return obj[dep_on]
	if (funct == "date"):
		obj = json.loads(str(values))
		todo = obj["todo"]
		format = obj["format"]
		old_date=datetime.datetime.strptime(dep_on.strip("\""), format)
		if (todo == "add_days"):
			toby=int(obj["by"])
			new_date=old_date + datetime.timedelta(days=toby)
			return new_date.strftime(format)
		elif (todo == "getMonth"):
			return old_date.month
		elif (todo == "getYear"):
			return old_date.year
