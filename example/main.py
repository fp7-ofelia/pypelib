import os
import sys
import time
import exceptions
import time

sys.path.append("../src/") 

from RuleTable import RuleTable
from MyPolicyEngine import MyPolicyEngine
from interface import myInterface

print "######################################################################\n"
print "Dumping inital table state...\n"
MyPolicyEngine.dump()
time.sleep(1)

#Generating requests
credential = {'CA':'i2CAT','user':'lbergesio'}
ope = open('example1.xml','r').read()
ope2 = open('example2.xml','r').read()


print "######################################################################\n"
#Adding a Rule to out Policy Engine
print "\nAdding a Rule to Policy Engine"
MyPolicyEngine._getInstance().addRule("if ( vm.RAM > 512 ) then deny do pass denyMessage Memory is more than 512 MB")
print "\nDumping table state..."
MyPolicyEngine.dump()

 
print "######################################################################\n"
#Simulating throwing first query to the interface
print "\nFirst query is:\n"
print ope
try:
	print "\nSimulating first query..."
	myInterface(credential,ope)
except Exception,e:
	print "\nFirst query failed"
	print str(e)

time.sleep(1)

print "######################################################################\n"
print "\nSecond query is:\n"
print ope2
#Throwing second query
try:
	print "\nSimulating second query..."
        myInterface(credential,ope2)
except Exception,e:
        print "\nSecond query failed"
        print str(e)

time.sleep(1)

print "######################################################################\n"
#Adding a rule & throwing first query again
print "\nAdding a Rule to Policy Engine"
MyPolicyEngine._getInstance().addRule("if ( vm.RAM > 128 ) then deny do pass denyMessage Memory is more than 128 MB")
print "\nDumping table state..."
MyPolicyEngine.dump()
time.sleep(1)

try:
	print "\nSimulating third query..."
	myInterface(credential,ope)
except Exception,e:
	print "\nFirst query failed the second time"
	print str(e)

