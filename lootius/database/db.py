from sqlalchemy.orm import sessionmaker
from lootius.database.setup import Setup
from lootius.models.databaseModel import Base
import os, sys, time, sqlalchemy
from os.path import realpath, join, dirname, abspath

class DB:
    dbFilePath = realpath(join(dirname(abspath(__file__)), ".", "lootiusTest.db"))
    print(dbFilePath)
    engine = sqlalchemy.create_engine(f"sqlite+pysqlite:///{dbFilePath}", echo=True)
    def __init__(self):
        pass

    #Returns new session
    @classmethod
    def getSession(self):
        return (sessionmaker(self.engine))
    
    @classmethod
    def dropAll(self):
        sqlalchemy.MetaData.drop_all(Base.metadata, bind=self.engine)