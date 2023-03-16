import sqlite3
import csv, time, sqlalchemy, typing
from databaseModel import Base
from sqlite3 import Error

class SetupDatabase:
    def __init__(self):
        pass

    def _dropDatabase():
        lootiusDB = Base()
        engine = sqlalchemy.create_engine("sqlite+pysqlite:///data/lootiusTest.db", echo=True)
        lootiusDB.metadata.drop_all(engine)
        

    def setupDatabse(dbFilePath):
        lootiusDB = Base()
        try:
            engine = sqlalchemy.create_engine(f"sqlite+pysqlite://{dbFilePath}", echo=True)
        except Error as e:
            print(e)  ;"""log to errors, have to find out what the error return is from alchemy"""
        finally:
            lootiusDB.metadata.create_all(engine)

SetupDatabase.setupDatabse("/lootius/database/lootiusTest.db")
# SetupDatabase._dropDatabase()