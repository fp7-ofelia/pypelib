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
	def save(obj, pBackend, parser=None, **kwargs):
		return PersistenceEngine._getDriver(pBackend).save(obj, parser, kwargs)
	
	@staticmethod
	def load(tableName, pBackend, parser=None, **kwargs):
		return PersistenceEngine._getDriver(pBackend).load(tableName, parser, kwargs)
