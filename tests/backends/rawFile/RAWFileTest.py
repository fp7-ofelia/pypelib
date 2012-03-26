import sys
import time
from random import * 
sys.path.append("../../../src/") 

from persistence.drivers.rawfile.RAWFile_old import RAWFile
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
