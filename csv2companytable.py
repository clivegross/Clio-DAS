#!/usr/bin/python
# 
# csv2companytable.py
# Clive Gross, Oct 2013
# 
# Usage:
# python csv2companytable.csv 'csvfile'
# 
# Takes a command-line argument as the input csv filename,
# reads in each row of the csvfile and inserts it into the
# clio.Company table if the company symbol is not already
# in the table. The csvfile must be in the format:
# 	c1_symbol,c1_name
# 	c2_symbol,c2_name
# 	c3_symbol,c3_name...

import csv
import MySQLdb
import sys

# Define filename of csv file
csvfile = sys.argv[1]
#csvfile = 'AORD2013.csv'

# Get password value
password = open('/home/pi/pword').read().split('\n')[0]

# Open database connection
db = MySQLdb.connect("localhost","clio",password,"clio" )

# Prepare a cursor object using cursor() method
cursor = db.cursor()

# Open csv and insert each record into Company table if not exists
with open(csvfile, 'rb') as infile:
	reader = csv.reader(infile)
	for row in reader:
		# Query to select from table Symbol if exists
		select_query = "SELECT Symbol FROM Company \
		WHERE Symbol = '%s'" % \
		row[0]
		# Execute query
		cursor.execute(select_query)
		# Fetch a matching symbol using fetchone() method
		existing_record = cursor.fetchone()
		# If record does not exist, insert row
		if existing_record is None:
			# Query to INSERT a record into the Company table
			insert_query = 'INSERT INTO Company(symbol,name) \
			VALUES("%s","%s")' % \
			(row[0],row[1])
			# Try insert record, rollback if fails
			try:
				# Execute the SQL command
				cursor.execute(insert_query)
				# Commit your changes in the database
				db.commit()
				print row[0]+" inserted into Company table"
			except:
				# Rollback if there is any error
				db.rollback()
				print "Failed to insert record, rolling back"
		else:
			# If record does exist, inform user
			print "Record already exists, skipping"

# disconnect from server
cursor.close()