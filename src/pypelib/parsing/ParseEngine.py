import os
import sys
import time
import uuid

'''
        @author: msune,lbergesio,cbermudo,omoya
	@organization: i2CAT, OFELIA FP7

	ParseEngine	
	Implementes driver-based parsing mechanism for rules
'''


class ParseEngine():

	#Drivers
	_drivers = ["RegexParser"]
	_defaultDriver = 'RegexParser'


	#Fill with appropiate path
	PATH_TO_DRIVERS="drivers"
	
	def __init__(self):
		raise Exception("Static class cannot be instanciated")	

	@staticmethod
	def _getDriver(driverName=None):
		if driverName == None or driverName not in ParseEngine._drivers:
			#TODO: Try all drivers?
			raise Exception("Cannot find parser")
	
		elif driverName == "RegexParser":

			path = '.' + ParseEngine.PATH_TO_DRIVERS + '.RegexParser'
			exec('from ' + path + ' import RegexParser') 
			#from ParseEngine.PATH_TO_DRIVERS.RegexParser import RegexParser
			return RegexParser
				
	@staticmethod
	def parseRule(string, driverName= _defaultDriver):
		return ParseEngine._getDriver(driverName).parseRule(string)

	@staticmethod
	def craftRule(rule, driverName=None):
		return ParseEngine._getDriver(driverName).craftRule(rule)

# This calls should not be here. Instead, use parseRule in the persistence drivers if required.
#	@staticmethod
#	def parseCondition(stringCond, driverName=None):
#		return ParseEngine._getDriver(driverName)._parseCondition(stringCond)
#	
#	@staticmethod
#	def craftCondition(condition, driverName=None):
#		return ParseEngine._getDriver(driverName).craftCondition(condition)


