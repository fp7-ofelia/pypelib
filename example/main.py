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


from pypelib.RuleTable import RuleTable
from MyPolicyEngine import MyPolicyEngine
from interface.interface import MyInterface
from pypelib.utils.Logger import Logger
from pypelib.persistence.backends.rawfile.RAWFile import RAWFile

logger = Logger.getLogger()


def addRuleAndDump(rule):
        if rule:
                logger.info("\nAdding a Rule to Policy Engine")
                MyPolicyEngine.getInstance().addRule(rule)
        logger.info("\nDumping table state...")
        logger.info("[RULETABLE]######################################################################")
        MyPolicyEngine.dump()
        logger.info("[RULETABLE]######################################################################\n")
        time.sleep(5)


def call(message, cred, xml):
        # Simulating throwing first query to the interface
        logger.info("%s", message)
        logger.info("Message: ope")
        try:
                logger.info("Simulating query...")
                MyInterface.remoteMethod(cred, xml)
        except Exception, e:
                logger.error("Query failed")
                logger.error(str(e))

        logger.info("-----")
        time.sleep(2)


'''
        Creating RawFile for database
'''


# Generate a simple RuleTable and store
def generateSimpleRuleTable():
        return RuleTable("MyPolicyEngine", None, "RegexParser", "RAWFile", False, False)


myTable = generateSimpleRuleTable()
# Testing with the driver directly
RAWFile.save(myTable, "RegexParser", fileName="./database/myPolicyEngine.db")
time.sleep(3)

'''
         Simulating instantiation of main engine, to call interface afterwards
'''

logger.info("Dumping inital table state...\n")
addRuleAndDump(None)

addRuleAndDump("if ( vm.RAM < 512 ) then accept do log denyMessage Memory is greater than 512 MB #Preventing VMs with more than 512 MB")

'''
         Simulating client
'''
# Generating requests
credential = {'CA':'i2CAT', 'user':'lbergesio'}
ope = open('interface/example1.xml', 'r').read()
ope2 = open('interface/example2.xml', 'r').read()

call("First query", credential, ope)
call("Second query", credential, ope2)

addRuleAndDump("if ( vm.RAM > 128 ) && (user.id = lbergesio) then deny denyMessage User is not able to instantiate VMs with more than 128 MB of memory #lbergesio specific rule")
logger.info("Now moving rule on top (will forbbid user)")
MyPolicyEngine.getInstance().moveRule(0, index=1)
addRuleAndDump(None)

call("Third query", credential, ope)
