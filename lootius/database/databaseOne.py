import sqlite3
import pandas, time, sqlalchemy, typing, sys
from lootius.models.databaseModel import Base
from sqlalchemy.orm import sessionmaker
from sqlite3 import Error

class SetupDatabase:
    def __init__(self):
        pass

    def _dropDatabase(self):
        lootiusDB = Base()
        engine = sqlalchemy.create_engine("sqlite+pysqlite:///lootius/database/lootiusTest.db", echo=True)
        lootiusDB.metadata.drop_all(engine)

    def __populateWeaponTypeTable(self, engine):
        Session = sessionmaker(engine)
        from lootius.models.databaseModel import WeaponTypes
        with Session.begin() as session:
            wType1, wType2, wType3 = (WeaponTypes() for _ in range(3))
            wType1.type = "unknown"
            wType2.type = "ranged"
            wType3.type = "melee"
            session.add_all([wType1, wType2, wType3])

    def __populateWeaponTable(self, engine):
        from lootius.models.databaseModel import Weapons
        weaponsCSV = "./data/csv/weapons.csv"
        convert = (lambda x: 3 if x == "Melee" else 2)
        df = pandas.read_csv(weaponsCSV, sep=";", converters={"Class":convert})
        df = df.rename(columns={"Name":"name", "Class":"weaponTypeID", "Damage":"damage", "Attacks":"firerate", "Decay":"decay", "Ammo":"ammoBurn"})
        df = df.replace(r'^\s*$', 0, regex=True)
        df.to_sql(con=engine, name=Weapons.__tablename__, if_exists="append", index=False)

    def __populateSightsTable(self, engine):
        from lootius.models.databaseModel import Sights
        sightsCSV = "./data/csv/sights.csv"
        df = pandas.read_csv(sightsCSV, sep=";")
        df = df.rename(columns={"Name":"name", "Type":"weaponTypeID", "Decay":"decay"}) # same as in scopes
        df[["weaponTypeID"]] = df[["weaponTypeID"]].replace("Sight", 2) # same as in scopes
        df = df.replace(r'^\s*$', 0, regex=True)
        df.to_sql(con=engine, name=Sights.__tablename__, if_exists="append", index=False)

    def __populateScopesTable(self, engine):
        from lootius.models.databaseModel import Scopes
        scopesCSV = "./data/csv/sights.csv"
        df = pandas.read_csv(scopesCSV, sep=";")
        df = df.rename(columns={"Name":"name", "Type":"weaponTypeID", "Decay":"decay"}) # same as in sights
        df[["weaponTypeID"]] = df[["weaponTypeID"]].replace("Sight", 2) # same as in sights
        df = df.replace(r'^\s*$', 0, regex=True)
        df.to_sql(con=engine, name=Scopes.__tablename__, if_exists="append", index=False)

    def __populateTable(self, engine, Session):
        pass

    def __populateTable(self, engine, Session):
        pass


    def __populateDatabase(self, engine):
        
        # Populate weaponType
        self.__populateWeaponTypeTable(engine)

        # Populate weapons
        self.__populateWeaponTable(engine)

        # Populate sights
        self.__populateSightsTable(engine)

        # Populate scopes
        self.__populateScopesTable(engine)


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
# time.sleep(1)
testDB.setupDatabase("/lootius/database/lootiusTest.db")

