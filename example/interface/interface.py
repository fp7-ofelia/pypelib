import sys
sys.path.append("../../src/pypelib/")


'''
        @author: msune

	Simple example simulating a Server remote method (e.g. rpc)
'''
import time
import logging
from SimpleXmlParser import SimpleXmlParser
from utils.Logger import Logger

'''
	RPC server interface, receives incomming request (in this example an XML request)
	Throws exception containing the messages
'''
logger = Logger.getLogger()

class MyInterface():
	
	#Stupid method to show how to call functions within conditions via mappings		
	@staticmethod
	def getUserId(metaObj): #Functions always receive the metaObj
		return "lbergesio"

	@staticmethod
	def remoteMethod(credential,request):
		logger.info(request)	
		try:
			#"Parse" request	
			dicReq = SimpleXmlParser.parse(request)
		
			#Invoke policy enforcement
			from MyPolicyEngine import MyPolicyEngine
			returnV = MyPolicyEngine.verify(dicReq)
		except Exception,e:
			logger.error(str(e))
			returnV=False
		logger.info("VERIFICATION RESULT: %s",str(returnV))
		
		if returnV:
			logger.info("Doing some fancy stuff...")
			time.sleep(2)
			logger.info("Request process ended") 
