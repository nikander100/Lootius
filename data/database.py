import sqlite3
from sqlite3 import Error
import csv

# Updates the database with new data from wiki (to be made)
class UpdateDatabse:
    def __init__(self):
        pass

# First time setup of the local database.
"""To be put into documentation"""
class SetupDatabase:
    def __init__(self):
        pass

    def __getRawData(self, csvInput, dbCur):
        fd = open(csvInput[0], "r")
        csvFr = csv.reader(fd ,delimiter=";")
        name = ''
        type = ''
        decay = ''
        ammo = ''
            
        for row in csvFr:
            for i in range(len(row)):
                name = row[0]
                type = row[1]
                try: decay = float(row[2])
                except ValueError: decay = 0
                if csvInput[1] == "Weapons" or csvInput[1] == "Amps":
                    try: ammo = int(row[3])
                    except ValueError: ammo = 0
            if csvInput[1] == "Weapons" or csvInput[1] == "Amps":
                InsertQuery=f"INSERT INTO {csvInput[1]} (name, type, decay, ammo) VALUES('{name}','{type}',{decay},{ammo})"
            else:
                InsertQuery=f"INSERT INTO {csvInput[1]} (name, type, decay) VALUES('{name}','{type}',{decay})"
            dbCur.executescript(InsertQuery)
        fd.close()

    def setupDatabase(dbFile):
        inputData = (
            ("data/csv/weapons.csv", "Weapons"),
            ("data/csv/sights.csv", "Sights"),
            ("data/csv/scopes.csv", "Scopes"),
            ("data/csv/amps.csv", "Amps"),
        )
        con = None
        try:
            con = sqlite3.connect(dbFile)
        except Error as e:
            print(e) # log to errors
        finally:
            if con:
                cur = con.cursor()

                with open("data/script.sql", "r") as fd:
                    script = fd.read()
                cur.executescript(script)
                for data in (inputData):
                    print(data)
                    self.__getRawData(data, cur)
                con.commit()
                con.close()

SetupDatabase.setupDatabase("data/test1.db")
