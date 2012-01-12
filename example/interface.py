


'''
        @author: msune

	Simple example simulating a Server interface (e.g. rpc)
'''
import time
from MyPolicyEngine import MyPolicyEngine
from SimpleXmlParser import SimpleXmlParser
'''
	RPC server interface, receives incomming request (in this example an XML request)
	Throws exception containing the messages
'''

def myInterface(credential,request):
	print request	
	try:
		#"Parse" request	
		dicReq = SimpleXmlParser.parse(request)
	
		#Invoke policy enforcement
		MyPolicyEngine.verify(dicReq)
	except Exception,e:
		print e
		raise e

	print "Request was verified. Doing some fancy stuff..."
	time.sleep(2)
	print "Request process ended" 
