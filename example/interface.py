


'''
        @author: msune

	Simple example simualting a Server interface (e.g. rpc)
'''

from MyPolicyEngine import MyPolicyEngine
from SimpleXmlParser import SimpleXmlParser
'''
	RPC server interface, receives incomming request (in this example an XML request)	
	Throws exception containing the messages
'''

def myInterface(request):
	
	#"Parse" request	
	dicReq = SimpleXmlParser(request)
	
	#Invoke policy 
	MyPolicyEngine.evaluate(dictReq)

	print "Request was verified. Doing some fancy stuff..."
	time.sleep(2)
	print "Request process ended" 
