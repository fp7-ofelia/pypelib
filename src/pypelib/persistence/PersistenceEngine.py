import os
import sys
import time

'''
        @author: msune,omoya,CarolinaFernandez
	@@organization: i2CAT, OFELIA FP7

	Persistence engine	
	Implementes driver-based persistence backend selection 
'''


class PersistenceEngine():

	#Default Class Attributes
	_defaultParser = "RegexParser"
        _defaultPersistence = "Django"

	#Drivers
	_drivers = ["Django","RAWFile","SQLAlchemy"]

	#Fill with appropiate path
	PATH_TO_DRIVERS="backends"
	
	def __init__(self):
		raise Exception("Static class cannot be instanciated")	

	@staticmethod
	def _getDriver(driverName):
		if driverName == "Django":
			PATH = PersistenceEngine.PATH_TO_DRIVERS + '.django.Django'
			try: 
				exec('from ' + PATH + ' import Django')
				return Django
			except:
				raise Exception(driverName + ' persistence driver not found in ' + PersistenceEngine.PATH_TO_DRIVERS)
		elif driverName == "RAWFile":
			PATH = PersistenceEngine.PATH_TO_DRIVERS + '.rawfile.RAWFile'
			try:
				exec('from ' + PATH + ' import RAWFile')
				return RAWFile
			except:
				raise Exception(driverName + ' persistence driver not found in ' + PersistenceEngine.PATH_TO_DRIVERS)
		elif driverName == "SQLAlchemy":
			PATH = PersistenceEngine.PATH_TO_DRIVERS + '.sqlalchemy.SQLAlchemy'
			try:
				exec('from ' + PATH + ' import SQLAlchemy')
				return SQLAlchemy
			except:
				raise Exception(driverName + ' persistence driver not found in ' + PersistenceEngine.PATH_TO_DRIVERS)
		else:
			raise Exception(driverName + ' not supported')
		
	@staticmethod
	def save(obj, pBackend, parser=None, **kwargs):
		return PersistenceEngine._getDriver(pBackend).save(obj, parser, **kwargs)
	
	@staticmethod
	def load(tableName, pBackend, resolverMappings, parser=None, **kwargs):
		return PersistenceEngine._getDriver(pBackend).load(tableName, resolverMappings, parser, **kwargs)

        '''
        Retrieves every Driver's PolicyRuleTable object for a given name.
        This method should be seldom used.
        '''
	@staticmethod
	def loadAll(tableName, pBackend):
		return PersistenceEngine._getDriver(pBackend).loadAll(tableName)

        '''
        Deletes a Driver's PolicyRuleTable object for a given ID.
        This method should be seldom used.
        '''
        @staticmethod
        def delete(tableID, pBackend):
                return PersistenceEngine._getDriver(pBackend).delete(tableID)

