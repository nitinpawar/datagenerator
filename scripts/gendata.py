#!/usr/bin/python

import sys, getopt
import functions
import profiler
import array
import random
import string
import multiprocessing as mp
import os
import time

batchappendsize=1000
sep=","
recorddef={}

def main(argv):
   directory=None
   records=None
   inputfile=None
   processes=None
   try:
      opts, args = getopt.getopt(argv,"hi:r:p:d:",["ifile=","records=","processes=","odirectory="])
   except getopt.GetoptError:
      print 'script -i <inputfile> -r records -t threads -d odirectory'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'script -i <inputfile> -r <records>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-r", "--records"):
         records = arg
      elif opt in ("-p", "--processes"):
         processes = arg
      elif opt in ("-d", "--odirectory"):
         directory = arg
   if processes is None:
	processes = 1

   if (inputfile is None) or (records is None) or (directory is None):
	print "One or more options needed"
	print "Usage: -i <inputfile> -r <records per process> -p <number or processes> -d <output directory>"
	sys.exit(1)


   defcols(inputfile)
   manager = mp.Manager()
   q = manager.Queue()    
   pool = mp.Pool(mp.cpu_count() + 2)

    #put listener to work first
   watcher = pool.apply_async(writetofile, (directory,q,)) 

   jobs = []
   for i in range(int(processes)):
       job = pool.apply_async(generatedata, (i,int(records), q))
       jobs.append(job)
    # collect results from the workers through the pool result queue
   for job in jobs: 
       job.get()

    #now we are done, kill the listener
   q.put('KILL')
   pool.close()

def writetofile(directory,q):
	if not os.path.exists(directory):
    		os.makedirs(directory)
	filename=''.join(random.choice(string.lowercase) for x in range(8))
	fo=open(os.path.join(directory, filename), "a+")
	while 1:
		m=q.get()
#		print m
		if m == "KILL":
			print "Done"
		fo.write(m)
		fo.flush()
	fo.close()


def generatedata(tt,records,q):
	totalcols=len(recorddef.keys())
	currentrecord=0
	batchappend=0
	batchappenddata=None
	totalrecords = int(records) 
	for currentrecord in range(0, totalrecords):
		i=0
		batchappend = batchappend + 1
		currentrecord = currentrecord + 1
		recordLine=None
		while (i < totalcols):	
			if recordLine is None:
				recordLine = str(makecall(recorddef[i]["funct"],recorddef[i]["values"], None))
			else:
				dep_on = recordLine.split(sep)[-1]
				recordLine = recordLine + sep + str(makecall(recorddef[i]["funct"],recorddef[i]["values"],dep_on))
			i = i+1
		if (batchappend == totalrecords):
			batchappenddata = batchappenddata + "\n" + recordLine + "\n"
			batchappend = 0
			q.put(batchappenddata)
			return batchappenddata
			batchappenddata=None
			
		elif (batchappend >= 0):
			if batchappenddata is None:
				batchappenddata = recordLine 
			else:
				batchappenddata = batchappenddata + "\n" + recordLine
def defcols(file):
   with open(file) as f:
      i=0
      for line in f:
         recorddef[i]={"funct":None, "values":None} 
	 localcols=line.split("\t")
	 recorddef[i]["funct"]=localcols[1]
	 recorddef[i]["values"]=localcols[len(localcols)-1].strip("\n").split("-")
	 i = i + 1
def makecall(colfunc,values,dep_on):
	if colfunc == "date":
		length=len(values)
		format=None
		start=None
		end=None
		i=0
		while (i < length):
			if i == 0:
				format = values[0]
			if i == 1:
				start = values[1]
			if i == 2:
				end = values[2]
			i = i+1
		return functions.mydate(format,start,end)
	elif colfunc == "int":
		if (values[0] is None) or (values is None):
			start=None
		else:
			start=int(values[0])
		if (values[1] is None) or (values is None):
			end=None
		else:
			end=int(values[1])
		return functions.myint(start,end)
	elif colfunc == "bool":
		return function.mybool()			
	elif colfunc == "string":
		
		return functions.mystring(values)
	elif colfunc == "dependent":
		return functions.dependent(dep_on, values[0], values[1])			
	

if __name__ == "__main__":
   main(sys.argv[1:])
