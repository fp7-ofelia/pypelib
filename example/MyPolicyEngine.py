
'''
        @author: msune

	Simple example Policy Engine simualting a Server interface (e.g. rpc)
 
'''

from threading import Thread, Lock
from RuleTable import RuleTable 

'''
	Uses pyPElib to build ONE RuleTable instance to apply policies to a certain scope (in this example, the interface).
	
	
'''
class  MyPolicyEngine():

	#kindof Singleton pattern
	_instance = None
	_mutex = Lock()

	#Mappings contains the basic association between keywords and objects, functions or static values
	
	_mappings = {"vm.Name":"['actions'][0]['vm']['Name']",
			"vm.RAM":"metaObj['actions'][0]['vm']['RAM']",
			"vm.HDD":"metaObj['actions'][0]['vm']['HDD']",
			"vm.OS":"metaObj['actions'][0]['vm']['OS']",
			"CA":"credentials['CA']",
			"log":"MyPolicyEngine.log(metaObj)"}
		
	@staticmethod
	def log(obj):
		print "This is a logging example"	
		
	@staticmethod
	def _getInstance():
		with MyPolicyEngine._mutex:
			if not MyPolicyEngine._instance:
				print "Loading ruletable from File..."
				MyPolicyEngine._instance = RuleTable.loadOrGenerate('MyPolicyEngine', MyPolicyEngine._mappings, "RegexParser", "RAWFile", True, fileName="database/myPolicyEngine.db") #Loading from file backend

		print "MyPolocyEngine instantiated"	
		return MyPolicyEngine._instance

	@staticmethod
	def verify(obj):
		return MyPolicyEngine._getInstance().evaluate(obj)		

	@staticmethod
	def dump():
		return MyPolicyEngine._getInstance().dump()
