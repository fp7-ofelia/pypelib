import os
import sys
import time
import exceptions
import time

from src.RuleTable import RuleTable


print "Dumping inital table state..."
MyPolicyEngine.dump()
time.sleep(1)

#Simulating throwing first query to the interface
try:
	print "Simulating first query..."
	interface(credential,ope)
except Exception,e:
	print "First query failed"
	print str(e)

time.sleep(1)
#Throwing second query
try:
	print "Simulating second query..."
        interface(credential,ope)
except Exception,e:
        print "Second query failed"
        print str(e)

time.sleep(1)
#Adding a rule & throwing first query again
print "Adding a new rule..."
Table1.addRule(rule22)
print "Dumping table state..."
MyPolicyEngine.dump()
time.sleep(1)

try:
	print "Simulating third query..."
        interface(credential,ope)
except Exception,e:
        print "First query failed the second time"
        print str(e)

