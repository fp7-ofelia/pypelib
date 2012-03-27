import os
import sys
import time
import copy
try:
   import cPickle as pickle
except:
   import pickle
from threading import Thread, Lock
from resolver.Resolver import Resolver

class RAWFile():
	_mutex = Lock()

	@staticmethod
	def save(obj, parser, **kwargs):
		if "fileName" not in kwargs:
			raise Exception("FileName is required")
			
		with RAWFile._mutex:
			fileObj = open(kwargs["fileName"], "wb" )

			try:
                        	cObj = obj.clone()
			except Exception,e:
				print "Could not clone original obj %s\n%s" %(str(obj),str(e))
			
			pickle.dump(cObj,fileObj)
			fileObj.close()
			
	@staticmethod
	def load(tableName, parser, **kwargs):

		with RAWFile._mutex:
			if not kwargs["fileName"]:
				raise Exception("FileName is required")
		
			fileObj = open(kwargs["fileName"], "r" )
			table = pickle.load(fileObj)
			table._mutex = Lock()
			table._resolver = Resolver(table._mappings)
			print table
			fileObj.close()
				
			if table.name != tableName:
				raise Exception("Table name mismatch; did you specify the correct file?")
			return table


