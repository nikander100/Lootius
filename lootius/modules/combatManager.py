from database import db
from models.databaseModel import *

Session = db.DB.getSession()

class loggingRun_BLL():

    @staticmethod
    def calculate_miss_chance(huntingLog: LoggingRun):
        if huntingLog.total_attacks_done == 0:
            return 0
        miss_chance = huntingLog.total_attacks_missed / huntingLog.total_attacks_done * 100
        return miss_chance 