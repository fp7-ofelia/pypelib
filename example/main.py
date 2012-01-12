import os
import sys
import time
import exceptions
import time

sys.path.append("../src/") 

from RuleTable import RuleTable
from MyPolicyEngine import MyPolicyEngine
from interface import myInterface

def addRuleAndDump(rule):
	print "\nAdding a Rule to Policy Engine"
	if rule:
		MyPolicyEngine._getInstance().addRule(rule)
	print "\nDumping table state..."
	print "######################################################################"
	MyPolicyEngine.dump()
	print "######################################################################\n"
	time.sleep(1)

def call(message,xml,cred):
	#Simulating throwing first query to the interface
	print "%s"%message
	print "Message: ope"
	try:
		print "\Simulating query..."
		print "->>>>>>>"
		myInterface(cred,xml)
	except Exception,e:
		print "Query failed"
		print str(e)

	print "<<<<<<<--"
	time.sleep(1)

'''
	Simulating instantiation of main engine, to call interface afterwards
'''
print "Dumping inital table state...\n"
addRuleAndDump(None)

addRuleAndDump("if ( vm.RAM < 512 ) then deny do log denyMessage Memory is more than 512 MB")

'''
	Simulating client
'''
#Generating requests
credential = {'CA':'i2CAT','user':'lbergesio'}
ope = open('example1.xml','r').read()
ope2 = open('example2.xml','r').read()



call("First query",credential,ope2)
call("Second query",credential,ope2)

addRuleAndDump("if ( vm.RAM > 128 ) then deny do pass denyMessage Memory is more than 128 MB")

call("Third query",credential,ope)

