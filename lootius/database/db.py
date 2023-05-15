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

def getSession():
    """Returns new Session.
    For the given session can also start: with Session. and include begin()/commit()/rollback()
    then dont have to commit, etc. manually"""
    return (sessionmaker(engine))
    

def dropAll():
    sqlalchemy.MetaData.drop_all(Base.metadata, bind=engine)