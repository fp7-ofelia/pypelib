import sys
from random import * 
sys.path.append("../../src/") 

from RuleTable import RuleTable 


_mappings = {"vm.Name":"metaObj['Name']",
			"vm.RAM":"metaObj['RAM']",
			"vm.HDD":"metaObj['HDD']",
			"vm.OS":"metaObj['OS']",
			"vm.Version":"metaObj['Version']",
			"vm.MAC":"metaObj['MAC']",
			"vm.IP":"metaObj['IP']",
			"organization":"metaObj['organization']"}
	
table = RuleTable("myTable",_mappings,"RegexParser","RAWFile",False,False)

#Add dummy rules
table.addRule("if  vm.RAM <= 256  then accept term # Accept RAM < 256")
table.addRule("if  (organization = A) && (vm.RAM <1024)  then accept term # Extended limit for organization A")

#Dump current table
table.dump()

metaObj1 = {"RAM":1024,"organization":"B"}
metaObj2 = {"RAM":1024,"organization":"A"}

print "\n"

print "trying with org B"
try:
	table.evaluate(metaObj1)
	print "OK!"
except Exception as e:
	print e	

metaObj1 = {"RAM":1024,"organization":"B"}
metaObj2 = {"RAM":1024,"organization":"A"}

print "trying with org A"
try:
	table.evaluate(metaObj1)
	print "OK!"
except Exception as e:
	print e	
