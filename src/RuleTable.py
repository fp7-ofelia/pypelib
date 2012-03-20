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
from parser.ParseEngine import *
from persistence.PersistenceEngine import *

class RuleTable():
	
	#Attributes
	uuid=None
	name=None
	_defaultPersistenceFlag = None
	_defaultParser = None
	_defaultPersistence = None
	

	#Policy
	_policy = None
	#Ruleset
	_ruleSet = list()
	#Mappings
	_mappings = dict()

	#Local mutex
	_mutex = None

	#Resolver
	_resolver = None
	
	#Constructor
	def __init__(self,name,resolverMappings,defaultParser, defaultPersistence, defaultPersistenceFlag, pType = False, uuid = None,FromLoad = False):
		#if not isinstance(pType,bool):
		#	raise Exception("Unknown default table policy")
		self.uuid = uuid
		self.name = name
		self._mutex=Lock()
		self._policy = pType
		self._defaultParser = defaultParser
		self._defaultPersistence = defaultPersistence
		self._defaultPersistenceFlag = defaultPersistenceFlag
		self._mappings = resolverMappings
		
		self._ruleSet = list()
		if defaultPersistenceFlag and not FromLoad:
			self.save()

		#Generate the resolver
		self._resolver = Resolver(resolverMappings)

	
	#Add, move and remove rule
	def addRule(self,string,pos=None,parser=None,persistence=None,doPersistence=None):
		if parser == None:
			usedParser = self._defaultParser
		else:
			usedParser = parser

		rule = ParseEngine.parseRule(string, driverName = usedParser)

		if doPersistence or (doPersistence == None and self._defaultPersistenceFlag):
			if persistence == None:
				usedPersistence = self._defaultPersistence
			else:
				usedPersistence = persistence
			#PersistenceEngine.save(string, usedParser, usedPersistence)
		#self.loadRuleSet()

		#self._ruleSet = PersistenceEngine.loadRuleSet(self.uuid, usedPersistence)
		
		with self._mutex:	
			if pos > len(self._ruleSet):
				#raise Exception("Invalid position")
				self._ruleSet.append(rule)				
			elif pos !=None:
				self._ruleSet.insert(pos,rule)
			else:
				self._ruleSet.append(rule)
			if self._defaultPersistenceFlag:
				self.save()	

	def removeRule(self,rule, position = None):	
		if position == 0:
			aux = True
		else:
			aux = False

		if not position and not aux:
			with self._mutex:
				self._ruleSet.pop(self._ruleSet.index(rule))
				if self._defaultPersistenceFlag:
					self.save()
		else:
			with self._mutex:
                                self._ruleSet.pop(position)
				if self._defaultPersistenceFlag:
                                	self.save()

	def moveRule(self,rule,newIndex):

		self.loadRuleSet()
		with self._mutex:	
			oldIndex = self._ruleSet.index(rule)
			l.insert(newindex, l.pop(oldIndex))
			if self._defaultPersistenceFlag:		
				self.save()

	def dump(self):
		#Debug dump
		#self.loadRuleSet(usedPersistence)
		print "Table: "+self.name+" UUID: "+str(self.uuid)
		print "NUmber of rules: "+str(len(self._ruleSet))
		with self._mutex:
			i=0
			for rule in self._ruleSet:
				#print "[%s]:"%i +rule.dump()
				print  "[%s]:"%i + ParseEngine.craftRule(rule,self._defaultParser)
				i+=1
		
		print "Default policy: "+str(self._policy)

	#Go through the table
	def process(self,metaObj):
		
		#Iterate over ruleset
		with self._mutex:
			for rule in self._ruleSet:
				try:
					rule.evaluate(metaObj,self._resolver)	

				except TerminalMatch as terminal:
					if terminal.value:
						return True
					else:
						raise terminal
			return self._policy	

	def save(self):
		PersistenceEngine._getDriver(self._defaultPersistence).saveRuleTable(self)
	
	@staticmethod
	def load(tableName, Persistence = 'Write'):
		return PersistenceEngine._getDriver(Persistence).loadRuleTable(tableName)

	def loadRuleSet(self):
		self._ruleSet = PersistenceEngine.loadRuleSet(self.uuid, self._defaultPersistence)
	
	def getRuleSet(self):
		return self._ruleSet
					

#table = RuleTable("My table","fancyUUID",{"vm.memory":"metaObj['memory']","project.vms":"metaObj['vms']","project.string":"metaObj['string']"},True)
#Adding dummy rule
#from Condition import Condition
#table.addRule(Rule(Condition("5","6","<"),"Description"))	

	
#table.addRule(Rule(Condition("vm.memory","2000",">"),"Memory", "Action forbbiden: You requested more that 2GB of RAM" ,Rule.NEGATIVE_TERMINAL))
#table.addRule(Rule(Condition("project.vms","4",">="),"VMs","Action forbidden: you have 4 VMs already in the project",Rule.NEGATIVE_TERMINAL))
#table.addRule(Rule(Condition("project.string","try","!="),"String","Action forbidden: String",Rule.NEGATIVE_TERMINAL))

#table.dump()

#metaObj = {"memory":2000,"vms":"3","string":"try2"}

#Create the metaObj

#try:
#	table.process(metaObj)
#except Exception as e:
#	print e	
