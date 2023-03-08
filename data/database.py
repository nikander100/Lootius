import sqlite3
from sqlite3 import Error
import csv

# Updates the database with new data from wiki (to be made)
class UpdateDatabse:
    def __init__(self):
        pass

# First time setup of the local database.
class SetupDatabase:
    def __init__(self):
        pass
    def setupDatabase(dbFile):
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
                with open("data/weapons.csv", "r") as fd:
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
                            try: ammo = int(row[3])
                            except ValueError: ammo = 0
                        InsertQuery=f"INSERT INTO Weapons (name, type, decay, ammo) VALUES('{name}','{type}',{decay},{ammo})"
                        cur.executescript(InsertQuery)
                    con.commit
                con.close()

SetupDatabase.setupDatabase("data/test.db")