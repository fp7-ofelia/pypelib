import os
import sys
import time
from cPickle import loads, dumps

from src.RuleTable import RuleTable


class RAWFile():

	def __intit__(self):
		raise Exception("Static class cannot be instanciated")

	@staticmethod
	def saveRuleTable(obj):

		File = open('src/persistence/drivers/rawFile/RuleTableFile.dat','a')
		File.close()
		if RAWFile.findRuleTable(obj):
			File.close()
			return	
		else:
			File = open('src/persistence/drivers/rawFile/RuleTableFile.dat','a')
			File.write('#uuid:\n')
	                File.write(obj.uuid)
			File.write('\n#Name:\n')
			File.write(obj.name)
			File.write('\n#Mappings:\n')
       		        File.write(str(obj._mappings))
			File.write('\n#Parser:\n')
        	        File.write(obj._defaultParser)
			File.write('\n#Persistence:\n')
               		File.write(obj._defaultPersistence)
			File.write('\n#PersistenceFlag:\n')
                	File.write(str(obj._defaultPersistenceFlag))
			File.write('\n#PolicyType:\n')
               		File.write(str(obj._policy))
          	        File.write('\n$$$$$')
			File.write('\n#RuleSet:\n')
			File.write(RAWFile.setRuleSet(str(dumps(obj._ruleSet))))
               		#File.write(str(dumps(obj._ruleSet)))
               		File.write('\n#####\n')
			File.close()

	@staticmethod
	def loadRuleTable(tableName):
		File = open('src/persistence/drivers/rawFile/RuleTableFile.dat','r')
		auxFile = open('src/persistence/drivers/rawFile/RuleTableFile.dat','r')
		EntireFile = auxFile.readlines()
		auxFile.close()
		lst = []
		line = 0	
		while True:
		
			text = File.readline()
			line += 1
			if str(text) == str(tableName) + '\n':
				lst.append(text)
				
				while True:
					text = File.readline()
					if text[0] =="#":
						pass
						#text = File.readline()
					elif text[0] == "$":
						File.close()
						lst = RAWFile.cleanRuleTableParameters(lst)
						ruleTable = RuleTable(lst[0],eval(lst[1]),lst[2],lst[3],lst[4],lst[5],int(EntireFile[line-3]),True)
						ruleTable.loadRuleSet()
						ruleTable.dump()
						return ruleTable
					else:
						lst.append(text)
						#text = File.readline
			elif text == "":
				File.close()
				raise Exception("Could not load this Rule Table")

	@staticmethod
	def loadRuleSet(obj):
		File = open('src/persistence/drivers/rawFile/RuleTableFile.dat','r')
		
		ruleSet = ""
		text = ""
		
		while True:
			text = File.readline()
			if text == str(obj) + '\n':
				while True:
					if text == "$$$$$\n":
						while True:
							text = File.readline()
							if text == '#RuleSet:\n':
								pass
							elif text == '#####\n':
								File.close()
								return loads(RAWFile.reSetRuleSet(ruleSet))

							else:
								ruleSet += text

					text = File.readline()
			elif text == "":

				return None

		
	@staticmethod
	def setRuleSet(obj):
		dumps = obj.replace('\n','%%%')
		return dumps
	@staticmethod
	def reSetRuleSet(string):
		loads = string.replace('%%%','\n')
		return loads

	@staticmethod
	def cleanRuleTableParameters(lst):
		lstout = list()
		for param in lst:
			lstout.append(param.replace('\n',''))
		return lstout		
