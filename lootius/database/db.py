from sqlalchemy.orm import sessionmaker, scoped_session
from lootius.database.setup import Setup
from lootius.models.databaseModel import Base
import sqlalchemy
from os.path import realpath, join, dirname, abspath

# TODO get path from config
dbFilePath = realpath(join(dirname(abspath(__file__)), ".", "lootiusTest.db"))
print(dbFilePath)
engine = sqlalchemy.create_engine(f"sqlite+pysqlite:///{dbFilePath}", echo=True)
SessionFactory = sessionmaker(engine)
LocalSession = scoped_session(SessionFactory)

class DB:
    # class is posisbly deprecated as the file acts as the module
    def __init__(self):
        pass

    #Returns new session DEPRECATED
    @classmethod
    def getSession(self):
        """Returns new Session.
        For the given session can also start: with Session. and include begin()/commit()/rollback()
        then dont have to commit, etc. manually"""
        return (sessionmaker(engine))
    
    @classmethod
    def dropAll(self):
        sqlalchemy.MetaData.drop_all(Base.metadata, bind=engine)