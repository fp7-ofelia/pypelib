import os
import sys
import time
import exceptions
import time
import logging

sys.path.append("../src/pypelib/") 

'''
        @author: msune, lbergesio,cbermudo,omoya

	Simple example to emulate Server/client side interaction
 
'''


from RuleTable import RuleTable
from MyPolicyEngine import MyPolicyEngine
from interface.interface import MyInterface

logging.basicConfig(format='%(asctime)s %(message)s')
def addRuleAndDump(rule):
	if rule:
		logging.info("\nAdding a Rule to Policy Engine")
		MyPolicyEngine.getInstance().addRule(rule)
	logging.info("\nDumping table state...")
	logging.info("[RULETABLE]######################################################################")
	MyPolicyEngine.dump()
	logging.info("[RULETABLE]######################################################################\n")
	time.sleep(5)

def call(message,cred,xml):
	#Simulating throwing first query to the interface
	logging.info("%s",message)
	logging.info("Message: ope")
	try:
		logging.info("Simulating query...")
		MyInterface.remoteMethod(cred,xml)
	except Exception,e:
		logging.error("Query failed")
		logging.error(str(e))

	logging.info("-----")
	time.sleep(2)

'''
	Simulating instantiation of main engine, to call interface afterwards
'''
logging.info("Dumping inital table state...\n")
addRuleAndDump(None)

addRuleAndDump("if ( vm.RAM < 512 ) then accept do log denyMessage Memory is greater than 512 MB #Preventing VMs with more than 512 MB")

'''
	Simulating client
'''
#Generating requests
credential = {'CA':'i2CAT','user':'lbergesio'}
ope = open('interface/example1.xml','r').read()
ope2 = open('interface/example2.xml','r').read()



call("First query",credential,ope)
call("Second query",credential,ope2)

addRuleAndDump("if ( vm.RAM > 128 ) && (user.id = lbergesio) then deny denyMessage User is not able to instantiate VMs with more than 128 MB of memory #lbergesio specific rule")
logging.info("Now moving rule on top (will forbbid user)")
MyPolicyEngine.getInstance().moveRule(0,index=1)
addRuleAndDump(None)

call("Third query",credential,ope)

