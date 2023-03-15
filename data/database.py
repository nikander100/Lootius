import sqlite3
from sqlite3 import Error
import csv, time

# Updates the database with new data from wiki (to be made)
class UpdateDatabse:
    def __init__(self):
        pass

# First time setup of the local database.
"""To be put into documentation"""
class SetupDatabase:
    def __init__(self):
        pass

    def __getRawDatabakup(self, csvInput, dbCur):
        fd = open(csvInput[0], "r")
        reader = csv.reader(fd ,delimiter=";")
        name = ''
        type = ''
        decay = ''
        ammo = ''
            
        for row in reader:
            for i in range(len(row)):
                print(row)
                name = row[0]
                type = row[1]
                try: decay = float(row[2])
                except ValueError: decay = 0
                if csvInput[1] == "weapons" or csvInput[1] == "amps":
                    try: ammo = int(row[3])
                    except ValueError: ammo = 0
            if csvInput[1] == "weapons" or csvInput[1] == "amps":
                InsertQuery=f"INSERT INTO {csvInput[1]} (name, type, decay, ammo) VALUES('{name}','{type}',{decay},{ammo})"
            else:
                InsertQuery=f"INSERT INTO {csvInput[1]} (name, type, decay) VALUES('{name}','{type}',{decay})"
            dbCur.executescript(InsertQuery)
        fd.close()

    def __getRawData(self, csvInput, dbCur):
        fd = open(csvInput[0], "r")
        reader = csv.reader(fd ,delimiter=";")
        next(reader)
        name = ''
        type = ''
        damage = ''
        firerate = ''
        decay = ''
        ammo = ''

        InsertQuery=f"INSERT INTO WeaponTypes(weaponType) Values('unknown')"
        dbCur.executescript(InsertQuery)
        InsertQuery=f"INSERT INTO WeaponTypes(weaponType) Values('ranged')"
        dbCur.executescript(InsertQuery)
        InsertQuery=f"INSERT INTO WeaponTypes(weaponType) Values('melee')"
        dbCur.executescript(InsertQuery)
        for row in reader:
            print(row)
            name = row[0]
            try:
                if row[1] == "Melee":   type = int(3)
                else:                   type = int(2)
            except ValueError: type = int(1)
            try: damage = int(row[2])
            except ValueError: damage = 0
            try: firerate = int(row[3])
            except ValueError: damage = 0
            try: decay = float(row[4])
            except ValueError: decay = 0
            try: ammo = int(row[5])
            except ValueError: ammo = 0

            InsertQuery=f"INSERT INTO {csvInput[1]} (name, damage, firerate, decay, ammoBurn, weaponTypeID) VALUES('{name}',{damage},{firerate},{decay},{ammo},'{type}')"
            print(InsertQuery)
            dbCur.executescript(InsertQuery)
        fd.close()

    def setupDatabase(self, dbFile):
        inputData = (
            ("data/csv/weapons.csv", "Weapons"),
            ("data/csv/sights.csv", "Sights"),
            # ("data/csv/scopes.csv", "Scopes"),
            # ("data/csv/amps.csv", "Amps"),
        )
        con = None
        
        # Create database
        try:
            con = sqlite3.connect(dbFile)
        except Error as e:
            print(e)  ;"""log to errors"""
        finally:
            if con:
                cur = con.cursor()

                # Setup database
                with open("data/script.sql", "r") as fd:
                    script = fd.read()
                cur.executescript(script)

                # Populate databse
                for data in (inputData):
                    print(data)
                    self.__getRawData(data, cur)
                    break
                con.commit()
                con.close()

setupdb = SetupDatabase()
setupdb.setupDatabase("data/test.db")

