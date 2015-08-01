from bs4 import BeautifulSoup
from urllib2 import urlopen

base_url = "http://www.marketindex.com.au"

allords_rel_url = "all-ordinaries"

url = base_url+'/'+allords_rel_url

print(url)

html = urlopen('http://www.marketindex.com.au/all-ordinaries').read()

soup=BeautifulSoup(html, "lxml")
soup.find("table", "asx_sp_table")
