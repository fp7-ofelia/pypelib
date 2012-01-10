


'''
        @author: msune

	Simple example simualting a Server interface (e.g. rpc)
'''

from MyPolicyEngine import MyPolicyEngine

'''
	RPC server interface, receives incomming request (in this example an XML request)	
	Throws exception containing the messages
'''

def myInterface(request):
	
	#"Parse" request	
	#xmlReq = parse()
	
	#Invoke policy 
	MyPolicyEngine.evaluate(xmlReq)

	print "Request was verified. Doing some fancy stuff..."
	time.sleep(2)
	print "Request process ended" 
