import sys
from random import * 
sys.path.append("../../src/") 

from pypelib.Condition import Condition,Collection,Range 

_collectionOperators= ["in"]
_logicalOperators = ["&&","||"]
_rangeOperators = ["[]","{}"]
_comparisonOperators = ["=","!=",">","<",">=","<="]

##Unit testing

#test comp operators
def createSimpleCompCondition(op=None):
	if op:
		Condition(randint(0,100),randint(0,100), op,bool(getrandbits(1)))	
	return Condition(randint(0,100),randint(0,100), _comparisonOperators[randint(0,len(_comparisonOperators)-1)],bool(getrandbits(1)))
def testComparisonOperators():
	print "COMP OPs"
	for op in _comparisonOperators:
		a = createSimpleCompCondition(op) 
		print "Condition: "+a.dump()+" result: "+str(a.evaluate(None,None))

#test collection
def testCollectionOperator():
	print "COLLECTION OPs"

	neg = bool(getrandbits(1))
	item = randint(0,10)
	elements = list()

	for i in range(5):	
		elements.append(randint(0,10)) 
	
	a = Condition(item,Collection(elements), "in",neg)
	print "Condition: "+a.dump()+" result: "+str(a.evaluate(None,None))
		
	
#test boolean
def testBooleanOperators():
	for op in _logicalOperators:
		neg = bool(getrandbits(1))
		a = Condition(createSimpleCompCondition(),createSimpleCompCondition(),op,neg)
		print "Condition: "+a.dump()+" result: "+str(a.evaluate(None,None))

#range operators
def testRangeOperators():
	print "RANGE OPs"
	
	for op in _rangeOperators:
		neg = bool(getrandbits(1))
		item = randint(0,40)
		rang = Range(0,randint(20,30)) 
		a = Condition(item,rang,op,neg)
		print "Condition: "+a.dump()+" result: "+str(a.evaluate(None,None))
			

#perform test
testComparisonOperators()
testBooleanOperators()
testCollectionOperator()
testRangeOperators()
