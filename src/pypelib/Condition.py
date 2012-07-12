import os
import sys
import time

'''
        @author: msune,cbermudo,omoya
	@organization: i2CAT, OFELIA FP7

	PolicyEngine Condition class
	Encapsulates logic of a simple condition	 
'''

'''Supported operators'''
_collectionOperators= ["in"]
_logicalOperators = ["&&","||"]
_rangeOperators = ["[]","{}"]
_comparisonOperators = ["=","!=",">","<",">=","<="]
_operators = _comparisonOperators + _logicalOperators + _rangeOperators + _collectionOperators


'''Collection inner class'''
class Collection(list):

	def __init__(self,coll):
		self +=coll
			
	@staticmethod
	def isCollection(x):
		return isinstance(x,Collection) 
	
'''Range inner class'''
class Range():
	upperLimit=None
	lowerLimit=None
	
	@staticmethod
	def isRange(x):
		return isinstance(x,Range) 

	@staticmethod
	def isInRange(x,urange):
		if not Range.isRange(urange):
			raise Exception("Unknown data type; must be a Range instance")
		return urange.lowerLimit <= x <= urange.upperLimit
	
	@staticmethod
	def isInRangeStrict(x,urange):
		if not Range.isRange(urange):
			raise Exception("Unknown data type; must be a Range instance")
		return urange.lowerLimit < x < urange.upperLimit
	
	def __init__(self,lower,upper):
		if int(upper)<int(lower):
			raise Exception("Cannot create Range; upper limit must be equal or higher that lower limit")
		
		self.upperLimit = upper
		self.lowerLimit = lower

	
	def __str__(self):
	#	return "(%s,%s)"%(str(self.lowerLimit),str(self.upperLimit))
		return "%s,%s"%(str(self.lowerLimit),str(self.upperLimit))

'''Condition class'''
class Condition():
	
	#Class attributes
	_leftOperand = None
	_rightOperand = None

	_operator=None
	_negate=None

	#Getters
	def getNegate(self):
		return self._negate
	def getOperator(self):
		return self._operator
	def getLeftOperand(self):
		return self._leftOperand
	def getRightOperand(self):
		#return self._rightOperand
		return self._rightOperand

	#Constructor
	def __init__(self, left, right, operator,negate=False):

		self._leftOperand = left
		self._rightOperand = right
		self._operator = operator
		self._negate = negate	

		#Make sure user is not comparing Conditions and Literals/Values 
		if Condition.isCondition(self._rightOperand) is not Condition.isCondition(self._leftOperand):
			raise Exception("Nested Condition can only be logically operated with another Condition") 
	
		#Check if one of the operands is a Condition
		if ( Condition.isCondition(self._leftOperand) ) and operator not in _logicalOperators:
			raise Exception("Cannot evaluate expression. Only logical operators can be used while using nested Conditions")
	
		if operator in _logicalOperators and (not Condition.isCondition(self._leftOperand) ):
			raise Exception("Cannot evaluate expression. Logical operators can only be used with nested Conditions")

		#If operator is a range Operator, check left or right is a Range instance
		if self._operator in _rangeOperators and ( not ( Range.isRange(self._rightOperand) or Range.isRange(self._leftOperand) )):
			raise Exception("Cannot operate with a range without using Range instance")

		#If operator is a collection, check right is a Collection instance
		if self._operator in _collectionOperators and not Collection.isCollection(self._rightOperand):
			raise Exception("Cannot operate with a Collection without using Collection instance")

		#Check operator
		if self._operator not in _operators:
			raise Exception("Unknown operator")
		
		#Check operator
		if not isinstance(self._negate,bool):
			raise Exception("Unknown negate value")
		
	@staticmethod
	def isCondition(x):
		return isinstance(x,Condition) 

	def dump(self):
                if ( Range.isRange(self._rightOperand) ):
			negate=""
			if self._negate:
				negate="not "
			if ( self._operator == '[]' ):
				return " %s %s in range [%s] "%(negate,self._leftOperand,str(self._rightOperand))
			else:
				return " %s %s in range {%s} "%(negate,self._leftOperand,str(self._rightOperand))

		if ( Collection.isCollection(self._rightOperand) ):
			negate = ""
			if self._negate:
				negate="not "
			rightOp = "collection {" 
			for item in self._rightOperand:
				rightOp = rightOp + str(item) + ","
			rightOp = rightOp[:-1] + "}"
			return " %s %s in %s "%(negate,self._leftOperand,rightOp)

		if Condition.isCondition(self._leftOperand):
			negate = ""
			if self._negate:
				negate = "not "
			return " %s (%s) %s (%s)  "%(negate,self._leftOperand.dump(),str(self._operator),self._rightOperand.dump())
		else:
			negate=""
			if self._negate:
				negate="not "
			return " %s %s %s %s   "%(negate,self._leftOperand,str(self._operator),str(self._rightOperand))


	#Evaluate condition
	def evaluate(self, metaObj,resolver):
		#Retrieve operand value
		rightValue=None
		leftValue=None

		if Condition.isCondition(self._leftOperand):
			leftValue = self._leftOperand.evaluate(metaObj,resolver)	
			rightValue = self._rightOperand.evaluate(metaObj,resolver)	
		else:
			#Try to retrieve value from the context (if it is not a literal)

			if Collection.isCollection(self._rightOperand):
				rightValue = self._rightOperand
			else:
				#Try to first resolve (allow string based comparison)
				try:
					rightValue = resolver.resolve(self._rightOperand,metaObj)
				except:
					rightValue =  self._rightOperand

			#Try to first resolve (allow string based comparison)
			try:
				leftValue = resolver.resolve(self._leftOperand,metaObj)
			except:
				leftValue =  self._leftOperand


		#Adjusting types for numeric comparison
		if (type(rightValue) != type(leftValue)) and (self._operator not in _rangeOperators ) and (self._operator not in _collectionOperators):
			if type(leftValue) in [int,float,complex,long] and type(rightValue)==str:
				rightValue = type(leftValue)(rightValue)
			elif type(rightValue) in [int,float,complex,long] and type(leftValue)==str: 
				leftValue = type(rightValue)(leftValue)

		#for simple conditions and str Values allow only == or !=
		if (type(leftValue) == str and type(rightValue) == str) and (self._operator not in ["=","!="]):
			raise Exception("Unknown operation over string or unresolvable keyword")
		
		#Perform comparison and return value
		if self._operator == "=":
			return self._negate ^ (leftValue == rightValue)
		elif self._operator == "!=":
			return self._negate ^ (leftValue != rightValue)
		elif self._operator == ">":
			return self._negate ^ (leftValue > rightValue)
		elif self._operator == "<":
			return self._negate ^ (leftValue < rightValue)
		elif self._operator == ">=":
			return self._negate ^ (leftValue >= rightValue)
		elif self._operator == "<=":
			return self._negate ^ (leftValue <= rightValue)
		elif self._operator == "in":
			return self._negate ^ (leftValue in rightValue)
		elif self._operator == "[]":
			return self._negate ^ (Range.isInRange(leftValue,self._rightOperand))	
		elif self._operator == "{}":
			return self._negate ^ (Range.isInRangeStrict(leftValue,self._rightOperand))	
		elif self._operator == "&&":
			return self._negate ^ (leftValue and rightValue)
		elif self._operator == "||":
			return self._negate ^ (leftValue or rightValue)
		else:
			raise Exception("Unknown operator??")
