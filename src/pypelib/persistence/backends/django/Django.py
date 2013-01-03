import os
import sys
import time
import uuid
import logging

'''
        @author: msune,lbergesio,cbermudo,omoya,CarolinaFernandez
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
from pypelib.utils.Logger import Logger
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from pypelib.utils.Exceptions import *


#XXX: Django is required to run this driver
class Django(): 
	
	logger = Logger.getLogger()
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
				# If #Rules == #Models then it is the PolicyRuleTableModel being
				# deleted, not the PolicyRuleModel (last is the normal case)
				if len(obj._ruleSet) != PolicyRuleModel.objects.all().count():
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
	def load(tableName, mappings, parser):
		Django.logger.info('Django.load')
		try:
			Table =  PolicyRuleTableModel.objects.get(name = tableName)
		# Translation of exceptions: Django -> PyPElib
		except ObjectDoesNotExist:
			raise ZeroPolicyObjectsReturned("[Django Driver] There is no table with name: " + tableName)
		except MultipleObjectsReturned:
			raise MultiplePolicyObjectsReturned("[Django Driver] There are multiple tables with name: " + tableName)
		except Exception as e:
			raise Exception("[Django Driver] Some error occurred when trying to fetch table table with name: " + tableName + ". Exception: " + str(e))

		ruleTable = RuleTable(Table.name,mappings,Table.defaultParser, Table.defaultPersistence,False, eval(Table.type), Table.uuid)
		ruleTable._ruleSet = Django.loadRuleSet(Table.uuid)
		ruleTable._persist = Table.defaultPersistenceFlag
		ruleTable._mappings = mappings
		ruleTable._resolver = Resolver(mappings)
		return ruleTable
	
	'''
	Retrieves every PolicyRuleTable object by name.
	This method should be seldom used.
	'''
	@staticmethod
	def loadAll(tableName):
		Django.logger.debug('Loading RuleTable set...')
		try:
			return PolicyRuleTableModel.objects.filter(name = tableName).order_by('id')
		except:
			Django.logger.warning('[Django Driver] Could not retrieve any PolicyRuleTable object by the name: %s' % tableName)
			return list()

        '''
        Deletes a PolicyRuleTable object for a given ID.
        This method should be seldom used.
        '''
        @staticmethod
        def delete(tableID):
                Django.logger.debug('Deleting RuleTable with id = %s...' % tableID)
                try:
                        table = PolicyRuleTableModel.objects.get(id = tableID)
			# If this is the latest PolicyRuleTable, delete its associated PolicyRule's
			if PolicyRuleTableModel.objects.filter(name=table.name).count() == 1:
				PolicyRuleModel.objects.filter(RuleTableName=table.name).delete()
			table.delete()
                except Exception as e:
                        Django.logger.warning('[Django Driver] Could not delete the PolicyRuleTable object with ID: %s. Exception: %s' % (tableID,str(e)))

	@staticmethod
	def loadRuleSet(table_uuid):
		Django.logger.debug('Loading Rule set...')
		try: 
			ruleTable = PolicyRuleTableModel.objects.get(uuid = table_uuid)
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
	

