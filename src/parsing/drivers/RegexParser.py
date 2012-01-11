import os
import sys
import time
import uuid

import re

'''
        @author: msune

	RegexParser class
'''


#from Rule import *
from Rule import *
from Condition import *
from ConditionGetter import*
#from Condition import *

'''RegexParser class'''
class RegexParser():
	
	_rValues=["accept","deny"] #Must be lowercase

	def __init__(self):
		raise Exception("Static class cannot be instanciated")	

	#Recover group by name from a matched regex
	@staticmethod
	def _getGroupByName(match,name):
		try:
			return match.group(name)
		except:
			return None

	#Try to parse as a number
	@staticmethod
	def _getNumericValue(string):
		try:
			#Try to parse integer
			return int(string)	
		except:
			#Try a floating point
			try:
				return float(string)	
			except:
				return string
	
	@staticmethod
	def stripExtraParenthesis(string):
		#TODO: implement if we want to support extra(outter) parenthesis; e.g. if (A>B) then ... 
		return string	

	@staticmethod
	def _parseCondition(conditionString):
		#Detect complex condition (Boolean) 
	
		#match = re.match(r'[\s]*(not)?[\s]*\((.+)\)[\s]*(&&|\|\|)[\s]*\((.+)\)[\s]*', conditionString,re.IGNORECASE)
		#match = re.match(r'[\s]*(not)?[\s]*\((.+)\)[\s]*(&&|\|\|)[\s]*(not)?[\s]*\((.+)\)[\s]*',conditionString,re.IGNORECASE)
		
		match = re.match(r'[\s]*(not)?[\s]*\(*(.+)\)*[\s]*(&&|\|\|)[\s]*(not)?[\s]*\(*(.+)\)*[\s]*',conditionString,re.IGNORECASE)
		

		if match:
			Complex_Condition = Split_Complex_Condition(match.group())

			return Condition(RegexParser._parseCondition(Complex_Condition[0]),RegexParser._parseCondition(Complex_Condition[1]),Complex_Condition[2],match.group(1) != None)
			#return Condition(RegexParser._parseCondition(match.group(2)),RegexParser._parseCondition(match.group(4)),match.group(3),match.group(1) != None)
		else:
			#Simple conditions
			match = re.match(r'[\s]*(not )?[\s]*([^()\s]+)[\s]*(=|!=|>|<|>=|<=)[\s]*([^()\s]+)[\s]*', conditionString,re.IGNORECASE)
			if match:
				return Condition(RegexParser._getNumericValue(match.group(2)),match.group(4),RegexParser._getNumericValue(match.group(3)),match.group(1) != None)	
			else:
				#Ranges and collections
				match = re.match(r'[\s]*(not )?[\s]*(\w+)[\s]+(in|not[\s]+in)[\s]+(collection|range)[\s]*(\{(.+)\}|\[(.+)\])[\s]*', conditionString,re.IGNORECASE)
				if match:
					negate = None
					if re.match(r'[\s]*\[(.*)]',match.group(5)):
						operator="[]"
						if match.group(4).lower() == "collection":
							raise Exception("Error while parsing Rule in field Condition. Unknown operator/collection")
					else:
						operator="{}"
						negate= match.group(1)!=None or match.group(3).lower().find("not") != -1
						
					if match.group(4).lower() == "collection":
						#is collection
						submatch = re.match(r'[\s]*\{[\s]*(.*)[\s]*\}',match.group(5))
							
						if not submatch:
							raise Exception("Error while parsing Rule in field Condition. Unknown Operator")
					#	strings = re.findall(r'[\s]*([^,]+)[\s]*,',submatch.group(1))
						strings = re.findall(r'[\s]*([^,]+)[\s]*',submatch.group(1))
						
						if not strings:
							raise Exception("Error while parsing Rule in field Condition. Substrings")
						
						return Condition(match.group(2),Collection(strings),"in", negate )
					else:
						#is range
						submatch = re.match(r'[\s]*(\[|\{)[\s]*(.*)[\s]*,[\s]*(.*)[\s]*(\]|\})[\s]*',match.group(5))
						if not submatch:
							raise Exception("Error while parsing Rule in field Condition.")
						
						return Condition(match.group(2),Range(submatch.group(2),submatch.group(3)),operator, negate)
		raise Exception("Error while parsing Rule in field Condition. Unknown Operator.")
			
	@staticmethod
	def parseRule(toParse,rule_uuid=None):
		
		#Extracting basics of the rule	
		match = re.match(r'[\s]*if[\s]+(?P<condition>.+)[\s]+then[\s]+(?P<rValue>\w+)[\s]+(?P<term>nonterminal)?[\s]*(?P<do>do)?[\s]*(?P<action>[^#\s]+)[\s]([\s]*denyMessage([\s])*(?P<errorMsg>[^#]+))?([\s]*#([\s]*)(?P<comment>.+))?[\s]*', toParse,re.IGNORECASE)
		if not match:
			raise Exception("Error while parsing Rule.") 
	
		#Generate Rule
		if match.group("rValue").lower() not in RegexParser._rValues:
			raise Exception("Error while parsing Rule. Unknown Rule value")
		
		cond = RegexParser._parseCondition(RegexParser.stripExtraParenthesis(match.group("condition")))
		
		description=RegexParser._getGroupByName(match,"comment")
		term=RegexParser._getGroupByName(match,"term")#.lower()
		error=RegexParser._getGroupByName(match,"errorMsg")
		UUID = uuid.uuid4()	
	
		if match.group("rValue").lower() == "accept":
			if  term == "nonterminal":
				rType = Rule.POSITIVE_NONTERMINAL
			else:
				rType = Rule.POSITIVE_TERMINAL
		else:
			if  term == "nonterminal":
				rType = Rule.NEGATIVE_NONTERMINAL
			else:
				rType = Rule.NEGATIVE_TERMINAL

		
		
		return Rule(cond,
			description,
			error,
			rType,
			RegexParser._getGroupByName(match,"action"),
			rule_uuid,
			)	



	#Crafter must be independent of the Rule representation via dump()
	@staticmethod
	def craftCondition(cond):
		string = ""
		operator=""

		if cond.getNegate():
			string+="not "
		
		if isinstance(cond.getLeftOperand(),Condition):
			#Complex condition (boolean)
			left = RegexParser.craftCondition(cond.getLeftOperand())
			right = RegexParser.craftCondition(cond.getRightOperand())
			
			string += "(%s) %s (%s)"%(left,cond.getOperator(),right)
			return string 
		else:
			#Simple condition
			if cond.getOperator() == "[]" or cond.getOperator() == "{}":
				#Range
				if not cond.getOperator == "[]":
					string+="%s %s {%s}"%(cond.getLeftOperand(),"in Range",cond.getRightOperand())
				else:
					string+="%s %s [%s]"%(cond.getLeftOperand(),"in Range",cond.getRightOperand())		
						
				return string 
			elif cond.getOperator() == "in":
				#Collection	
				string+="%s %s {%s}"%(cond.getLeftOperand(),"in collection",cond.getRightOperand())		
				return string 
			else:
				string+="%s %s %s"%(cond.getLeftOperand(),cond.getOperator(),cond.getRightOperand())		
				return string 

	@staticmethod
	def craftRule(rule):
		  
		string  = " if %s then " %(RegexParser.craftCondition(rule.getCondition()))
		#rValue
		if rule.getType()["value"]:
			string+="accept "
		else:
			string+="deny "
		#terminal
		if not rule.getType()["terminal"]:
			string+="nonterminal "	
		#Match action
		if rule.getMatchAction():
			string+="do %s "%rule.getMatchAction()
		#ErrorMsg action
		if rule.getErrorMsg():
			string+="denyMessage %s "%rule.getErrorMsg()
		#Description
		if rule.getDescription():
			string+="#%s "%rule.getDescription()

		return string 

	''' Rule Class Getters '''
	
        @staticmethod
	def getRuleCondition(rule):
		return rule.getCondition()

	@staticmethod
	def getRuleType(rule):		
		dic = rule.getType()
		if dic['value']:
			toReturnValue = 'accept'
		else:
			toReturnValue = 'deny'

		if dic['terminal']:
			toReturnTerminal = 'terminal'
		else:
			toReturnTerminal = 'non-terminal'
	
		return toReturnValue, toReturnTerminal

	@staticmethod
	def getRuleError(rule):
		return rule.getErrorMsg()

	@staticmethod
	def getRuleDescription(rule):
		return rule.getDescription()

	@staticmethod
	def getRuleAction(rule):
		return rule.getMatchAction()

	@staticmethod
	def getRuleDump(rule):
		return rule.dump()

	''' Condition Class Getters '''
	@staticmethod
	def getCondition(rule):
		return rule.getCondition()
	
	@staticmethod
	def getConditionLeftOperand(rule):
		return rule.getCondition().getLeftOperand()

	@staticmethod
	def getConditionRightOperand(rule):
		return rule.getCondition().getRightOperand()

	@staticmethod
	def getConditionOperator(rule):
		return rule.getCondition().getOperator()

	@staticmethod
	def getConditionDump(rule):
		return rule.getCondition().dump()


