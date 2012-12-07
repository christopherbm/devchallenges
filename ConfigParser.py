"""

"""

import pickle

class ConfigParser:
	def __init__(
		self, 
		filename='',
		allowableSections=[], 
		allowableKeys=[], 
		sectionContainer='[]', 
		keyDivider=':',
		maxLineLength=50
	):
				
		try:
			# run all initialized values through setters
			self.file = None
			self.setFileName(filename)
			self.setAllowableSections(allowableSections)
			self.setAllowableKeys(allowableKeys)
			self.setSectionContainer(sectionContainer)
			self.setKeyDivider(keyDivider)
			self.setMaxLineLength(maxLineLength)
			self.config = [] # holds config data as associative array / dictionary
		
			# only run parse if filename has been set
			if( self.filename != '' ):
				f = open(filename, 'r')
				self.file = f
			
				# begin parsing
				self.parse()
		
		# errors are passed out of class
		except (IOError, Exception) as e: raise
		
		# always close file
		finally: self.file.close()

	# main
	def parse(self):
		try:
			for line in self.file:
				
				# line is all whitespace
				if line.isspace(): continue
				
				# line is a section header
				elif line[0] == self.sectionContainer[0]:					
					if( self.isSection(line) != True ):
						raise Exception('invalid section name: {0}'.format(line))
			
				# line is part of a long string
				elif line[0] == " ":
					self.addToLastDatum(line)
			
				# line is a key/value pair
				elif type(line[0]) is str:					
					if( self.isKey(line) != True ):
						raise Exception('invalid key name: {0}'.format(line))
					
				# skip line, but do not raise error
				else: continue
				
		except Exception as e: raise
	
	def isSection(self, line):
		section = ''
		for c in line:
			if( c != self.sectionContainer[0] and c!= self.sectionContainer[1] ):
				section += c
		
		section = section.strip()

		# validate section
		if( self.isAllowableSection(section) ):
			self.config.append( [section, []] )			
			return True
		
		return False
		
	def isKey(self, line):
		# split and strip
		kv = line.split(self.keyDivider)
		key = kv[0].strip()
		value = kv[1].strip()
		
		# type casting
		value = self.returnAsType(value)
		
		# add to last item in config
		#keys = self.config.keys()
		if( self.isAllowableKey(key) ):
			self.config[-1][1].append([key, value])
			return True
			
		return False
			
	def addToLastDatum(self, line):
		# strip line and concatenate with last value
		self.config[-1][-1][-1][-1] += ' '
		self.config[-1][-1][-1][-1] += line.strip()
	
	# checks if value contains characters or space (except for '.')
	def returnAsType(self, value):
		try:
			if( value.find(" ") != -1 ):
				return str(value)
	
			containsAlpha = False
			for c in value:
				if( c.isalpha() and c != '.' ):
					containsAlpha = True
					break
				break
			
			if(containsAlpha):
				return str(value)
		
			elif value.find(".") != -1:
				return float(value)
			
			else:
				return int(value)
				
		except ValueError as error:
			return value
	
	def isAllowableSection(self, section):
		if( len(self.allowableSections) == 0) : return True
		else:
			if( section in self.allowableSections ): return True
			else: return False
		
		return False
		
	def isAllowableKey(self, key):
		if len(self.allowableKeys) == 0: return True
		else:
			if key in self.allowableKeys: return True
			else: return False
		
		return False
	
	def writeConfig(self):
		try:
			el = '\r\n'
			so = self.sectionContainer[0]
			sc = self.sectionContainer[1]
			kd = self.keyDivider + ' '
			
			self.file = open(self.filename, 'w')
			for sec in self.config:
				self.file.write(so + sec + sc + el)
				
				for k,v in self.config[sec].iteritems():
					v = str(v)
					
					# if it is a long string, split and write line by line
					if( len(v) > self.maxLineLength ):
						self.file.write(k + kd)
						lines = self.splitLine(v)
						for line in lines:
							self.file.write(' ' + line + el)
						
					else:
						self.file.write(k + kd + v + el)
					
				self.file.write(el)
				
			return True
		
		# all exceptions are passed out
		except (IOError, Exception) as e: raise
		
		# always close file
		finally:
			self.file.close()
	
	def splitLine(self, line):
		count = 0
		lines = []
		nl = ''

		words = line.split(" ")
		for word in words:
			l = len(word)
			if( count + l <= self.maxLineLength ):
				count = count + l
				nl += word + ' '
			else:
				lines.append(nl)
				count = 0
				nl = ''
				
		# make sure to grab the last words
		lines.append(nl)
		
		return lines
	
	def setFileName(self, filename):
		if( self.file != None ):
			self.file.close()
			self.file = None
			
		self.filename = filename
		
	def getFileName(self): return self.filename	
	
	def setAllowableKeys(self, keys):
		if( type(keys) != list ):
			raise Exception('Allowable Keys must be of type List')
			return
		
		self.allowableKeys = keys
		
	def getAllowableKeys(self): return self.allowableKeys
	
	def setAllowableSections(self, sections):
		if( type(sections) != list ):
			raise Exception('Allowable Sections must be of type List')
			return
		
		self.allowableSections = sections
	
	def getAllowableSections(self): return self.allowableSections
	
	def setKeyDivider(self, key):
		if( type(key) != str ):
			raise Exception('Key Divider must be of type String')
			return
		
		if( len(key) != 1 ):
			raise Exception('Key Divider format must be ":" (only one char)')
			return
			
		self.keyDivider = key
		
	def getKeyDivider(self): return self.keyDivider
	
	def setSectionContainer(self, container):
		if( type(container) != str ):
			raise Exception('Section Container must be of type String')
			return
			
		if( len(container) != 2 ):
			raise Exception('Section Container format must be "[]" (only two chars)')
			return
			
		self.sectionContainer = container
			
	def getSectionContainer(self): return self.sectionContainer
	
	def setMaxLineLength(self, length):
		if( type(length) != int ):
			raise Exception('Max Line Length must be of type int')
			return
			
		self.maxLineLength = length
		
	def getMaxLineLength(self): return self.maxLineLength
	
	def setConfigValue(self, section, key, value):
		try:
			if( self.isAllowableSection(section) != True ):
				raise Exception('invalid section name: {0}'.format(section))
				
			if( self.isAllowableKey(key) != True):
				raise Exception('invalid key name: {0}'.format(key))
				
			self.config[section][key] = value
			
			return True
			
		except Exception as e:
			raise e
	
	def getConfigValue(self, section, key):
		try:
			value = self.config[section][key]
			return value
			
		except KeyError as e:
			raise e
		
	def getCount(self):
		keyCount = 0
		for sec, keys in self.config.iteritems():
			keyCount = keyCount + len(keys)
			
		return [ len(self.config), keyCount ]
	
	def getConfig(self): return self.config
	
	def getSerializedConfig(self):
		try:
			return pickle.dumps(self.config)
		
		except Exception as e: raise


def test():
	try:
		p = ConfigParser('config.txt')
		#p.set('header', 'project', 'New Problem')
		#print p.get('header', 'Project')
		print p.config
		#v =  p.get('header', 'budget')
		#print v
		#print type(v)
		#print p.getCount()
		
		#p.filename = 'config2.txt'
		#p.writeConfig()
		
		#print p.getSerializedConfig()
		
	except (IOError, KeyError, Exception) as e:
		print e, e.args

if __name__ == '__main__':
    test()