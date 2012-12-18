import os
import sys
import time
import exceptions
import copy 
import logging
from threading import Thread, Lock
import uuid

try:
   import cPickle as pickle
except:
   import pickle

'''
        @author: msune,lbergesio,omoya,cbermudo,CarolinaFernandez
	@organization: i2CAT, OFELIA FP7

	PolicyEngine RuleTable class
	Encapsulates logic of a simple Rule Table 
'''
from pypelib.resolver.Resolver import Resolver 
from pypelib.Rule import Rule,TerminalMatch
from pypelib.parsing.ParseEngine import ParseEngine
from pypelib.persistence.PersistenceEngine import PersistenceEngine
from pypelib.utils.Logger import Logger
from pypelib.utils.Exceptions import *

class RuleEntry():
	rule = None
	enabled = True	

	def __init__(self,rule, enabled=True):
		self.rule = rule
		self.enabled = enabled

class RuleTable():
	
	logger = Logger.getLogger()
	uuid=None
	name=None
	_persist = None
	_parser = None
	_persistenceBackend = None
	_persistenceBackendParameters=None	

	#Default table policy
	_policy = None
	_ruleSet = None 
	_mappings = None 
	_mutex = None
	_resolver = None

	#Constructor
	def __init__(self,name,resolverMappings,defaultParser, defaultPersistence, defaultPersistenceFlag, pType = False, uuid = None,**kwargs):
		if not isinstance(pType,bool):
			raise Exception("Unknown default table policy")
		self.uuid = uuid
		self.name = name
		self._mutex = Lock()
		self._policy = pType
		self._parser = defaultParser
		self._persistenceBackend = defaultPersistence
		self._persist = defaultPersistenceFlag
		self._mappings = resolverMappings
		self._ruleSet = list()
		self._persistenceBackendParameters = kwargs

		if self._persist: 
			self.save(self._persistenceBackend,**kwargs)

		#Generate the resolver
		self._resolver = Resolver(resolverMappings)

        #Deep copy
        def clone(self):
                #XXX: in principle mutex is not needed since methods calling clone() are already protected
                #with self._mutex:
                cpTable = RuleTable(self.name,None,self._parser,self._persistenceBackend, False,self._policy,self.uuid, **self._persistenceBackendParameters)
                cpTable._mutex = None
                cpTable._persist = copy.deepcopy(self._persist)
                cpTable._ruleSet = copy.deepcopy(self._ruleSet)
                cpTable._resolver = None
                return cpTable

	
	#Determine rule position
	def _getRuleIndex(self, rule):	
		for it in self._ruleSet:
			if it.rule == rule:
				return self._ruleSet.index(it)
		return None	

	def getRule(self, index):	
		return self._ruleSet[index].rule
	
	#Add, move and remove rule
	def addRule(self,string,enabled=True,pos=None,parser=None,pBackend=None,persist=True):
		if not parser:
			parser = self._parser
		
		rule = ParseEngine.parseRule(string, parser)
		rule.setUUID(uuid.uuid4().hex)
		
		with self._mutex:	
			if pos > len(self._ruleSet):
				#raise Exception("Invalid position")
				self._ruleSet.append(RuleEntry(rule,enabled))				
			elif pos !=None:
				self._ruleSet.insert(pos,RuleEntry(rule,enabled))
			else:
				self._ruleSet.append(RuleEntry(rule,enabled))
			if self._persist:
				self.save()	

	def removeRule(self,rule=None, index=None):
		if (not rule) and (index == None):
			raise Exception("Unable to determine which rule to remove; you must specify either the rule or the index")

		with self._mutex:
			if index == None:
				index = self._getRuleIndex(rule)
				if index == None:
					raise Exception("Unable to find rule in the ruleSet")
			self._ruleSet.pop(index)
			if self._persist:
				self.save()

	def moveRule(self, newIndex, rule=None, index=None):
		if (not rule) and (index == None):
			raise Exception("Unable to determine which rule to move; you must specify either the rule or the index")

		with self._mutex:	
			if index == None:
				index = self._getRuleIndex(rule)
				if index == None:
					raise Exception("Unable to find rule in the ruleSet")
			self._ruleSet.insert(newIndex, self._ruleSet.pop(index))
			if self._persist:		
				self.save()

	def _modEnableRule(self, enable, rule=None,index=None):
		if (not rule) and (index == None):
			raise Exception("Unable to determine which rule to enable; you must specify either the rule or the index")

		with self._mutex:	
			if index == None:
				index = self._getRuleIndex(rule)
				if index == None:
					raise Exception("Unable to find rule in the ruleSet")
			self._ruleSet[index].enabled = enable	
			if self._persist:		
				self.save()

	def enableRule(self,  rule=None, index=None):
		return self._modEnableRule(True,rule,index)
	def disableRule(self, rule=None, index= None):
		return self._modEnableRule(False,rule,index)

	def setPolicy(self, policy):
		if not isinstance(policy,bool):
			raise Exception("Unknown default table policy")
		with self._mutex:
			self._policy = policy
			if self._persist:
				self.save()

	def setParser(self, parser):
		with self._mutex:
			self._parser = parser
			if self._persist:
				self.save()

	def setPersistenceBackend(self, persistenceBackend):
		with self._mutex:
			self._persistenceBackend = persistenceBackend
			if self._persist:
				self.save()

	def setPersistenceFlag(self, persistenceFlag):
		with self._mutex:
			self._persist = persistenceFlag
			if self._persist:
				self.save()

	def setMappings(self, mappings):
		with self._mutex:
			self._mappings = mappings
			if self._persist:
				self.save()

	def dump(self):
		print "Table: "+self.name+" UUID: "+str(self.uuid)
		print "NUmber of rules: "+str(len(self._ruleSet))
		with self._mutex:
			i=0
			for it in self._ruleSet:
				print "[%s]:"%i +it.rule.dump()+ " Enabled: "+str(it.enabled)
				i+=1
		
		print "Default policy: "+str(self._policy)

	#Go through the table
	def evaluate(self,metaObj):
		#Iterate over ruleset
		with self._mutex:
			for it in self._ruleSet:
				if it.enabled:
					try:
						it.rule.evaluate(metaObj,self._resolver)	
					except TerminalMatch as terminal:
						if terminal.value:
							return True
						else:
							raise terminal
			if self._policy:
				return self._policy
			else:
				raise Exception("Policy verification failed. Policy type is DENY")	

	def save(self, pBackend=None,**kwargs):
		if not pBackend:
			pBackend = self._persistenceBackend
		if not kwargs:
			kwargs2 = self._persistenceBackendParameters
		else:
			kwargs2 = kwargs
		PersistenceEngine.save(self,pBackend,**kwargs2)

	#In general should not be called, use loadOrGenerate instead	
	@staticmethod
	def load(name, resolverMappings, pBackend, **kwargs):
		return PersistenceEngine.load(name,pBackend,resolverMappings,**kwargs)
	
	@staticmethod
	def loadOrGenerate(name,resolverMappings,defaultParser, defaultPersistence, defaultPersistenceFlag, pType=False, uuid=None,**kwargs):
		try:
			return PersistenceEngine.load(name,defaultPersistence, resolverMappings, defaultParser,**kwargs)
		except ZeroPolicyObjectsReturned:
			RuleTable.logger.warning("Unable to load RuleTable, generating a new one")
			return RuleTable(name,resolverMappings,defaultParser, defaultPersistence, defaultPersistenceFlag, pType, uuid,**kwargs)
		except MultiplePolicyObjectsReturned:
			RuleTable.logger.warning("Unable to load a single RuleTable, asking the user")
			raise MultiplePolicyObjectsReturned
		except Exception as e:
			RuleTable.logger.error("Unable to load RuleTable. Exception: %s" % str(e))

        '''
        Retrieves every Engine's PolicyRuleTable object for a given name.
        This method should be seldom used.
        '''
	@staticmethod
	def loadAll(name, defaultPersistence):
		return PersistenceEngine.loadAll(name, defaultPersistence)

        '''
        Deletes a Engine's PolicyRuleTable object for a given ID.
        This method should be seldom used.
        '''
        @staticmethod
        def delete(tableID, defaultPersistence):
                return PersistenceEngine.delete(tableID, defaultPersistence)

	#Getters
        def getRuleSet(self):
                return self._ruleSet

        def getName(self):
                return self.name

        def getPolicyType(self):
                return self._policy

        def getPersistence(self):
                return self._persistenceBackend

        def getParser(self):
                return self._parser

        def getResolverMappings(self):
                return self._mappings

        def getPersistenceFlag(self):
                return self._persist
