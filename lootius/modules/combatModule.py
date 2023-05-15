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
import modules.combatManager as combatManager
import modules.loadoutManager as loadoutManager
import modules.loggingRunManager as loggingRunManager



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

        # ??? # MOVE TO COMBAT MODULE???
        self.adjustedCost = Decimal(0)




class CombatModule(BaseModule):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Core Controls
        self.isLogging = False
        # self.shouldRedrawRuns = True

        # Loot instance
        self.lastLootInstance = None
        # Tracking Multipliers (for graphs not used atm)
        self.lootInstanceCost = Decimal(0)
        self.lootInstanceValue = Decimal(0)


        # Loadout Types
        # TODO get value from selected ui
        # self.weaponLoadout = combatManager.setActiveWeaponLoadout(1)
        self.weaponLoadout = None

        self.costPerShot = loadoutManager.getCostPerShot(self.weaponLoadout) if self.weaponLoadout else None

        # exmaple begin\
        # config = config
        # config.selectedloadout.id =1
        # # ofcourse combatmodule has acess to selected loadout from session so can get id form that
        # selectedWeapon = loadoutManager.getSelectedWeapon(config.selectedloadout.id)
        # self.ammoBurn = selectedWeapon["weapon"].ammoBurn + selectedWeapon["amps"].ammoBurn

        # example end

        # TODO Hunting Runs (change to db object, so need active session!)
        self.activeRun: LoggingRun = None

    # TODO check where and how to add new data to database, I kinda wanted to so a seperate save function that runs every 10-15 sec on a seperate thread
    # but maybe I might as well do it on the end of every tick, as not to many lines are added at once. and as it is local it shouldnt hold the rest,
    # i will try this first and if it does end up breaking. im gonn ahev to remake / think some tings
    def tick(self, lines: List[BaseChatRow]):
        if self.isLogging is True:

            if self.activeRun is None:
                self.activeRun = loggingRunManager.createNewRun()
            
            for chatInstance in lines:
                if isinstance(chatInstance, CombatRow):
                    self.addCombatChatRow(LoggingRun, chatInstance)
                # add heal row here after first working version.
                elif isinstance(chatInstance, LootRow):
                    self.addLootChatRow(LoggingRun, chatInstance)
                elif isinstance(chatInstance, EnhancerRow):
                    self.addEnhancerChatRow(LoggingRun, chatInstance)
                elif isinstance(chatInstance, SkillRow):
                    self.addSkillChatRow(LoggingRun, chatInstance)
                elif isinstance(chatInstance, GlobalRow):
                    self.addGlobalChatRow(LoggingRun, chatInstance)
                
            #from lootnan
            '''if self.app.streamer_window:
                self.app.streamer_window.set_text_from_module(self)

                part of original code, have to implment this still.
                part of entangled ui code.

        if self.runs and self.should_redraw_runs:
            self.update_tables()
            self.should_redraw_runs = False'''

    def addCombatChatRow(self, huntingLog: LoggingRun, row: CombatRow):
        self.lootInstanceCost += self.costPerShot
        loggingRunManager.addCombatRow(huntingLog, row, self.costPerShot)

    def addLootChatRow(self, huntingLog: LoggingRun, row: LootRow):
        ts = time.mktime(row.time.timetuple()) // 2
        
        # We dont want to consider sharp conversion as a loot event
        # TODO Make a function / list to reffernce to to check if it sohuld not be part as loot event. e.a convert, keys, boxes, probes, etc.
        if row.name == "Universal Ammo":
            return
        
        if self.last_loot_instance != ts:
            if row.name == "Vibrant Sweat":
                # Dont count sweat as a loot instance
                pass
            elif row.name == "Shrapnel" and row.amount in {4000, 6000, 8000, 10000}:
                # If looks like an enhancer break
                pass  # But we still add the shrapnel back to the total items looted | enhancer break
            else:
                self.lastLootInstance = ts

                loggingRunManager.addLootRow(huntingLog, row, self.lootInstanceCost, self.lootInstanceValue)
                if self.lootInstanceValue and self.lootInstanceCost:
                    self.lootInstanceCost = Decimal(0)
                    self.lootInstanceValue = Decimal(0)
        
        self.lootInstanceValue += row.value
    
    def addEnhancerChatRow(self, huntingLog: LoggingRun, row: EnhancerRow):
        loggingRunManager.addEnhancerRow(huntingLog, row)

    def addSkillChatRow(self, huntingLog: LoggingRun, row: SkillRow):
        loggingRunManager.addSkillRow(huntingLog, row)

    def addGlobalChatRow(self, huntingLog: LoggingRun, row: GlobalRow):
        #add is statement for chekcing if global name == player or list plaer/team names.
        #add screenshot module and trigger it.
        loggingRunManager.addGlobalRow(huntingLog, row)
        # possibly add more to this later, maybe not needed though.

    def saveActiveRun(self, force=False):
        if not self.activeRun:
            if not force:
                return
            pass # force save last run instnace from db.
            #combatManager.saveRun(self.activeRun)
        else:
            combatManager.saveRun(self.activeRun)
