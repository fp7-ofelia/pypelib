import os
import sys
import time

'''
        @author: msune

	ParseEngine	
	Implementes driver-based parsing mechanism for rules
'''


class PersistenceEngine():

	#Default Class Attributes
	_defaultParser = "RegexParser"
        _defaultPersistence = "Django"

	#Drivers
	_drivers = ["Django","RAWFile"]

	#Fill with appropiate path
	PATH_TO_DRIVERS="drivers"
	
	def __init__(self):
		raise Exception("Static class cannot be instanciated")	

	@staticmethod
	def _getDriver(driverName):
		#Trying to deduce driver
		#if driverName == None and obj._defaultPersistenceDriver:
		#	try:
		#		driverName = obj._defaultPersistenceDriver
		#	except:
		#		#raise Exception (" Could not")
		#if driverName == None or driverName not in PersistenceEngine._drivers:
		#	#TODO: Try all drivers?
		#	raise Exception("Cannot find persistence driver")
	
		#elif driverName == "Django":
		#	PATH = '.' + PersistenceEngine.PATH_TO_DRIVERS + '.django.Django'
		#	exec('from ' + PATH + ' import Django')
		#	#from drivers.django.Django import *
		#	return Django
		
		if driverName == "Django":
			PATH = '.' + PersistenceEngine.PATH_TO_DRIVERS + '.django.Django'
			try: 
				exec('from ' + PATH + ' import Django')
				return Django
			except:
				Exception(driverName + ' persistence driver not found in ' + PersistenceEngine.PATH_TO_DRIVERS)
		elif driverName == "RAWFile":
			PATH = '.' + PersistenceEngine.PATH_TO_DRIVERS + '.rawFile.RAWFile'
			try:
				exec('from ' + PATH + ' import RAWFile')
				return RAWFile
			except:
				Exception(driverName + ' persistence driver not found in ' + PersistenceEngine.PATH_TO_DRIVERS)
		
	@staticmethod
	def save(obj, parser = _defaultParser, persistence = _defaultPersistence):
		return PersistenceEngine._getDriver(persistence).save(obj, parser)
	
	@staticmethod
	def load( parser = _defaultParser, persistence = _defaultPersistence):
		return PersistenceEngine._getDriver(persistence).load(parser)

	@staticmethod
        def saveRuleTable(obj, persistence = _defaultPersistence):
                return PersistenceEngine._getDriver(persistence).saveRuleTable(obj)
	@staticmethod
	def loadRuleTable(obj,auxuuid = None, persistence = _defaultPersistence):
		return PersistenceEngine._getDriver(persistence).loadRuleTable(obj, auxuuid)
	@staticmethod
        def loadRuleSet(uuid, persistence = _defaultPersistence):
		return PersistenceEngine._getDriver(persistence).loadRuleSet(uuid)
