import os
import sys
import time
from django.db import models



'''
        @author: lbergesio,omoya,CarolinaFernandez
	@organization: i2CAT, OFELIA FP7
	

        Django RuleTable Model class
'''
#Django is required to run this model
class PolicyRuleTableModel(models.Model):
        class Meta:
                """RuleTable model class"""
                app_label = 'pypelib'
                db_table = 'pypelib_RuleTableModel'

        type = models.CharField(max_length = 16, default="") #terminal/non terminal
        uuid = models.CharField(max_length = 512, default="") # uuid
        name = models.TextField(max_length = 120, default="") # name
	# FIXME: set 'name' to 'unique', but that seems only possible with 'CharField'
        #name = models.CharField(max_length = 120, default="", unique=True) # name
        defaultParser = models.CharField(max_length = 64, default="", blank =True, null =True)
        defaultPersistence = models.CharField(max_length = 64, default="", blank =True, null =True)
        defaultPersistenceFlag = models.BooleanField()

