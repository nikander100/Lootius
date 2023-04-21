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
import combatManager, loadoutManager

#dbfilepath to be set in config
dbFilePath = "/lootius/database/lootiusTest.db"
"C://Users/ndvds/Documents/GitHub/Lootius/lootius/database/lootiusTest.db"
LootiusDB = sqlalchemy.create_engine(f"sqlite+pysqlite://{dbFilePath}", echo=True)
#use with DBSession.begin() as ... to interact with db
DBSession = sessionmaker(LootiusDB)

# turn this into db table too?
class HuntingRun(object):
    def __init__(self, timeStart: datetime, costPerShot: Decimal, costPerHeal: Decimal):

        # Costs [gotten from selected wepaonloadout]
        self.costPerShot = costPerShot
        self.costPerHeal = costPerHeal



        # Returns [what do with these, figure out?]
        self.cachedTotalReturnMu = Decimal("0.0")

        #loot instance from chat row. used in calcs
        self.lastLootInstance = None
        self.lootInstance = 0

        # Tracking Multipliers (for graphs not used atm)
        self.lootInstanceCost = Decimal(0)
        self.lootInstanceValue = Decimal(0)
        self.multiplier = ([], [])
        self.returnOverTime = []

        # ???
        self.adjustedCost = Decimal(0)




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

        # exmaple begin\
        # config = config
        # config.selectedloadout.id =1
        # # ofcourse combatmodule has acess to selected loadout from session so can get id form that
        # selectedWeapon = loadoutManager.getSelectedWeapon(config.selectedloadout.id)
        # self.ammoBurn = selectedWeapon["weapon"].ammoBurn + selectedWeapon["amps"].ammoBurn

        # example end

        # Hunting Runs
        self.activeRun: HuntingRun = None
        self.runs: List[HuntingRun] = []

        # Graphs
        self.multiplierGraph = None
        self.returnGraph = None

        # Keypress
        self.lastKeyPress = None
