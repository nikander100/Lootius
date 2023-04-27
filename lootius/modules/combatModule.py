from collections import namedtuple, defaultdict
from datetime import datetime
from decimal import Decimal
from typing import List
import threading
import time
import os
import sqlalchemy
from sqlalchemy.orm import scoped_session
from database import db
from database.db import LocalSession

from modules.baseModule import BaseModule
from modules.logParser import BaseChatRow, CombatRow, LootRow, SkillRow, HealRow, GlobalRow, EnhancerRow
from models.databaseModel import *
# from ocr import screenshot_window
import combatManager, loadoutManager



# turn this into db table too?
class HuntingRun(object):
    def __init__(self, timeStart: datetime, costPerShot: Decimal, costPerHeal: Decimal):

        # Costs [gotten from selected wepaonloadout]
        # MOVE TO COMBAT MODULE
        self.costPerShot = costPerShot
        self.costPerHeal = costPerHeal



        # Returns [what do with these, figure out?]
        # MOVE TO COMBAT MODULE
        self.cachedTotalReturnMu = Decimal("0.0")

        #loot instance from chat row. used in calcs
        # MOVE TO COMBAT MODULE
        self.lastLootInstance = None
        self.lootInstance = 0

        # Tracking Multipliers (for graphs not used atm)
        # MOVE TO COMBAT MODULE???
        self.lootInstanceCost = Decimal(0)
        self.lootInstanceValue = Decimal(0)
        self.multiplier = ([], [])
        self.returnOverTime = []

        # ??? # MOVE TO COMBAT MODULE???
        self.adjustedCost = Decimal(0)




class CombatModule(BaseModule):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Core Controls
        self.isLogging = False
        self.shouldRedrawRuns = True

        # Set by Parent in lootnan (what should i do?) think this is all frontend
        self.lootTable = None #table? maybe need to change to db connection
        self.runsTable = None #table? maybe need to change to db connection
        self.skillsTable = None #table? maybe need to change to db connection
        self.enhancerTable = None #table? maybe need to change to db connection (part of weaponloadout)
        self.combatFields = {}
        self.lootField = {}

        # Loadout Types
        # TODO get value from selected ui
        self.weaponLoadout = combatManager.setActiveWeaponLoadout(1)

        # exmaple begin\
        # config = config
        # config.selectedloadout.id =1
        # # ofcourse combatmodule has acess to selected loadout from session so can get id form that
        # selectedWeapon = loadoutManager.getSelectedWeapon(config.selectedloadout.id)
        # self.ammoBurn = selectedWeapon["weapon"].ammoBurn + selectedWeapon["amps"].ammoBurn

        # example end

        # TODO Hunting Runs (change to db object, so need active session!)
        self.activeRun: HuntingRun = None

        # Graphs
        self.multiplierGraph = None
        self.returnGraph = None

    def tick(self, lines: List[BaseChatRow]):
        if self.isLogging is True:

            if self.activeRun is None:
                self.activeRun = LoggingRun

