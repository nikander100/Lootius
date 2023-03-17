import sqlite3
import csv, time, sqlalchemy, typing, sys
from lootius.models.databaseModel import Base
from sqlite3 import Error

class SetupDatabase:
    def __init__(self):
        pass

    def _dropDatabase(self):
        lootiusDB = Base()
        engine = sqlalchemy.create_engine("sqlite+pysqlite:///lootius/database/lootiusTest.db", echo=True)
        lootiusDB.metadata.drop_all(engine)
        

    def setupDatabase(self, dbFilePath):
        lootiusDB = Base()
        try:
            engine = sqlalchemy.create_engine(f"sqlite+pysqlite://{dbFilePath}", echo=True)
        except Error as e:
            print(e)  ;"""log to errors, have to find out what the error return is from alchemy"""
        finally:
            lootiusDB.metadata.create_all(engine)

testDB = SetupDatabase()
testDB.setupDatabase("/lootius/database/lootiusTest.db")
# time.sleep(1)
# testDB._dropDatabase()
