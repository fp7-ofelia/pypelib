import os
import sys
import time
import exceptions



class VM():
	
	#Basic Atributes
	_name = None
	_RAM = None
	_OS = None
	_version = None
	_MAC = None
	_IP = None
	_HDD = None
	
	#Getters
	def getName(self):
		return self._name

	def getRAM(self):
		return self._RAM

	def getOS(self):
		return self._OS

	def getVersion(self):
		return self._version
	
	def getMAC(self):
		return self._MAC
	
	def getIP(self):
		return self._IP
	
	def getHDD(self):
		return self._HDD

	def __init__(self,name,RAM,HDD,OS,version,MAC=None,IP=None):
		
		self._name = name
       	 	self._RAM = RAM
		self._HDD = HDD
        	self._OS = OS
		self._version = version
        	self._MAC = MAC
        	self._IP = IP
	
	def dump(self):

		metaObj  = {'Name':self._name, 'RAM':self._RAM, 'HDD':self._HDD, 'OS':self._OS, 'Version':self._version, 'MAC':self._MAC, 'IP':self._IP}
		return metaObj
		
