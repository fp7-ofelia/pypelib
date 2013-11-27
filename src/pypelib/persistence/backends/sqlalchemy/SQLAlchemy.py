import os
import sys
import time
import uuid
import logging

from .RuleModel import PolicyRuleModel
from .RuleTableModel import PolicyRuleTableModel
from pypelib.parsing.ParseEngine import ParseEngine
from pypelib.Rule import Rule
from pypelib.RuleTable import*
from pypelib.resolver.Resolver import Resolver
from pypelib.utils.Logger import Logger
from pypelib.utils.Exceptions import *

from utils.commonbase import DB_SESSION

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists

'''
        @author: SergioVidiella
	@organization: i2CAT, OFELIA FP7

	SQLAlchemy backend driver	
	Implementes SQLAlchemy model-based backend 
'''


#XXX: SQLAlchemy is required to run this driver
class SQLAlchemy(): 
	
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
			ruleTable = DB_SESSION.query(PolicyRuleTableModel).filter(PolicyRuleTableModel.name == obj.name).first()
			ruleTable.type = obj._policy
			ruleTable.defaultParser = obj._parser
			ruleTable.defaultPersistence = obj._persistenceBackend
			ruleTable.defaultPersistenceFlag = obj._persist
			DB_SESSION.add(ruleTable)
			DB_SESSION.commit()
			DB_SESSION.expunge(ruleTable)
		except:		
			ruleTable = PolicyRuleTableModel(name = obj.name, uuid = obj.uuid, type = obj._policy, defaultParser = parser, defaultPersistence = obj._persistenceBackend, defaultPersistenceFlag = obj._persist)
			
			DB_SESSION.add(ruleTable)
			DB_SESSION.commit()
			DB_SESSION.expunge(ruleTable)


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
				ruleModel = DB_SESSION.query(PolicyRuleModel).filter(PolicyRuleModel.RuleUUID == rule.rule.getUUID()).first()
			except:	
				# If #Rules == #Models then it is the PolicyRuleTableModel being
				# deleted, not the PolicyRuleModel (last is the normal case)
				if len(obj._ruleSet) != DB_SESSION.query(PolicyRuleModel).all().count():
				    addRule = 1
				    ruleModel = DB_SESSION.query(PolicyRuleModel).filter(PolicyRuleModel.RuleUUID == rule.rule.getUUID()).first()

			ruleModel.RuleTableName = obj.name
			ruleModel.Rule = ParseEngine.craftRule(rule.rule, obj._parser)
			ruleModel.RuleIsEnabled = rule.enabled
			ruleModel.RulePosition = obj._ruleSet.index(rule)
			DB_SESSION.add(ruleModel)
			DB_SESSION.commit()
			DB_SESSION.expunge_all()
		#if the save() comes from a removeRule, check which one was removed and delete
		if not addRule:
			for ruleModel in DB_SESSION.query(PolicyRuleModel).filter(PolicyRuleModel.RuleTableName == obj.name).all():
				if ruleModel.RuleUUID not in uuidInRuleSet:
					DB_SESSION.delete(ruleModel)
					DB_SESSION.commit()
					DB_SESSION.expunge_all()
					break
			DB_SESSION.expunge_all()

	@staticmethod
	def load(tableName, mappings, parser):
		SQLAlchemy.logger.info('SQLAlchemy.load')
		try:
			Table =  DB_SESSION.query(PolicyRuleTableModel).filter(PolicyRuleTableModel.name == tableName).one()
		# Translation of exceptions: SQLAlchemy -> PyPElib
		except NoResultFound:
			raise ZeroPolicyObjectsReturned("[SQLAlchemy Driver] There is no table with name: " + tableName)
		except MultipleResultsFound:
			raise MultiplePolicyObjectsReturned("[SQLAlchemy Driver] There are multiple tables with name: " + tableName)
		except Exception as e:
			raise Exception("[SQLAlchemy Driver] Some error occurred when trying to fetch table table with name: " + tableName + ". Exception: " + str(e))

		ruleTable = RuleTable(Table.name,mappings,Table.defaultParser, Table.defaultPersistence,False, eval(Table.type), Table.uuid)
		ruleTable._ruleSet = SQLAlchemy.loadRuleSet(Table.uuid)
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
			return DB_SESSION.query(PolicyRuleTableModel).filter(PolicyRuleTableModel.name == tableName).order_by(PolicyRuleTableModel.id).all()
		except:
			SQLAlchemy.logger.warning('[SQLAlchemy Driver] Could not retrieve any PolicyRuleTable object by the name: %s' % tableName)
			DB_SESSION.expunge_all()
			return list()

        '''
        Deletes a PolicyRuleTable object for a given ID.
        This method should be seldom used.
        '''
        @staticmethod
        def delete(tableID):
                SQLAlchemy.logger.debug('Deleting RuleTable with id = %s...' % tableID)
                try:
                        table = DB_SESSION.query(PolicyRuleTableModel).filter(PolicyRuleTableModel.id == tableID).first()
			# If this is the latest PolicyRuleTable, delete its associated PolicyRule's
			if DB_SESSION.query(PolicyRuleTableModel).filter(PolicyRuleTableModel.name==table.name).count() == 1:
				PolicyRuleModel.objects.filter(RuleTableName=table.name).delete()
			DB_SESSION.delete(table)
			DB_SESSION.commit()
			DB_SESSION.expunge_all()
                except Exception as e:
                        SQLAlchemy.logger.warning('[SQLAlchemy Driver] Could not delete the PolicyRuleTable object with ID: %s. Exception: %s' % (tableID,str(e)))

	@staticmethod
	def loadRuleSet(table_uuid):
		SQLAlchemy.logger.debug('Loading Rule set...')
		try: 
			ruleTable = DB_SESSION.query(PolicyRuleTableModel).filter(PolicyRuleTableModel.uuid == table_uuid).first()
		except: 
			return list()
		rules = DB_SESSION.query(PolicyRuleModel).filter(PolicyRuleModel.RuleTableName == ruleTable.name).order_by(PolicyRuleModel.RulePosition).all()
		ruleSet = []
		#The rules sort by priority 
		for rule in rules:
			ruleObj= ParseEngine.parseRule(rule.Rule)
			ruleObj._uuid = rule.RuleUUID
			ruleEntry = RuleEntry(ruleObj,rule.RuleIsEnabled)
			ruleSet.append(ruleEntry)
		DB_SESSION.expunge_all()
		return ruleSet
	

