import sqlite3
import pandas, time, sqlalchemy, typing, sys
from lootius.models.databaseModel import *
from sqlite3 import Error

class SetupDatabase:
    def __init__(self):
        pass

    def _dropDatabase(self):
        lootiusDB = Base()
        engine = sqlalchemy.create_engine("sqlite+pysqlite:///lootius/database/lootiusTest.db", echo=True)
        lootiusDB.metadata.drop_all(engine)
        

    def __populateDatabase(self, engine):

        # Populate weapons
        weaponsCSV = "./data/csv/weapons.csv"
        convert = (lambda x: 3 if x == "Melee" else 2)
        df = pandas.read_csv(weaponsCSV, sep=";", converters={"Class":convert})
        df = df.rename(columns={"Name":"name", "Class":"weaponTypeID", "Damage":"damage", "Attacks":"firerate", "Decay":"decay", "Ammo":"ammoBurn"})
        df = df.replace(r'^\s*$', 0, regex=True)
        df.to_sql(con=engine, name=Weapons.__tablename__, if_exists="append", index=False)

    def setupDatabase(self, dbFilePath):
        lootiusDB = Base()
        try:
            engine = sqlalchemy.create_engine(f"sqlite+pysqlite://{dbFilePath}", echo=True)
        except Error as e:
            print(e)  ;"""log to errors, have to find out what the error return is from alchemy"""
        finally:
            lootiusDB.metadata.create_all(engine)
            self.__populateDatabase(engine)



testDB = SetupDatabase()
testDB._dropDatabase()
time.sleep(1)
testDB.setupDatabase("/lootius/database/lootiusTest.db")

