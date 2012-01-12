import os
import sys
import time

from threading import Thread, Lock

'''
        @author: msune

	PolicyEngine Resolver class
	Encapsulates logic of  
'''

#Resolvers dictionary
_resolvers = {}	

'''Resolver class'''
class Resolver():
	
	#Class attributes
	_mappings = None
	_mutex = None
	#Constructor
	def __init__(self,mappings):
		self._mutex=Lock()
		self._mappings =mappings
		pass

	#set mappings
	#@mappings: dictionary containing name <-> mapping (object...)
	def setMappings(self,mappings):
		with self._mutex:	
			self._mappings = mappings

	#Get or generate the resolver	
	@staticmethod
	def getOrGenerateResolver(theId,mappings=None):
		if theId in _resolvers:
			return _resolvers[theId]
		
		if mappings == None:
			raise Exception("Could not find the resolver with id:"+theId)		

		instance = Resolver(mappings)
		#Save instance
		_resolvers[theId] = instance	
		
		return instance		
	
	#Try to parse as a number
	def _getNumericValue(self,string):
		try:
			#Try to parse integer
			return int(string)	
		except:
			#Try a floating point
			try:
				return float(string)	
			except:
				return string
	
	#Resolve a key
	def resolve(self, key, metaObj):
		#print "[DEBUG] resolving:"+key
		with self._mutex:
			if not isinstance(key,str):
				raise Exception("Only string keys are able to be resolved")

			if key not in self._mappings:
				return self._getNumericValue(key)
				#raise Exception("Could not resolve key "+key)
			
			if type(self._mappings) == str:	
				#print "[DEBUG] will eval"	
				return eval(self._mappings[key])
			else:
				return self._mappings(metaObj)
				

#resolver = Resolver.getOrGenerateResolver("hola",{"test":"metaObj","test2":2})
#metaObj = 3
#print "Value:"+str(resolver.resolve("test",metaObj))
#print "Value:"+str(resolver.resolve("test2",metaObj))
