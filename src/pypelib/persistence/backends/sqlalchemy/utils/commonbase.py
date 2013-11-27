from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pypelib.persistence.backends.sqlalchemy.settings import *

'''@author: SergioVidiella'''

#A Common Base for the table models
Base = declarative_base()

#A Common Session manager for all the querys
ENGINE = DATABASE_DIALECT+DATABAE_DRIVER+"://"+DATABASE_USER+":"+DATABASE_PASSWORD+"@"+DATABASE_HOST+"/"+DATABASE_NAME
db_engine = create_engine(ENGINE, pool_recycle=6000)
db_session_factory = sessionmaker(autoflush=True, bind=db_engine, expire_on_commit=False) # the class which can create sessions (factory pattern)
DB_SESSION = scoped_session(db_session_factory) # still a session creator, but it will create _one_ session per thread and delegate all method calls to it

