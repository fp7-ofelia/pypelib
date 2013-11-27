from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, LONGTEXT

from utils.commonbase import Base


'''
        @author: SergioVidiella
        @organization: i2CAT, OFELIA FP7
        

        SQLAlchemy RuleTable Model class
'''

#SQLAlchemy is required to run this model
class PolicyRuleTableModel(Base):

    __tablename__ = 'pypelib_RuleTableModel'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(VARCHAR(length=16), default="", nullable=False) #terminal/non terminal
    uuid = Column(VARCHAR(length=512), default="", nullable=False) # uuid
    name = Column(LONGTEXT, default="", nullable=False) # name
    defaultParser = Column(VARCHAR(length=64), default="", nullable =True)
    defaultPersistence = Column(VARCHAR(length=64), default="", nullable =True)
    defaultPersistenceFlag = Column(TINYINT(1))

