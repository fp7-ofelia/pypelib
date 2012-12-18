import os
import sys
import time

sys.path.append("../../") 
import re
from pyparsing import nestedExpr

'''
        @author: msune,cbermudo,omoya
	@organization: i2CAT, OFELIA FP7

	RegexParser class
'''

from pypelib.Rule import *
from pypelib.Condition import *



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
	def _stripExtraParenthesis(s):
		
		try:
			if s.count("(") != s.count(")"):
				raise Exception("Cannot parse condition")

			toStrip=0
			el = nestedExpr('(', ')').searchString(s).asList()
			
			if len(el) >1:
				raise Exception("non-strippable")

			def _countExtraParenthesis(el):
				if len(el) == 1 and isinstance(el[0],list):
					return 1+_countExtraParenthesis(el[0])
				return 0	
			toStrip+=_countExtraParenthesis(el[0])	

			for it in range(0,toStrip):
				match = re.match(r'[\s]*\((?P<inner>.+)\)[\s]*',s)
				s = match.group("inner")
			
		except Exception as e:
			pass
		return s 
	@staticmethod
	def _parseComplexCond(string):
                #In case of complex condition it will always be, as it is stripped, (something) 
                #re has some limitations on this
		
		string = string.replace("not(","not (")
                match = re.match(r'[\s]*(not[\s])?[\s]*\((?P<left>.+)\)[\s]*(?P<operand>&&|\|\|)[\s]*\((?P<right>.+)\)[\s]*\Z', string,re.IGNORECASE)
                neg=""
                if match:
                        neg=match.group(1) != None
                        counter = 0
                        #Complex cond
                        for iterator in range(0,len(string)-1):
                                if string[iterator] == '(':
                                        counter+=1
                                elif string[iterator] == ')':
                                        counter-=1
                                if counter== 0 and  ( string[iterator] == '&' and string[iterator+1] == '&' ):
                                        if neg:
                                                return "&&", string[0:iterator].replace("not","",1), string[iterator+2:len(string)],neg
                                        else:
                                                return "&&", string[0:iterator], string[iterator+2:len(string)],neg
#                                       return "&&", string[(0+3*int(neg)):iterator], string[iterator+2:len(string)],neg
                                elif counter == 0 and (  string[iterator] == '|' and string[iterator+1] == '|' ):
                                        if neg:
                                                return "||", string[0:iterator].replace("not","",1), string[iterator+2:len(string)],neg
                                        else:
                                                return "||", string[0:iterator], string[iterator+2:len(string)],neg
#                                       return "||", string[(0+3*int(neg)):iterator], string[iterator+2:len(string)],neg

                return None,None,None,None
 
	@staticmethod
	def _parseCondition(string):
		#first strip extra parenthesis if any
		conditionString = RegexParser._stripExtraParenthesis(string)
		#Detect complex condition (Boolean) 
		op,leftOP,rightOP,neg = RegexParser._parseComplexCond(conditionString)
		
		if op:
			#print "---->Value neg:"+str(neg)+ " left: "+leftOP+"right: "+rightOP+" op:"+op
			return Condition(RegexParser._parseCondition(leftOP),RegexParser._parseCondition(rightOP),op,neg)
		else:
			#Simple conditions
			match0 = re.match(r'[\s]*(not[\s])?[\s]*([^()\s]+)[\s]*(>=|<=)[\s]*([^()\s]+)[\s]*', conditionString,re.IGNORECASE)
			if match0:
                        	return Condition(RegexParser._getNumericValue(match0.group(2)),match0.group(4),RegexParser._getNumericValue(match0.group(3)),match0.group(1) != None)
			match = re.match(r'[\s]*(not[\s])?[\s]*([^()\s]+)[\s]*(=|!=|>|<)[\s]*([^()\s]+)[\s]*', conditionString,re.IGNORECASE)
			if match:
				return Condition(RegexParser._getNumericValue(match.group(2)),match.group(4),RegexParser._getNumericValue(match.group(3)).replace(" ",""),match.group(1) != None)	
			else:
				#Ranges and collections
				match = re.match(r'[\s]*(not[\s])?[\s]*(.+)[\s]+(in|not[\s]+in)[\s]+(collection|range)[\s]*(\{(.+)\}|\[(.+)\])[\s]*', conditionString,re.IGNORECASE)
				if match:
					negate = None
					if re.match(r'[\s]*\[(.*)]',match.group(5)):
						operator="[]"
						if match.group(4).lower() == "collection":
							raise Exception("Error while parsing Rule(Condition). Unknown operator/collection")
					else:
						operator="{}"
					negate= match.group(1)!=None or match.group(3).lower().find("not") != -1
						
					if match.group(4).lower() == "collection":
						#is collection
						submatch = re.match(r'[\s]*\{[\s]*(.*)[\s]*\}',match.group(5))
						if not submatch:
							raise Exception("Error while parsing Rule(Condition).")
						strings = submatch.group(1).split(",")
						
						if not strings:
							raise Exception("Error while parsing Rule(Condition). Substrings")
						
						
						return Condition(match.group(2),Collection(strings),"in", negate )
					else:
						#is range
						submatch = re.match(r'[\s]*(\[|\{)[\s]*(.*)[\s]*,[\s]*(.*)[\s]*(\]|\})[\s]*',match.group(5))
						if not submatch:
							raise Exception("Error while parsing Rule(Condition).")
						
					
						return Condition(match.group(2),Range(submatch.group(2),submatch.group(3)),operator, negate)
		raise Exception("Error while parsing Rule(Condition)")
			
	@staticmethod
	def parseRule(toParse):
		
		#Extracting basics of the rule	
		#match = re.match(r'[\s]*if[\s]+(?P<condition>.+)[\s]+then[\s]+(?P<rValue>\w+)[\s]+(?P<term>nonterminal)?[\s]*(?P<do>do)?[\s]*(?P<action>[^#\s]+)[\s]([\s]*denyMessage([\s])*(?P<errorMsg>[^#]+))?([\s]*#([\s]*)(?P<comment>.+))?[\s]*', toParse,re.IGNORECASE)
		match = re.match(r'[\s]*if[\s]+(?P<condition>.+)[\s]+then[\s]+(?P<rValue>\w+)[\s]*(?P<term>nonterminal)?[\s]*(do[\s]+(?P<action>[^#\s]+))?[\s]*(denyMessage[\s]+(?P<errorMsg>[^#]+))?[\s]*(#[\s]*(?P<comment>.+))?[\s]*', toParse,re.IGNORECASE)
		
		if not match:
			raise Exception("Error while parsing Rule.") 
	
		#Generate Rule
		if match.group("rValue").lower() not in RegexParser._rValues:
			raise Exception("Error while parsing Rule. Unknown Rule value")
		
		cond = RegexParser._parseCondition(match.group("condition"))
		
		description=RegexParser._getGroupByName(match,"comment")
		term=RegexParser._getGroupByName(match,"term")
		error=RegexParser._getGroupByName(match,"errorMsg")
	
		if match.group("rValue").lower() == "accept":
			if  term and term.lower() == "nonterminal":
				rType = Rule.POSITIVE_NONTERMINAL
			else:
				rType = Rule.POSITIVE_TERMINAL
		elif match.group("rValue").lower() == "deny":
			if  term and term.lower() == "nonterminal":
				rType = Rule.NEGATIVE_NONTERMINAL
			else:
				rType = Rule.NEGATIVE_TERMINAL
		
		else:
			raise Exception("Unknown return value")
		return Rule(cond,
			description,
			error,
			rType,
			RegexParser._getGroupByName(match,"action")	
			)	



	#Crafter must be independent of the Rule representation via dump()
	@staticmethod
	def _craftCondition(cond):
		string = ""
		operator=""

		if cond.getNegate():
			string+="not "
		
		if isinstance(cond.getLeftOperand(),Condition):
			#Complex condition (boolean)
			left = RegexParser._craftCondition(cond.getLeftOperand())
			right = RegexParser._craftCondition(cond.getRightOperand())
			
			string += "(%s) %s (%s)"%(left,cond.getOperator(),right)
			return string 
		else:
			#Simple condition
			if cond.getOperator() == "[]" or cond.getOperator() == "{}":
				#Range
				if not cond.getOperator() == "[]":
					string+="%s %s {%s}"%(cond.getLeftOperand(),"in range",cond.getRightOperand())
				else:
					string+="%s %s [%s]"%(cond.getLeftOperand(),"in range",cond.getRightOperand())		
						
				return string 
			elif cond.getOperator() == "in":
				#Collection	
				string+="%s %s {"%(cond.getLeftOperand(),"in collection")
				it=0
				for item in cond.getRightOperand():
					string +=item
					if it+1 != len(cond.getRightOperand()):
						 string+=","
					it+=1
				string +="}"
				return string 
			else:
				string+="%s %s %s"%(cond.getLeftOperand(),cond.getOperator(),cond.getRightOperand())		
				return string 

	@staticmethod
	def craftRule(rule):
		string  = "if %s then " %(RegexParser._craftCondition(rule.getCondition()))
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
			string+="denyMessage %s "%rule.getErrorMsg().rstrip()
		#Description
		if rule.getDescription():
			string+="#%s "%rule.getDescription().rstrip()

		return string



