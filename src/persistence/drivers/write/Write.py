import os
import sys
import time
from cPickle import loads, dumps

from RuleTable import RuleTable


class Write():

	def __intit__(self):
		raise Exception("Static class cannot be instanciated")

	@staticmethod
	def saveRuleTable(obj):

		print 'saveRuleTable'
		print obj.uuid		
		File = open('persistence/drivers/write/RuleTableFile.dat','a')
		File.close()
		if Write.findRuleTable(obj):
			print 'True'
			print obj.uuid
			File.close()
			return	
		else:
			print 'False'
			File = open('persistence/drivers/write/RuleTableFile.dat','a')
			print obj.uuid
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
			File.write(Write.setRuleSet(str(dumps(obj._ruleSet))))
               		#File.write(str(dumps(obj._ruleSet)))
               		File.write('\n#####\n')
			print File.tell()
			File.close()

	@staticmethod
	def findRuleTable(obj):
		File = open('persistence/drivers/write/RuleTableFile.dat','r+')
		print 'while'
		print obj
#		while True:
#			text = File.readline()
#			print str(text) == str(obj.uuid)+'\n'
#			if str(text) == str(obj.uuid)+'\n':
#				text = File.readline()
#				print 'text == uuid'
#                        	File.write(obj.name)
 #                       	File.write('\n#Mappings:\n')
  #                      	File.write(str(obj._mappings))
   #                     	File.write('\n#Parser:\n')
    #                    	File.write(obj._defaultParser)
     #                   	File.write('\n#Persistence:\n')
      #                	 	File.write(obj._defaultPersistence)
       #                 	File.write('\n#PersistenceFlag:\n')
        #                	File.write(str(obj._defaultPersistenceFlag))
         #               	File.write('\n#PolicyType:\n')
          #              	File.write(str(obj._policy))
           #             	File.write('\n$$$$$')
            #            	File.write('\n#RuleSet:\n')
	#			File.write(Write.setRuleSet(str(dumps(obj._ruleSet))))
         #               	File.write('\n#####\n')
          #              	File.close()
	#			return True
	#		elif text == "":
	#			print 'break!!'
	#			File.close()
	#			return 	False
	
		i = 0
		lst = File.readlines()
		File.seek(0)
		while i < len(lst):
			if lst[i] == obj.uuid + '\n':
				lst[i+2] = str(obj.name) + '\n'
				lst[i+4] = str(obj._mappings) + '\n'
				lst[i+6] = str(obj._defaultParser) + '\n'
				lst[i+8] = str(obj._defaultPersistence) + '\n'
				lst[i+10] = str(obj._defaultPersistenceFlag) + '\n'
				lst[i+12] = str(obj._policy) + '\n'
				lst[i+15] = Write.setRuleSet(str(dumps(obj._ruleSet))) + '\n'
				File.writelines(lst)
				File.truncate()
				File.close()
				print 'liiiiiiiiiiiiiiiiiiiiiiiiiiist', lst
				return True
			i += 1
		File.close()
		return False
	@staticmethod
	def loadRuleTable(tableName):
		File = open('persistence/drivers/write/RuleTableFile.dat','r')
		auxFile = open('persistence/drivers/write/RuleTableFile.dat','r')
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
					print text[0]
					print lst 
					if text[0] =="#":
						pass
						#text = File.readline()
					elif text[0] == "$":
						File.close()
						print 'close'
						lst = Write.cleanRuleTableParameters(lst)
						ruleTable = RuleTable(lst[0],eval(lst[1]),lst[2],lst[3],lst[4],lst[5],int(EntireFile[line-3]),True)
						ruleTable.loadRuleSet()
						ruleTable.dump()
						return ruleTable
					else:
						print 'append'
						lst.append(text)
						#text = File.readline
			elif text == "":
				File.close()
				raise Exception("Could not load this Rule Table")

	@staticmethod
	def loadRuleSet(obj):
		File = open('persistence/drivers/write/RuleTableFile.dat','r')
		
		ruleSet = ""
		text = ""
		
		while True:
			text = File.readline()
			print text
			print obj
			if text == str(obj) + '\n':
				while True:
					if text == "$$$$$\n":
						while True:
							text = File.readline()
							print text
							if text == '#RuleSet:\n':
								pass
							elif text == '#####\n':
								print 'RuleSET:',ruleSet
								print Write.reSetRuleSet(ruleSet)
								File.close()
								return loads(Write.reSetRuleSet(ruleSet))

							else:
								ruleSet += text

					text = File.readline()
			elif text == "":

				return None

		
	@staticmethod
	def setRuleSet(obj):
		print obj
		dumps = obj.replace('\n','%%%')
		return dumps
	@staticmethod
	def reSetRuleSet(string):
		loads = string.replace('%%%','\n')
		print loads
		return loads

	@staticmethod
	def cleanRuleTableParameters(lst):
		lstout = list()
		for param in lst:
			lstout.append(param.replace('\n',''))
		return lstout
		
		
