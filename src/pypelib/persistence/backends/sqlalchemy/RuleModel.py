from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR, TINYINT

from utils.commonbase import Base


'''
        @author: SergioVidiella
        @organization: i2CAT, OFELIA FP7

        SQLAlchemy Rule Model class
'''

#XXX: SQLAlchemy is required to run this model
class PolicyRuleModel(Base):

    __tablename__ = 'pypelib_RuleModel'

    id = Column(Integer, autoincrement=True, primary_key=True)
    RuleUUID = Column(VARCHAR(length=512), default="", nullable=False) # uuid
    RuleTableName = Column(VARCHAR(length=512), default="", nullable=True) #Table Name
    Rule = Column(VARCHAR(length=2048), default="", nullable=True)
    RuleIsEnabled = Column(TINYINT(1))# Enabled or disabled Rule
    RulePosition = Column(VARCHAR(length=512), default="", nullable=False)#Position in RuleSet

