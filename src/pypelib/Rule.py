import os
import sys
import time
import exceptions
import uuid
import logging

'''
        @author: msune,lbergesio,omoya,CarolinaFernandez
	@organization: i2CAT, OFELIA FP7

	PolicyEngine Rule class
	Encapsulates logic of a simple Rule	 
'''

from pypelib.Condition import Condition
from pypelib.persistence.PersistenceEngine import PersistenceEngine
from pypelib.utils.Logger import Logger

class TerminalMatch(exceptions.Exception):
	value = None
	desc = None
	def __init__(self,rType,desc):
		if isinstance(rType['value'],bool):
			self.value = rType['value']
		else:
			raise Exception("Unknown rule type")
		self.desc = desc	
	def __str__(self):
		return "%s "%self.desc

class Rule():	
	
	logger = Logger.getLogger()
	#Class Attributes
	_condition = None 
	_description = None 
	_errorMsg = None
	_uuid = None #uuid.uuid4().hex
        _defaultParser = "RegexParser"
        _defaultPersistence = "Django"

	#Types of rule
	POSITIVE_TERMINAL={'value':True,'terminal':True}
	POSITIVE_NONTERMINAL={'value':True,'terminal':False}
	NEGATIVE_TERMINAL={'value':False,'terminal':True}
	NEGATIVE_NONTERMINAL={'value':False,'terminal':False}
	
	_types = [POSITIVE_TERMINAL,POSITIVE_NONTERMINAL,NEGATIVE_TERMINAL, NEGATIVE_NONTERMINAL]

	#Rule type 
	_type = None 

	#Rule match Action
	_matchAction=None


	#Getters
	def getCondition(self):
		return self._condition
	def getDescription(self):
		return self._description
	def getType(self):
		return self._type
	def getErrorMsg(self):
		return self._errorMsg
	def getMatchAction(self):
		return self._matchAction
	def getUUID(self):
		return self._uuid
	#setters
	def setUUID(self,UUID):
		self._uuid = UUID
	
	#Constructor
	def __init__(self,condition,description,errorMsg,ruleType=POSITIVE_TERMINAL,action=None,uuid=None):
		if not isinstance(condition,Condition):
			raise Exception("Object must be an instance of Condition")
		if ruleType not in self._types:
			raise Exception("Unknown rule type")
		if action == None and (ruleType == self.NEGATIVE_NONTERMINAL or ruleType == self.POSITIVE_NONTERMINAL):
			raise Exception("You cannot create non-terminal actionless rules")	

		self._condition = condition
		self._matchAction = action
		self._type = ruleType
		self._description = description
		self._errorMsg = errorMsg
		self._uuid = uuid 

	def dump(self):
		#Debug dump
		toReturn = self._condition.dump()
		
		toReturn+="=> %s "%str(self._type['value'])
		if self._matchAction != None:
			toReturn += "(%s) "%str(self._matchAction)
		if self._type['terminal']:
			toReturn += "[TERM] "
		if self._description:
			toReturn+=" #"+self._description
		return toReturn

	#Resolver is passed at evaluation time to be able to dynamically redirect actions
	def evaluate(self,metaObj,resolver):
		try:
			result = self._condition.evaluate(metaObj,resolver)
			Rule.logger.debug('Result was: %s',str(result))
		except Exception as e:
			Rule.logger.error('Error on rule: %s',self.dump())
			Rule.logger.error('Exception: %s', str(e))
			Rule.logger.error('Rule will be skiped!')
			result = False
		
		if result: 
			if self._matchAction != None:
				resolver.resolve(self._matchAction,metaObj)
			#If is terminal raise TerminalMatch
			if self._type['terminal']: 
				raise TerminalMatch(self._type,self._errorMsg)
		#return whatever	
		return

	def getConditionDump(self):
		return self.getCondition().dump()

