import os
import sys
import time
import exceptions
import time

sys.path.append("../src/") 

from RuleTable import RuleTable
from MyPolicyEngine import MyPolicyEngine
from interface.interface import MyInterface

def addRuleAndDump(rule):
	if rule:
		print "\nAdding a Rule to Policy Engine"
		MyPolicyEngine.getInstance().addRule(rule)
	print "\nDumping table state..."
	print "[RULETABLE]######################################################################"
	MyPolicyEngine.dump()
	print "[RULETABLE]######################################################################\n"
	time.sleep(5)

def call(message,cred,xml):
	#Simulating throwing first query to the interface
	print "%s"%message
	print "Message: ope"
	try:
		print "Simulating query..."
		MyInterface.remoteMethod(cred,xml)
	except Exception,e:
		print "Query failed"
		print str(e)

	print "-----"
	time.sleep(2)

'''
	Simulating instantiation of main engine, to call interface afterwards
'''
print "Dumping inital table state...\n"
addRuleAndDump(None)

addRuleAndDump("if ( vm.RAM < 512 ) then accept do log denyMessage Memory is greater than 512 MB")

'''
	Simulating client
'''
#Generating requests
credential = {'CA':'i2CAT','user':'lbergesio'}
ope = open('interface/example1.xml','r').read()
ope2 = open('interface/example2.xml','r').read()



call("First query",credential,ope)
call("Second query",credential,ope2)

addRuleAndDump("if ( vm.RAM > 128 ) && (user.id = lbergesio) then deny denyMessage User is not able to instantiate VMs with more than 128 MB of memory")
print "Now moving rule on top (will forbbid user)"
MyPolicyEngine.getInstance().moveRule(0,index=1)
addRuleAndDump(None)

call("Third query",credential,ope)

