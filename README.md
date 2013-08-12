datagenerator
=============

datagenerator


Its a random data generator using gendata.py. Soul purpose of having this 
is make it easy to generate large scale data with ease. There are a lot of
online tools available but none of the tools could give me 100M records 
generated for my testing purposes. 
I have done performance tests and for me with a 8 core CPU it took 30 minutes 
to generate 10M records with each record being 30 random columns. This can be 
improveda a lot. I will do it once I get some free time.

Input parameters:
	-i <inputfile> [[ this file holds the table definition ]]
	-r <records per process>  [[ how many records per process ]]
	-p <number or processes> [[ total processes to be launched ]]
	-d <output directory> [[ directory to store the output file ]]

There is an example of inputfile inside the scripts directory. 
Its a simple tab(\t) separated file where first column is column name.
Second column is datatype for the column and third column is data related 
information like format and range etc 

Currently it supports only date, int and string datatypes, feel free to add any more in 
functions.py and then invoke it via makecall() in main file

A special function "dependent" is added which generates 
dependent values based on some other column. 
Format for dependent function is 
columnname<tab>dependent<tab>function-{values for functions and subfunction}<tab><column on which dependent>
Column on which dependent is the # of column starting first column ranked 0

date function has three subfunctions
	addDays
	getMonth
	getYear
map function basically maps the keys with values
