import sys
import time
from random import *
try:
   import cPickle as pickle
except:
   import pickle
 
sys.path.append("../../../src/") 

#from persistence.drivers.rawfile.RAWFile_old import RAWFile
from persistence.backends.rawfile.RAWFile import RAWFile
from RuleTable import RuleTable


#Generate a simple RuleTable and store
def generateSimpleRuleTable():
	return RuleTable("myTable",None,"RegexParser","RAWFile",False,False)

myTable = generateSimpleRuleTable()

#Testing with the driver directly
RAWFile.save(myTable, "RegexParser",fileName="/tmp/myTable.dat")

time.sleep(3)

myTable2 = RAWFile.load("myTable",None,fileName="/tmp/myTable.dat")
	

print "Objects equal:"+str(myTable==myTable2)
print "Objects equal:"+str(myTable==myTable2)
print myTable.uuid
print myTable2.uuid
print myTable.name
print myTable2.name
print myTable._persist
print myTable2._persist
print myTable._parser
print myTable2._parser
print myTable._persistenceBackend
print myTable2._persistenceBackend
print myTable._persistenceBackendParameters
print myTable2._persistenceBackendParameters
print myTable._policy
print myTable2._policy
print myTable._ruleSet
print myTable2._ruleSet
print myTable._mappings
print myTable2._mappings
print myTable._mutex
print myTable2._mutex
print myTable._resolver
print myTable2._resolver

