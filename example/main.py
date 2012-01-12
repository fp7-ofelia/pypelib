import os
import sys
import time
import exceptions
import time

sys.path.append("../src/") 

from RuleTable import RuleTable
from MyPolicyEngine import MyPolicyEngine
from interface import myInterface

print "Dumping inital table state..."
MyPolicyEngine.dump()
time.sleep(1)


#Adding a Rule to out Policy Engine
MyPolicyEngine._getInstance().addRule("if ( vm.RAM > 128 ) && (vm.RAM <1024) then accept do pass denyMessage Memory is less than 128 MB or exceeds 1024MB")

credential = {'CA':'i2CAT','user':'lbergesio'}
ope = open('example1.xml','r').read()

#Simulating throwing first query to the interface
try:
	print "Simulating first query..."
	myInterface(credential,ope)
except Exception,e:
	print "First query failed"
	print str(e)

time.sleep(1)



#Throwing second query
#try:
#	print "Simulating second query..."
#        interface(credential,ope)
#except Exception,e:
#        print "Second query failed"
#        print str(e)
#
#time.sleep(1)
##Adding a rule & throwing first query again
#print "Adding a new rule..."
#Table1.addRule(rule22)
#print "Dumping table state..."
#MyPolicyEngine.dump()
#time.sleep(1)
#
#try:
#	print "Simulating third query..."
#        interface(credential,ope)
#except Exception,e:
#        print "First query failed the second time"
#        print str(e)
#
