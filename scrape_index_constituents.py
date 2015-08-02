"""Summary"""
from bs4 import BeautifulSoup
from urllib.request import urlopen

# classes
class HtmlTable():
	"""Represents the contents of a html table in Python.
	
	The data contained in the html table can be represented as a list.
	Instantiated with a bs4.element.Tag object containing a html table.
	
	Dependencies:
		* BeautifulSoup4
		* urllib
	
	Example:
		>>> html_table = HtmlTable(bs4_table)
		>>> result = html_table.get_data_by_col_names(['col1 name', 'col3 name'])
		[['col1 row 1', 'col3 row 1'], ['col1 row 2', 'col3 row 2'], ...]

	"""
	
	def __init__(self, table):
		"""__init__ method of the HtmlTable class.
		
		Note:
			Do not include the `self` parameter in the ``Args`` section.
		
		Args:
			table (bs4.element.Tag): bs4 html object containing a table.

		"""
		self.table = table
		self.col_names = []
		self.col_names = self.get_col_names()
		# UGLY! REMOVE THE NEED FOR THIS
		# BAD
		# BAD!
		# BAD!!
		# BAD!!!
		self.col_name_indices = []

	def get_cell_content(self, col):
		"""Returns the contents of the html table data element as a string.
		
		Args:
		    col (list): Contents of the html table data element <td>content</td>.
		
		Returns:
		    str: Contents of table data element or '' if empty list.

		"""
		# INCLUDE OPTIONS FOR DEEP EXTRACT, EG IF THE TABLE CELL
		# CONTAINS A HREF
		if not col.contents:
			return ''
		else:
			return col.contents[0]

	def get_col_names(self):
		"""Returns a list of column names (th element contents).
		
		Returns:
		    list: Content of <th> elements in a list of strings.

		"""
		if self.col_names:
			return self.col_names
		cols = self.table.findAll('th')
		col_names_raw = list(map(self.get_cell_content, cols))
		self.col_names = list(map(self.strip_str, col_names_raw))
		return self.col_names

	def get_rows(self):
		"""Returns a list of table rows (tr elements).
		
		Returns:
		    list: List of tr elements in the table.

		"""
		return self.table.find('tbody').findAll('tr')

	def get_col_name_index(self, col_name):
		"""Returns the index of a column name (th element).
		
		Args:
		    col_name (str): Column name (contents of a th element).
		
		Returns:
		    int: Index of col_name in list of th elements.

		"""
		col_names_all = self.get_col_names()
		return col_names_all.index(col_name)

	def get_indices_by_col_names(self, col_names):
		"""Returns a list of indices of column names (th elements).
		
		Args:
		    col_names (list): List of column names (contents of th elements).
		
		Returns:
		    list: List if indices of column names in col_names.

		"""
		return list(map(self.get_col_name_index, col_names))
		
	def get_rows_by_index(self, row):
		"""Returns a list of cleaned up table cells for a given row (tr element).
		
		Args:
		    row (bs4.element.Tag): bs4 <tr> html object.
		
		Returns:
		    list: Cleaned up contents of row cells (td elements).

		"""
		# get list of column elements in table row
		data_cols = row.findAll('td')
		row_data = []
		for i in self.col_name_indices:
			row_data.append(self.strip_str(self.get_cell_content(data_cols[i])))
		return row_data

	def get_row_data(self, row):
		"""Returns the cells (td) as items in a list, given a row (tr).
		
		Args:
		    row (bs4.element.Tag): bs4 <tr> html object.
		
		Returns:
		    list: Cleaned up contents of row cells (td elements).

		"""
		data_cells = row.findAll('td')
		cells = list(map(self.get_cell_content, data_cells))
		return list(map(self.strip_str, cells))

	def get_data_by_col_names(self, col_names):
		"""Returns a list of lists of table cells, given a list of column names (th elements).
		
		Example:
			>>> html_table = HtmlTable(bs4_table)
			>>> result = html_table.get_data_by_col_names(['col1 name', 'col3 name'])
			[
				['row1 col1', 'row1 col3'],
				['row2 col1', 'row2 col3'],
				...
			]		

		Args:
		    col_names (list): List of column names (contents of th elements).
		
		Returns:
		    list: List of lists containing cleaned up contents of td elements.

		"""
		# get indices of required columns
		self.col_name_indices = self.get_indices_by_col_names(col_names)
		return list(map(self.get_rows_by_index, self.get_rows()))

	def get_rows_by_col_names(self, col_names):
		"""Returns a list of cleaned up table cells for a given row (tr element).
		
		Args:
		    row (bs4.element.Tag): bs4 <tr> html object
		
		Returns:
		    list: Cleaned up contents of row cells (td elements).

		"""
		# get list of column elements in table row
		data_cols = row.findAll('td')
		return list(map(self.strip_str(self.get_cell_content), data_cols))
		# row_data = []
		# for i in self.col_name_indices:
		# 	row_data.append(self.strip_str(self.get_cell_content(data_cols[i])))
		# return row_data	

	def get_data(self):
		"""Returns a list of lists of all table cells (td elements).
		
		Example:
			>>> html_table = HtmlTable(bs4_table)
			>>> result = html_table.get_data()
			[
				['row1 col1', 'row1 col2', 'row1 col3'],
				['row2 col1', 'row2 col2', 'row2 col3'],
				...
			]		

		Args:
		    col_names (list): List of column names (contents of th elements).
		
		Returns:
		    list: List (rows) of lists (cols) containing cleaned up contents of td elements.
		"""
		return list(map(self.get_row_data, self.get_rows()))		

	def strip_str(self, string):
		"""Strips out whitespace and newlines on either side of string.
		
		Args:
		    string (str): A string.
		
		Returns:
		    str: A cleaned up string.
		"""
		return string.replace('\n','').strip()


# request
# read html
base_url = "http://www.marketindex.com.au"

allords_rel_url = "all-ordinaries"

url = base_url+'/'+allords_rel_url

allords_tableid = 'asx_sp_table'

html = urlopen(url).read() #'http://www.marketindex.com.au/all-ordinaries').read()

soup = BeautifulSoup(html, "lxml")
# find a html table
allords_table = soup.find("table", { "id" : allords_tableid })
# sort through table and put into python list
html_table = HtmlTable(allords_table)

required_col_names = ['Code','Company']
# data_rows = get_data_by_col_names(allords_table, )
result = html_table.get_data_by_col_names(required_col_names)

# print(result)

print(html_table.get_data())

# save data
