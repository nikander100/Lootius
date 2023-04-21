from sqlalchemy.orm import sessionmaker
from lootius.database.setup import Setup
from lootius.models.databaseModel import Base
import os, sys, time, sqlalchemy
from os.path import realpath, join, dirname, abspath

class DB:
    # TODO get path from config
    dbFilePath = realpath(join(dirname(abspath(__file__)), ".", "lootiusTest.db"))
    print(dbFilePath)
    engine = sqlalchemy.create_engine(f"sqlite+pysqlite:///{dbFilePath}", echo=True)
    def __init__(self):
        pass

    #Returns new session
    @classmethod
    def getSession(self):
        """Returns new Session.
        For the given session can also start: with Session. and include begin()/commit()/rollback()
        then dont have to commit, etc. manually"""
        return (sessionmaker(self.engine))
    
    @classmethod
    def dropAll(self):
        sqlalchemy.MetaData.drop_all(Base.metadata, bind=self.engine)