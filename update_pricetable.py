#!/usr/bin/python
# 
# update_pricetable.py
# Clive Gross, Oct 2013
# 
# Usage:
#
# Fetches intraday prices from Yahoo Finance for each company
# in company table and updates price table
import MySQLdb
import urllib2
import datetime as dt

# Get Yahoo Finance API URL from yahoo_url.txt
url_template = open('yahoo_url.txt').read().split('\n')[0]
url_template = "http://chartapi.finance.yahoo.com/instrument/1.0/[TICKER]/chartdata;type=quote;range=[DAYS]d/csv"

# Get password value
password = open('/home/pi/pword').read().split('\n')[0]

# Open database connection
db = MySQLdb.connect("localhost","clio",password,"clio" )

# Prepare a cursor object using cursor() method
cursor = db.cursor()

# Query to select all IDs from Company table
select_query = 'SELECT id FROM Company'

# Execute query
cursor.execute(select_query)

# Fetch all Company IDs from table and convert from tuple to list of integers
cids = cursor.fetchall()
cids = [int(row[0]) for row in cids]
N = len(cids)

# Initialise log file
with open('insert.log','w') as logfile:
	# Loop through company list, pull Yahoo Finance quotes and insert into Price table
	for n,cid in enumerate(cids):
		# Query to select symbol
		select_query = 'SELECT symbol \
		FROM Company \
		WHERE id = "%d"' \
		% cid
		# Execute query
		cursor.execute(select_query)
		# Fetch all Company IDs from table and convert from tuple to list of integers
		symbol = cursor.fetchone()[0]
		# ASX exchange code for Yahoo
		exchange = 'AX'
		# Ticker symbol in correct format for API, ie SYMBOL.EXCHANGE
		ticker = symbol+'.'+exchange
		# Define URL for company price data
		url = url_template.replace('[TICKER]',ticker).replace('[DAYS]','5')

		# Get company price data from URL
		response = urllib2.urlopen(url).readlines()

		# Trim off unrequired data
		for i,element in enumerate(response):
			if element.find('volume:') > -1:
				j = i
				break
	
		response = response[j+1:]

		# Parse string response into useful list of data
		quotes = list()
		for element in response:
			quote = element.split(',')
			quote[0] = dt.datetime.fromtimestamp(int(quote[0]))
			quotes.append(quote)

		# For each timestamp, if it doesnt already exist for Company in Price table, insert quote
		for quote in quotes:
			# Insert into table
			existing_query = 'SELECT utctimestamp \
			FROM Price \
			WHERE companyid = "%s" \
			AND utctimestamp = "%s"' \
			% (cid,quote[0])
			# Execute query
			cursor.execute(existing_query)
			# Fetch a matching symbol using fetchone() method
			existing_record = cursor.fetchone()
			# INSERT record if doesnt exist
			if existing_record is None:
				# Query to INSERT a record into the Company table
				insert_query = 'INSERT INTO Price(companyid,utctimestamp,close,high,low,open,volume) \
				VALUES("%s","%s","%s","%s","%s","%s","%s")' % \
				(cid,str(quote[0]),quote[1],quote[2],quote[3],quote[4],quote[5])
				# Try insert record, rollback if fails
				try:
					# Execute the SQL command
					cursor.execute(insert_query)
					# Commit your changes in the database
					db.commit()
					# print row[0]+" inserted into Company table"
				except:
					# Rollback if there is any error
					db.rollback()
					# print "Failed to insert record, rolling back"
			# else:
				# If record does exist, inform user
				# print "Record already exists, skipping"
		print str(n)+' of '+str(N)+': Updated company '+symbol+', '+str(int(n*1.0/N*100))+'% complete'
		# Write stock insert time into logfile
		logfile.write('Update %d%% complete: %s quotes inserted at %s UTC\n' % (n*100.0/N,symbol,dt.datetime.today()))


# disconnect from server
cursor.close()
