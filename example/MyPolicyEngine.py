
'''
        @author: msune

	Simple example Policy Engine simualting a Server interface (e.g. rpc)
 
'''

from src.RuleTable import RuleTable 

'''
	Uses pyPElib to build ONE RuleTable instance to apply policies to a certain scope (in this example, the interface).
	
	
'''
class  MyPolicyEngine():

	#kindof Singleton pattern
	_instance = None
	_mutex = Lock()

	#Mappings contains the basic association between keywords and objects, functions or static values
	
	_mappings = {"vm.Name":"metaObj['Name']",
			"vm.RAM":"metaObj['RAM']",
			"vm.HDD":"metaObj['HDD']",
			"vm.OS":"metaObj['OS']",
			"vm.Version":"metaObj['Version']",
			"vm.MAC":"metaObj['MAC']",
			"vm.IP":"metaObj['IP']"
			"organization":"credentials['organization']"}
	
	@staticMethod
	def _getInstance():
		with self._mutex:
			if self._instance = None
				print "Loading ruletable from File..."
				self._instance = RuleTable.load('Table1') #Loading from file backend
		
		return self._instance

	@staticMethod
	def verify(obj):
		return self._getInstance().evaluate(obj)		

	@staticMethod
	def dump():
		return self._getInstance().dump()
