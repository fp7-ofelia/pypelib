from SimpleXmlParser import SimpleXmlParser
xml = open("example1.xml").read()
rspec = SimpleXmlParser.parse(xml)
print rspec

