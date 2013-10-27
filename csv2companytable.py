#!/usr/bin/python

import csv
import MySQLdb

csvfile = 'AORD2013.csv'
# Open database connection
db = MySQLdb.connect("localhost","clio","dickbum69","clio" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Open csv and insert each record to Company table if not exists
with open(csvfile, 'rb') as infile:
	reader = csv.reader(infile)
	for row in reader:
		# execute SQL query using execute() method.
		select_query = "SELECT Symbol FROM Company \
		WHERE Symbol = '%s'" % \
		row[0]
		cursor.execute(select_query)
		# Fetch a matching symbol using etchone() method.
		existing_record = cursor.fetchone()
		# If record does not exist
		if existing_record is None:
			# SQL query to INSERT a record into the Company table
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
				# Rollback in case there is any error
				db.rollback()
				print "Failed to insert record, rolling back"
		else:
			print "Record already exists, skipping"

# disconnect from server
cursor.close()