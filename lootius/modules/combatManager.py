from database import db
from database.db import LocalSession
from models.databaseModel import *
from decimal import Decimal
from sqlalchemy import func
import datetime

from modules.logParser import CombatRow, LootRow, SkillRow, HealRow, GlobalRow, EnhancerRow

#TODO maybe need to allow both id and WeaponLoadout class object as input.
def setActiveWeaponLoadout(weaponLoadoutID: int) -> WeaponLoadout:
    activeLoadout = LocalSession.query(WeaponLoadout).filter_by(id=weaponLoadoutID)
    return activeLoadout