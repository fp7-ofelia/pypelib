import os
import sys
import time
import exceptions
from threading import Thread, Lock

'''
        @author: msune

	PolicyEngine RuleTable class
	Encapsulates logic of a simple Rule Table 
'''
from resolver.Resolver import Resolver 
from Rule import Rule,TerminalMatch
from parsing.ParseEngine import *
from persistence.PersistenceEngine import *

class RuleEntry():
	rule = None
	enabled = True	

	def __init__(self,rule, enabled=True):
		self.rule = rule
		self.enabled = enabled

class RuleTable():
	uuid=None
	name=None
	_persist = None
	_parser = None
	_persistenceBackend = None
	
	#Default table policy
	_policy = None
	_ruleSet = None 
	_mappings = None 
	_mutex = None
	_resolver = None
	
	#Constructor
	def __init__(self,name,resolverMappings,defaultParser, defaultPersistence, defaultPersistenceFlag, pType = False, uuid = None):
		if not isinstance(pType,bool):
			raise Exception("Unknown default table policy")
		self.uuid = uuid
		self.name = name
		self._mutex=Lock()
		self._policy = pType
		self._parser = defaultParser
		self._persistenceBackend = defaultPersistence
		self._persist = defaultPersistenceFlag
		self._mappings = resolverMappings
		self._ruleSet = list()

		if self._persist: 
			self.save()

		#Generate the resolver
		self._resolver = Resolver(resolverMappings)
	
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
		if (not rule) and (not index):
			raise Exception("Unable to determine which rule to remove; you must specify either the rule or the index")

		with self._mutex:
			if not ruleNumber:
				index = self._getRuleIndex(rule)
				if not index:
					raise Exception("Unable to find rule in the ruleSet")
			self._ruleSet.pop(position)
			if self._persist:
				self.save()

	def moveRule(self, newIndex, rule=None, index=None,):
		if (not rule) and (not index):
			raise Exception("Unable to determine which rule to move; you must specify either the rule or the index")

		with self._mutex:	
			if not index:
				index = self._getRuleIndex(rule)
				if not index:
					raise Exception("Unable to find rule in the ruleSet")
			self._ruleSet.insert(newIndex, self._ruleSet.pop(index))
			if self._persist:		
				self.save()

	def _modEnableRule(self, enable, rule=None,index=None):
		if (not rule) and (not index):
			raise Exception("Unable to determine which rule to enable; you must specify either the rule or the index")

		with self._mutex:	
			if not index:
				index = self._getRuleIndex(rule)
				if not index:
					raise Exception("Unable to find rule in the ruleSet")
			self._ruleSet[index].enable = enable	
			if self._persist:		
				self.save()

	def enableRule(self,  rule=None, index=None):
		return self._modEnableRule(True,rule,index)
	def disableRule(self, rule=None, index= None):
		return self._modEnableRule(False,rule,index)
	
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
			return self._policy	

	def save(self, pBackend=None,**kwargs):
		if not pBackend:
			pBackend = self._persistenceBackend
		PersistenceEngine.saveRuleTable(self,pBackend,kwargs)

	#In general should not be called, use loadOrGenerate instead	
	@staticmethod
	def load(tableName, pBackend,**kwargs):
		return PersistenceEngine.loadRuleTable(tableName,pBackend,kwargs)
	
	@staticmethod
	def loadOrGenerate(name,resolverMappings,defaultParser, defaultPersistence, defaultPersistenceFlag, pType = False, uuid = None,**kwargs):
		try:
			return PersistenceEngine.loadRuleTable(tableName,pBackend,kwargs)
		except Exception as e:
			print "Unable to load RuleTable, generating a new one"

		return RuleTable(name,resolverMappings,defaultParser, defaultPersistence, defaultPersistenceFlag, pType, uuid,kwargs)
	
	def getRuleSet(self):
		return self._ruleSet
					
