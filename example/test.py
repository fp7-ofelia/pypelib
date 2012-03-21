from src.RuleTable import*
from src.persistence.PersistenceEngine import*
from cPickle import loads, dumps


table = RuleTable("My table",{"vm.memory":"metaObj['memory']","project.vms":"metaObj['vms']","project.string":"metaObj['string']"},'RegexParser','Write',True,False,'333')
t2 = RuleTable("My table2",{"project.vms":"metaObj['vms']","project.string":"metaObj['string']"},'RegexParser','Write',True,True,'111')
s3 = RuleTable("My table3",{"project.string":"metaObj['string']"},'RegexParser','Write',False,True,'000')



#Adding dummy rule
#from Condition import Condition
#table.addRule(Rule(Condition("5","6","<"),"Description"))      

table.addRule('In My table with enabled state if vm.memory < 2000 then accept do project.string denyMessage You requested more that 2GB of RAM # descr')
t2.addRule('In My table2 with enabled state if project.vms > 2 then deny nonterminal do project.string denyMessage You requested more that 2 of vms # descr')



#table.addRule(Rule(Condition("vm.memory","2000",">"),"Memory", "Action forbbiden: You requested more that 2GB of RAM" ,Rule.NEGATIVE_TERMINAL))
#table.addRule(Rule(Condition("project.vms","4",">="),"VMs","Action forbidden: you have 4 VMs already in the project",Rule.NEGATIVE_TERMINAL))
#table.addRule(Rule(Condition("project.string","try","!="),"String","Action forbidden: String",Rule.NEGATIVE_TERMINAL))
#for rule in table._ruleSet:
#	print rule._matchAction

table.dump()
t2.dump()
s3.dump()
#table.save()

metaObj = {"memory":200,"vms":"1","string":"try2"}
metaObj2 = {"memory":20000,"vms":"3","string":"try2"}


#Create the metaObj

#try:
 #      table.process(metaObj)
#except Exception as e:
#       print e 

#t2 = RuleTable("My table2",{"project.vms":"metaObj['vms']","project.string":"metaObj['string']"},'RegexParser','Write',False,True,'111')

