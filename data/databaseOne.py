import sqlite3
import csv, time, sqlalchemy, typing
from databaseModel import Base
from sqlite3 import Error

lootiusDB = Base()
engine = sqlalchemy.create_engine("sqlite+pysqlite:///data/lootiusTest.db", echo=True)
lootiusDB.metadata.create_all(engine)
# lootiusDB.metadata.drop_all(engine)