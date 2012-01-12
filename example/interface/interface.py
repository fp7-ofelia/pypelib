


'''
        @author: msune

	Simple example simulating a Server interface (e.g. rpc)
'''
import time

from SimpleXmlParser import SimpleXmlParser
'''
	RPC server interface, receives incomming request (in this example an XML request)
	Throws exception containing the messages
'''

class MyInterface():
	
	#Stupid method to show how to call functions within conditions via mappings		
	@staticmethod
	def getUserId(metaObj): #Functions always receive the metaObj
		return "lbergesio"

	@staticmethod
	def remoteMethod(credential,request):
		print request	
		try:
			#"Parse" request	
			dicReq = SimpleXmlParser.parse(request)
		
			#Invoke policy enforcement
			from MyPolicyEngine import MyPolicyEngine
			returnV = MyPolicyEngine.verify(dicReq)
		except Exception,e:
			print e
			returnV=False
		print "VERIFICATION RESULT: "+str(returnV)
		
		if returnV:
			print"Doing some fancy stuff..."
			time.sleep(2)
			print "Request process ended" 
