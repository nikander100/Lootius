from collections import namedtuple, defaultdict
from datetime import datetime
import time
from decimal import Decimal
from typing import List
import threading
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from modules.baseModule import BaseModule
from modules.logParser import BaseChatRow, CombatRow, LootRow, SkillRow, HealRow, GlobalRow, EnhancerRow
# from ocr import screenshot_window

#dbfilepath to be set in config
dbFilePath = "/lootius/database/lootiusTest.db"
"C://Users/ndvds/Documents/GitHub/Lootius/lootius/database/lootiusTest.db"
LootiusDB = sqlalchemy.create_engine(f"sqlite+pysqlite://{dbFilePath}", echo=True)
#use with DBSession.begin() as ... to interact with db
DBSession = sessionmaker(LootiusDB)

# turn this into db table too?
class HuntingRun(object):
    def __init__(self, timeStart: datetime, costPerShot: Decimal, costPerHeal: Decimal):
        self.timeStart = timeStart
        self.timeEnd = None
        self.notes = ""
        
        # Costs
        self.costPerShot = costPerShot
        self.costPerHeal = costPerHeal
        self.totalCost = 0
        self.extraSpend = Decimal(0.0)

        # Returns
        self.ttReturn = 0
        self.globals = 0
        self.hofs = 0
        self.cachedTotalReturnMu = Decimal("0.0")
        self.lootItems = defaultdict(lambda: {"c": 0, "v": Decimal()})

        self.lastLootInstance = None
        self.lootInstance = 0

        # Tracking Multipliers
        self.lootInstanceCost = Decimal(0)
        self.lootInstanceValue = Decimal(0)
        self.multiplier = ([], [])
        self.returnOverTime = []


        self.adjustedCost = Decimal(0)


        # Combat Stats
        self.totalAttacks = 0
        self.totalDamage = 0
        self.totalCrits = 0
        self.totalMisses = 0
        # Healing Stats
        self.totalHeals = 0
        self.totalHealed = 0
        # Misc Stats
        self.enhancerBreaks = defaultdict(int)
        self.skillgains = defaultdict(int)



class CombatModule(BaseModule):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Core Controls
        self.isLogging = False
        self.shouldRedrawRuns = True

        # Set by Parent
        self.lootTable = None #table? maybe need to change to db connection
        self.runsTable = None #table? maybe need to change to db connection
        self.skillsTable = None #table? maybe need to change to db connection
        self.enhancerTable = None #table? maybe need to change to db connection (part of weaponloadout)
        self.combatFields = {}
        self.lootField = {}

        # Loadout Types
        self.weaponLoadout = None
        self.healingLoadout = None

        # Calculated Conf
        self.ammoBurn = 0
        self.decay = 0

        # Hunting Runs
        self.activeRun: HuntingRun = None
        self.runs: List[HuntingRun] = []

        # Graphs
        self.multiplierGraph = None
        self.returnGraph = None

        # Keypress
        self.lastKeyPress = None
