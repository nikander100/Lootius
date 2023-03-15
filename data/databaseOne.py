import sqlite3
from sqlite3 import Error
import csv, time, sqlalchemy, sqlalchemy.orm


"""
New database setup based on ORM to keep sql in code to a minimum.
"""
class