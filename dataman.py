import collections as collection
import numpy
import re

class TSVFile:
	'''
		Easy to acquire data with TSV files.
	'''
	def __init__(self, file=str()):
		self.file = file   # file location of the TSV File
		self.data = list() # list containing all the data in the TSV File
		self.assorted_data = dict() # dictionary containing all variables matched with the first corresponding labels/titles in the first row of elements

		# if the file paramter is not an empty string
		if not self.file == '':
			# parse all the data in the file
			self.parse_file(self.file)
	
	def parse_file(self, file: str)-> None:
		'''
			Parse all the data in the CSV File and store the data into the data member
		'''
		if file != self.file:
			# if the file does not match the file memeber, the file member will be replaced
			self.file = file
		
		with open(self.file, 'r') as f:
			for line in f.readlines():
				# loop through the lines of the file, and store the data into the data member
				self.data.append( line.rstrip().split('\t') )
				
	
	def look_at(self, idx: int)-> str:
		'''
			Look at data of a line. Uses the line's key
		'''
		if idx < 0 or idx >= len(self.data):
			return ''
		else:
			return ' -> '.join(self.data[idx])

	def peek(self, idx: int)-> str:
		# alternative to look_at
		return self.look_at(idx)

	def add_at(self, idx: int, nvar)-> bool:
		'''
			If the user prefers to add to a line via function rather than manually (modifying the data member)
		'''
		if idx < 0 or idx >= len(self.data):
			return False
		else:
			self.data[idx].append(nvar)
			return True
	def add(self, idx: int, nvar)-> bool:
		return self.add_at(idx, nvar)
	
	def write_tsv(self)-> bool:
		try:
			with open(self.file, 'w') as f:
				for line in self.data:
					for i in range(len(line)):
						f.write(line[i])
						if not i == len(line) - 1:
							f.write('\t')
					f.write('\n')
			return True
		except Exception as e:
			print("Error writing to file.")
			print(f"Error: {e}")
			return False

	def save(self)-> bool:
		return self.write_tsv()
	
	def write(self)-> bool:
		return self.write_tsv()

	def __str__(self):
		formatted_len = list()  # formatted length for all variables
		longest_line = -1       # longest line of variables from the TSV file
		res = str()
		# find the longest line in the tsv file
		for i in range(len(self.data)):
			if len(self.data[i]) > longest_line:
				longest_line = i
		
		for i in range(len(self.data[longest_line])):
			formatted_len.append(-1)
			for j in range(len(self.data)):
				try:
					if formatted_len[i] < len(self.data[j][i]):
						formatted_len[i] = len(self.data[j][i])
				except IndexError:
					continue
		
		for line in self.data:
			for i in range(len(line)):
				res += '  {0:<{1}}'.format(line[i], formatted_len[i])
				#print(f'%{formatted_len[i]}s' % line[i], end='')
				if i != len(line) - 1:
					#print(' : ')
					res += ' || '
			#print() # add a new line
			res += '\n'
		return res



class Diagnostics:
	def __init__(self):
		self.preferences = dict()


	def diagnose(self, obj)-> str():
		report = str()
		# clear the report if there was a previous one

		for pref in self.preferences.keys():
			if pref == 'fixed-element-count':
				if not type(self.preferences[pref]) ==  int:
					report += "FIXED-ELEMENT-COUNT must be an integer"
					break
				elif self.preferences[pref] < 0:
					report += "FIXED-ELEMENT-COUNT cannot interact with negative values"
					break
				else:
					report += 'Fixed Element Count Diagnosis: TYPE: '
					if type(obj) is TSVFile:
						report += 'TSV File\n\n'
						fileline = 1
						for data in obj.data:
							counter = len(data)
							if counter > self.preferences[pref] or counter < self.preferences[pref]:
								report += f'line {fileline}! line contains {counter} elements! line: {fileline}\n'
							else:
								report += f'line {fileline} OK\n'
							fileline += 1
					report += '  =========\n\n'
			elif pref == 'match-pattern':
				if not type(self.preferences[pref]) == list:
					report += 'MATCH-PATTERN must be a list of regex strings.'
					break
				else:
					report += 'Pattern Matching Diagnosis: TYPE: '

			elif pref == 'pattern-match-col':
				if type(self.preferences[pref]) != list and type(self.preferences[pref]) != tuple:
					report += 'PATTERN-MATCH-COL must be a list or tuple. Example: (int, regex)'
					break
				else:
					report += "Column Pattern Match Diagnosis: TYPE: "
					if type(obj) is TSVFile:
						report += 'TSV File\n\n'
						col_idx = self.preferences[pref][0]
						regex = self.preferences[pref][1]
						report += f"Must match pattern: {regex}\n\n"

						fileline = 1
						for line in obj.data:
							if re.fullmatch(regex, line[col_idx]) != None:
								report += f"Line {fileline}, Col {col_idx}; OK\n"
							else:
								report += f"Line {fileline}, Col {col_idx}; Failed! ;  \"{line[col_idx]}\"\n"
							fileline += 1
					report += '  ========\n\n'
			elif pref == 'find-common':
				try:
					if not type(self.preferences):
						pass
				except TypeError as e:
					pass

		report += 'END OF REPORT'
		return report

	def add_pref(self, preference_title: str, details)-> None:
		self.preferences[preference_title]=details
	
	def rem_pref(self, preference_title: str)-> None:
		if preference_title in self.preferences:
			self.preferences.popitem(preference_title)
		else:
			print(f"No such preference called '{preference_title}'")
	def set_pref(self, pref_obj: dict)-> None:
		'''
			Set the preferences member of this class to the prefernce that is passed
		'''
		self.preferences = pref_obj

	def __str__(self):
		r = str()
		for pref in self.preferences.items():
			r += pref[0] + ': ' + pref[1] + '\n'
		return r