import os
import sys
import time
import uuid
import logging

'''
        @author: msune,lbergesio,cbermudo,omoya
	@organization: i2CAT, OFELIA FP7

	Django backend driver	
	Implementes django model-based backend 
'''
from .RuleModel import PolicyRuleModel
from .RuleTableModel import PolicyRuleTableModel
from pypelib.parsing.ParseEngine import ParseEngine 
from pypelib.Rule import Rule
from pypelib.RuleTable import*
from pypelib.resolver.Resolver import Resolver

logging.basicConfig(format='%(asctime)s %(message)s')

#XXX: Django is required to run this driver
class Django(): 
	
	#Driver attributes
	_types = ["Rule","RuleTable"]	

	def __init__(self):
		raise Exception("Static class cannot be instanciated")	

	'''
	Stores object	
	@params: 
		parser - parser to be used
	@returns persisted instance
	'''
	@staticmethod
	def save(obj, parser):
	
		if parser == None:
			parser = obj._parser
		try:
			ruleTable = PolicyRuleTableModel.objects.get(name=obj.name)
			ruleTable.type = obj._policy
			ruleTable.defaultParser = obj._parser
			ruleTable.defaultPersistence = obj._persistenceBackend
			ruleTable.defaultPersistenceFlag = obj._persist
			ruleTable.save()
		except:		
			ruleTable = PolicyRuleTableModel(name = obj.name, uuid = obj.uuid, type = obj._policy, defaultParser = parser, defaultPersistence = obj._persistenceBackend, defaultPersistenceFlag = obj._persist)

			ruleTable.save()


		#flag to know if save comes from addRule or removeRule()
		addRule = 0
		uuidInRuleSet=list()
		for rule in obj._ruleSet:
			
			#need to removeRule later
			uuidInRuleSet.append(rule.rule.getUUID())
			#lbergesio: Rule is saved parsed, as a string
			#Possibly if Rule exists (try) it is not required to update its fields.==> 
			#==> IT IS NEEDED FOR THE RuleTable.moveRule()
			try:
				ruleModel = PolicyRuleModel.objects.get(RuleUUID = rule.rule.getUUID())
			except:	
				addRule = 1
				ruleModel = PolicyRuleModel(RuleUUID = rule.rule.getUUID())

			ruleModel.RuleTableName = obj.name
			ruleModel.Rule = ParseEngine.craftRule(rule.rule, obj._parser)
			ruleModel.RuleIsEnabled = rule.enabled
			ruleModel.RulePosition = obj._ruleSet.index(rule)
			ruleModel.save()
		#if the save() comes from a removeRule, check which one was removed and delete
		if not addRule:
			for ruleModel in PolicyRuleModel.objects.filter(RuleTableName = obj.name):
				if ruleModel.RuleUUID not in uuidInRuleSet:
					ruleModel.delete()
					break



	@staticmethod
	def load(tableName, mappings, parser ):
		logging.info('Django.load')
		try:
			Table =  PolicyRuleTableModel.objects.get(name = tableName)
		except:
			raise Exception("[Django Driver] There is no table with name: "+tableName)
		ruleTable = RuleTable(Table.name,mappings,Table.defaultParser, Table.defaultPersistence,False, eval(Table.type), Table.uuid)
		ruleTable._ruleSet = Django.loadRuleSet(Table.uuid)
		ruleTable._persist = Table.defaultPersistenceFlag
		ruleTable._mappings = mappings
		ruleTable._resolver = Resolver(mappings)
		return ruleTable
	
	@staticmethod
	def loadRuleSet(table_uuid):
		logging.debug('loading RuleSet...')
		try: 
			ruleTable = PolicyRuleTableModel.objects.get(uuid=table_uuid)
		except: 
			return list()
		rules = PolicyRuleModel.objects.filter(RuleTableName = ruleTable.name).order_by('RulePosition')
		ruleSet = []
		#The rules sort by priority 
		for rule in rules:
			ruleObj= ParseEngine.parseRule(rule.Rule)
			ruleObj._uuid = rule.RuleUUID
			ruleEntry = RuleEntry(ruleObj,rule.RuleIsEnabled)
			ruleSet.append(ruleEntry)
		return ruleSet
	
 
