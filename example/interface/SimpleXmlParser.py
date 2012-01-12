
'''
        @author: lbergesio 

	Simple XML parser using minidom for this example
 
'''

from xml.dom import minidom 

'''
	SimpleXmlParser class.
	
	
'''
class  SimpleXmlParser():


	@staticmethod
	def parse(xml):
		self = SimpleXmlParser()
		data = minidom.parseString(xml)
		actions=list()
		actiond=dict()
		rspec=dict()
		for action in self.getActions(self.getRspec(data)):
			actiond['type'] = self.getActionParams(action)['type']
			actiond['id']   = self.getActionParams(action)['id']
			actiond['vm']   = self.parseVM(action)
			actions.append(actiond)

		rspec['actions'] = actions
		return rspec
			
	def getActionParams(self,action):
		actionAttributes = ('type','id')
		atts=dict()
		l = action.attributes.items()
		for item in l:
			for att in actionAttributes:
				if item[0] == att:
					atts[item[0]]=str(item[1])
					break
		return atts
				
			
	def getRspec(self,xml):
		return xml.getElementsByTagName('rspec')[0]

	def getActions(self,rspec):
		return rspec.getElementsByTagName('action')

	def parseVM(self,action):
		vmAttributes = (('name','Name'),('ram','RAM'),('hdd','HDD'),('os','OS'),('version','Version'),('mac','MAC'),('ip','IP'))
		vmd=dict()
		for att in vmAttributes:
			try:
				vmd[att[1]] = str(action.getElementsByTagName('vm')[0].getElementsByTagName(att[0])[0].toxml().replace('<'+att[0]+'>','').replace('</'+att[0]+'>',''))
			except:
				vmd[att[1]]=''

		return vmd	
