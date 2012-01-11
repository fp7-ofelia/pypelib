import sys
import time
from random import * 
sys.path.append("../../src/") 

from parsing.drivers.RegexParser import RegexParser

def parseDumpAndCraft(s):
	rule =RegexParser.parseRule(s)
	print "Original: "+s
	print "Dumping: "+rule.dump()
	print "Craft: "+RegexParser.craftRule(rule)
	print "---------"

print "\n\nCOLLECTIONS:"
#collections
parseDumpAndCraft(" if  A in collection {2,3,4}  then accept ")
parseDumpAndCraft(" if  not A in collection {2,3,4}  then deny do C # dd")
parseDumpAndCraft(" if  A not in collection {2,3,4}  then accept do C denyMessage ksdfkdfskf  # dd")

print "\n\nRANGE NO STRICT:"
#range no strict
parseDumpAndCraft(" if   A in range [2,4]  then accept")
parseDumpAndCraft(" if  not A in range [2,4]  then accept do C # dd")
parseDumpAndCraft(" if   A not in range [2,4]  then deny do C # dd")

print "\n\nRANGE  STRICT:"
#range no strict
parseDumpAndCraft(" if   A in range {2,4}  then accept do C # dd")
parseDumpAndCraft(" if  not A in range {2,4}  then accept do C # dd")
parseDumpAndCraft(" if   A not in range {2,4}  then accept do C # dd")


print "\n\nSIMPLE :"
#simple
parseDumpAndCraft(" if ( not a>5 ) then accept nonterminal do something denyMessage ksdfkdfskf # comment")
parseDumpAndCraft(" if ( not a>5 ) then accept do something denyMessage ksdfkdfskf # comment")

print "\n\nCOMPLEX:"
#complex
parseDumpAndCraft(" if  ( (a>5) && (B = 5)) && ((a<4)&&(b!=5))   then accept nonterminal do something denyMessage ksdfkdfskf # comment")
parseDumpAndCraft(" if   ( (( (a>5) && (B = 5)) || (a=b) ) && ((a<4)&&(b!=5)))   then deny do something denyMessage ksdfkdfskf # comment")
parseDumpAndCraft(" if   ( (( (a>5) && (B in range [2,3])) || (a=b) ) && ((a<4)&&(b!=5)))   then accept nonterminal do something denyMessage ksdfkdfskf # comment")

