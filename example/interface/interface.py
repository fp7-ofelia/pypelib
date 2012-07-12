


'''
        @author: msune

	Simple example simulating a Server remote method (e.g. rpc)
'''
import time
import logging
from SimpleXmlParser import SimpleXmlParser
'''
	RPC server interface, receives incomming request (in this example an XML request)
	Throws exception containing the messages
'''
logging.basicConfig(format='%(asctime)s %(message)s')

class MyInterface():
	
	#Stupid method to show how to call functions within conditions via mappings		
	@staticmethod
	def getUserId(metaObj): #Functions always receive the metaObj
		return "lbergesio"

	@staticmethod
	def remoteMethod(credential,request):
		logging.info(request)	
		try:
			#"Parse" request	
			dicReq = SimpleXmlParser.parse(request)
		
			#Invoke policy enforcement
			from MyPolicyEngine import MyPolicyEngine
			returnV = MyPolicyEngine.verify(dicReq)
		except Exception,e:
			logging.error(str(e))
			returnV=False
		logging.info("VERIFICATION RESULT: %s",str(returnV))
		
		if returnV:
			logging.info("Doing some fancy stuff...")
			time.sleep(2)
			logging.info("Request process ended") 
