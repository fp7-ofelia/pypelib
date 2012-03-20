import os
import sys
import time
import exceptions

from pypelib.src.RuleTable import RuleTable
from VM import VM

vm1 = VM('MyVM',512,2048,'Ubuntu',10.0,'AC-AC-AC-AC-AC-AC','192.168.1.127')
vm2 = VM('MyVM2',1024,4096,'Ubuntu',11.04,'BC-BC-BC-BC-BC-BC','192.168.1.127')
metaObj = vm1.dump()
metaObj2 = vm2.dump()

Parser = 'RegexParser'
Persistence = 'Write'
doPersistence = True
Mappings = {"vm.Name":"metaObj['Name']","vm.RAM":"metaObj['RAM']","vm.HDD":"metaObj['HDD']","vm.OS":"metaObj['OS']","vm.Version":"metaObj['Version']","vm.MAC":"metaObj['MAC']","vm.IP":"metaObj['IP']"}

Table1 = RuleTable('Table1', Mappings, Parser, Persistence, doPersistence, True,'333')

rule = 'In Table1 with disabled state if vm.RAM > 1024 then deny nonterminal do vm.OS  denyMessage You requested more than 1024 MB of RAM #RAM memory rule'
rule2 = 'In Table1 with disabled state if vm.HDD > 2048 then deny do vm.OS  denyMessage You requested more than 2048 MB of HDD #RAM memory rule'

Table1.addRule(rule)

Table1.dump()
