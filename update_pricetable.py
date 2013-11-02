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

# Query to select symbol
select_query = "SELECT symbol FROM Company \
WHERE id = 82"

# Execute query
cursor.execute(select_query)

# Fetch a matching symbol using fetchone() method
symbol = cursor.fetchone()[0]
# symbol = 'MYR'
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
for period in response:
	quote = period.split(',')
	quote[0] = dt.datetime.fromtimestamp(int(quote[0]))
	quotes.append(quote)

