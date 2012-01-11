import os
import sys
import time
import copy
try:
   import cPickle as pickle
except:
   import pickle
from threading import Thread, Lock


class RAWFile():
	_mutex = Lock()

	@staticmethod
	def save(obj, parser, **kwargs):
		if "fileName" not in kwargs:
			raise Exception("FileName is required")
			
		with RAWFile._mutex:
			fileObj = open(kwargs["fileName"], "wb" )

			#copy original object and unmute if it is the case

			# PROBAR LO DEL __copy__ en la clase RuleTable A VER SI FUNCIONA
                        cObj = copy.deepcopy(obj)
			#if obj is a Rule it has no _mutex
			try:
				cObj._mutex = None
			except Exception,e:
				print e
				pass

			pickle.dump(cObj,fileObj)
			fileObj.close()
			
#                with RAWFile._mutex:
#                        fileObj = open(kwargs["fileName"], "wb" )
#
#                        #copy original object and unmute if it is the case
#                        cObj = RuleTable(obj.name,obj._mappings, obj._parser, obj._persistenceBackend, obj._persist, obj._policy, obj.uuid)
#                        print obj.name
#                        print cObj.name
#                        cObj.name="ELIMINADO"
#                        print obj.name
#                        for rule in obj.getRuleSet():
#                                cObj.getRuleSet().append(rule._uuid)
#                        cObj._mutex = None
#
#                        pickle.dump(cObj,fileObj)
#                        fileObj.close()
#
#	
	@staticmethod
	def load(tableName, parser, **kwargs):
		if not kwargs["fileName"]:
			raise Exception("FileName is required")
	
		fileObj = open(kwargs["fileName"], "r" )
		table = pickle.load(fileObj)
		table._mutex = Lock()
		fileObj.close()
			
		if table.name != tableName:
			raise Exception("Table name mismatch; did you specify the correct file?")
		return table



			
