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

    def __populateEnhancerTypeTable(self, engine):
        Session = sessionmaker(engine)
        from lootius.models.databaseModel import EnhancerTypes
        with Session.begin() as session:
            typeOne, typeTwo, typeThree = (EnhancerTypes() for _ in range(3))
            typeTwo.type = "healing"
            typeThree.type = "mining"
            typeOne.type = "weapon"
            session.add_all([typeOne, typeTwo, typeThree])

    def __populateEnhancerNameTable(self, engine):
        Session = sessionmaker(engine)
        from lootius.models.databaseModel import EnhancerNames
        with Session.begin() as session:
            nameOne, nameTwo, nameThree, nameFour = (EnhancerNames() for _ in range(4))
            nameOne.name = "Medical Tool"
            nameTwo.name = "Mining Excavator"
            nameThree.name = "Mining Finder"
            nameFour.name = "Weapon"
            session.add_all([nameOne, nameTwo, nameThree, nameFour])

    def __populateEnhancerTypeNameTable(self, engine):
        Session = sessionmaker(engine)
        from lootius.models.databaseModel import EnhancerTypeNames
        with Session.begin() as session:
            name = [EnhancerTypeNames() for i in range(8)]
            name[0].name = "Economy"
            name[1].name = "Heal"
            name[2].name = "Speed"
            name[3].name = "Depth"
            name[4].name = "Range"
            name[5].name = "Accuracy"
            name[6].name = "Damage"
            name[7].name = "Skill Modification"
            session.add_all([name[0], name[1], name[2], name[3], name[4], name[5], name[6], name[7]])

    def __populateEnhancerClassTable(self, engine):
        enhancerClassCSV = "./data/csv/enhancerClass.csv"
        from lootius.models.databaseModel import EnhancerClass
        df = pandas.read_csv(enhancerClassCSV, sep=";")
        df = df.rename(columns={"SkillName":"enhancerTypeNameID", "Effect":"enhancerEffectID", "Type":"enhancerTypeID", "TypeName":"enhancerNameID"})
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)
        df.to_sql(con=engine, name=EnhancerClass.__tablename__, if_exists="append", index=False)
    
    def __populateEnhancerEffectsTable(self, engine):
        from lootius.models.databaseModel import EnhancerEffects
        enhancerEffectsCSV = "./data/csv/enhancerEffects.csv"
        df = pandas.read_csv(enhancerEffectsCSV, sep=";")
        df = df.rename(columns={"DecayAmount":"decayAmount", "BonusAmount":"bonusAmount"})
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)
        df.to_sql(con=engine, name=EnhancerEffects.__tablename__, if_exists="append", index=False)
    
    def __populateWeaponTypeTable(self, engine):
        Session = sessionmaker(engine)
        from lootius.models.databaseModel import WeaponTypes
        with Session.begin() as session:
            typeOne, typeTwo, typeThree, typeFour, typeFive = (WeaponTypes() for _ in range(5))
            typeOne.type = "all"
            typeTwo.type = "laser"
            typeThree.type = "blp"
            typeFour.type = "mindforce"
            typeFive.type = "melee"
            session.add_all([typeOne, typeTwo, typeThree, typeFour, typeFive])


    def __populateWeaponTable(self, engine):
        from lootius.models.databaseModel import Weapons
        weaponsCSV = "./data/csv/weapons.csv"
        laserSet = {"laser", "gauss"}
        blpSet = {"blp", "plasma"}
        mindforceSet = {"cryogenic", "electric", "pyro"}
        meleeSet = {"axes", "clubs", "longblades", "power fist", "shortblades", "whip"}
        convert = (lambda x: 5 if str(x).lower() in meleeSet \
                    else 4 if str(x).lower() in mindforceSet \
                    else 3 if str(x).lower() in blpSet \
                    else 2 if str(x).lower() in laserSet \
                    else 1)
        df = pandas.read_csv(weaponsCSV, sep=";", converters={"Type":convert})
        df = df.rename(columns={"Name":"name", "Type":"weaponTypeID", "Damage":"damage", "Attacks":"firerate", "Decay":"decay", "Ammo":"ammoBurn"})
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)
        df.to_sql(con=engine, name=Weapons.__tablename__, if_exists="append", index=False)

    def __populateSightsTable(self, engine):
        from lootius.models.databaseModel import Sights
        sightsCSV = "./data/csv/sights.csv"
        df = pandas.read_csv(sightsCSV, sep=";")
        df = df.rename(columns={"Name":"name", "Type":"weaponTypeID", "Decay":"decay"}) # same as in scopes
        df[["weaponTypeID"]] = df[["weaponTypeID"]].replace("Sight", 2) # same as in scopes
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)
        df.to_sql(con=engine, name=Sights.__tablename__, if_exists="append", index=False)

    def __populateScopesTable(self, engine):
        from lootius.models.databaseModel import Scopes
        scopesCSV = "./data/csv/scopes.csv"
        df = pandas.read_csv(scopesCSV, sep=";")
        df = df.rename(columns={"Name":"name", "Type":"weaponTypeID", "Decay":"decay"}) # same as in sights
        df[["weaponTypeID"]] = df[["weaponTypeID"]].replace("Scope", 2) # same as in sights
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)
        df.to_sql(con=engine, name=Scopes.__tablename__, if_exists="append", index=False)

    def __populateWeaponAmpsTable(self, engine):
        from lootius.models.databaseModel import WeaponAmps
        ampsCSV = "./data/csv/weaponAmps.csv"
        convert = (lambda x: 5 if str(x).lower() == "melee amp" \
                    else 4 if str(x).lower() in "mf amp" \
                    else 3 if str(x).lower() in "blp amp" \
                    else 2 if str(x).lower() in "energy amp" \
                    else 1)
        df = pandas.read_csv(ampsCSV, sep=";", converters={"Type":convert})
        df = df.rename(columns={"Name":"name", "Type":"weaponTypeID", "Decay":"decay", "Ammo":"ammoBurn"}) #
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)
        df.to_sql(con=engine, name=WeaponAmps.__tablename__, if_exists="append", index=False)

    def __populateAbsorberTable(self, engine):
        from lootius.models.databaseModel import WeaponAbsorbers
        absorbersCSV = "./data/csv/absorbers.csv"
        convert = (lambda x: 5 if str(x).lower() == "melee absorber" else 1)
        df = pandas.read_csv(absorbersCSV, sep=";", converters={"Type":convert})
        df = df.rename(columns={"Name":"name", "Type":"weaponTypeID", "Decay":"decay", "AbsorbPercent":"absorbPercent"})
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)
        df.to_sql(con=engine, name=WeaponAbsorbers.__tablename__, if_exists="append", index=False)

    def __populateDatabase(self, engine):
        self.__populateWeaponTypeTable(engine)
        self.__populateEnhancerClassTable(engine)
        self.__populateEnhancerTypeNameTable(engine)
        self.__populateEnhancerNameTable(engine)
        self.__populateEnhancerTypeTable(engine)
        self.__populateEnhancerEffectsTable(engine)
        self.__populateWeaponTable(engine)
        self.__populateSightsTable(engine)
        self.__populateScopesTable(engine)
        self.__populateWeaponAmpsTable(engine)
        self.__populateAbsorberTable(engine)




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
