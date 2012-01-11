import sys
from random import * 
sys.path.append("../../src/") 

from Rule import Rule
from parsing.drivers.RegexParser import RegexParser 


#parser.parseCondition("A not      in collection  {B}")
#parser.parseCondition("A!=B")
#parser.parseRule(" if  not A in collection {2,3,4}  then accept term do C # dd")
#rule = parser.parseRule(" if  not a>5   then accept term do something denyMessage ksdfkdfskf # comment")
rule = RegexParser.parseRule(" if  not (a>5) && (B = 5)   then accept term do something denyMessage ksdfkdfskf # comment")
print rule.dump()

import pprint
pprint.pprint(rule.getType())
#print rule.dump()

#print RegexParser.craftRule(rule)
