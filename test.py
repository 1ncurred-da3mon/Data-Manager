from dataman import *

if __name__ == '__main__':
	# create a TSVFile Object
	tf = TSVFile('test.tsv')
	
	# Print the TSV File formatted output
	print(tf)

	# Diagnostics object
	dt = Diagnostics()
	
	# elements in the table should amount to 4 elements per line
	dt.add_pref('fixed-element-count', 4)

	# first column should match a username
	dt.add_pref('pattern-match-col', (0, '([a-zA-Z]+ [a-zA-Z]+)'))

	# save the report 
	report = dt.diagnose(tf)

	#print the report
	print(report)