import os
import sys
import time
from django.db import models



'''
        @author: msune,omoya
	@organization: i2CAT, OFELIA FP7

	Django Rule Model class
'''

#XXX: Django is required to run this model
class PolicyRuleModel(models.Model):
	class Meta:
		"""Machine exportable class"""
		app_label = 'pypelib'
		db_table = 'pypelib_RuleModel'

	RuleUUID = models.CharField(max_length = 512, default="") # uuid
	RuleTableName = models.CharField(max_length = 512, default="", blank = True, null = True )#Table Name
	Rule = models.CharField(max_length = 2048, default="", blank =True, null =True)
	RuleIsEnabled = models.BooleanField()# Enabled or disabled Rule
	RulePosition = models.CharField(max_length = 512, default = "")#Position in RuleSet




