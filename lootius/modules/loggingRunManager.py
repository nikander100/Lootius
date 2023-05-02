from database import db
from database.db import LocalSession
from models.databaseModel import *
from decimal import Decimal
from sqlalchemy import func
import datetime

from modules.logParser import CombatRow, LootRow, SkillRow, HealRow, GlobalRow, EnhancerRow

def getDuration(huntingLog: LoggingRun) -> str:
    """Return the duration of a hunting session.

    Parameters
    ----------
    huntingLog : LoggingRun
        The hunting session logging information.

    Returns
    -------
    str
        A string with the duration in hours:minutes:seconds format.

    Example
    --------
    >>> log = LoggingRun()
    >>> log.timeStart = datetime.now() - timedelta(minutes=30)
    >>> log.timeStop = datetime.now()
    >>> Session.getDuration(log)
    '0:30:0'
    """
    duration = huntingLog.timeStop - huntingLog.timeStart if huntingLog.timeStop else datetime.now() - huntingLog.timeStart
    return "{}:{}:{}".format(duration.hours, duration.seconds // 60, duration.seconds % 60)

def missChance(huntingLog: LoggingRun) -> float:
    """
    Calculates the percentage of missed attacks in a Hunting Log.

    Parameters
    ----------
    huntingLog : LoggingRun
        The Hunting Log containing the data to be analyzed.

    Returns
    -------
    float
        The percentage of missed attacks in the Hunting Log, expressed as a float between 0.0 and 100.0.

    Example
    -------
    >>> log = LoggingRun(...)
    >>> missChance = HuntingCalculator.missChance(log)
    >>> print(missChance)
    12.34
    """
    if huntingLog.totalAttacks == 0:
        return 0.00
    missChance = huntingLog.totalMisses / float(huntingLog.totalAttacks) * 100
    return missChance

def critChance(huntingLog: LoggingRun) -> float:
    """
    Calculates the percentage of Critical Attacks in a Hunting Log.

    Parameters
    ----------
    huntingLog : LoggingRun
        A hunting log instance containing attack data.

    Returns
    -------
    float
        The percentage of critical hits, expressed as a float between 0 and 100.

    Example
    -------
    >>> log = LoggingRun(...)
    >>> critChance = HuntingCalculator.critChance(log)
    >>> print(critChance)
    12.34
    """
    if huntingLog.totalAttacks == 0:
        return 0.00
    critChance = huntingLog.totalCrits / float(huntingLog.totalAttacks) * 100
    return critChance

def damagePerPec(huntingLog: LoggingRun) -> Decimal:
    """
    Calculate the damage per pec (DPP) in a hunting log.

    Parameters
    ----------
    huntingLog : LoggingRun
        The hunting log containing the data to calculate DPP.

    Returns
    -------
    Decimal
        The DPP value calculated from the hunting log.

    Notes
    -----
    DPP is calculated as total damage dealt divided by the total cost of the hunt in pecs (including any extra spending).

    Example
    --------
    >>> log = LoggingRun(...)
    >>> dpp = damagePerPec(log)
    >>> print(dpp)
    Decimal('12.34')
    """
    if huntingLog.costTotal > Decimal(0):
        dpp = Decimal(huntingLog.totalDamage) / Decimal(huntingLog.costTotal + huntingLog.costExtraSpend) * 100
        return dpp
    return Decimal(0.0)
    
def getTotalSkillsGained(huntingLog: LoggingRun) -> Decimal:
    """
    Get the total amount of skills gained during a hunting log.

    Parameters
    ----------
    huntingLog : LoggingRun
        The hunting log to retrieve the total skills gained for.

    Returns
    -------
    Decimal
        The total amount of skills gained during the hunting log.

    Example
    --------
    >>> log = LoggingRun(...)
    >>> totalSkillsGained = LoggingRun.getTotalSkillsGained(log)
    >>> print(totalSkillsGained)
    125.0
    """
    totalSkillsGained = LocalSession.query(func.sum(SkillItem.value)).filter_by(LoggingRunID=huntingLog.id).scalar()

    return Decimal(totalSkillsGained) if totalSkillsGained is not None else Decimal(0)



def addCombatRow(huntingLog: LoggingRun, row: CombatRow, costPerShot: Decimal):
    huntingLog.totalAttacks += 1
    huntingLog.totalDamage += row.amount
    if row.critical:
        huntingLog.totalCrits += 1
    if row.miss:
        huntingLog.totalMisses += 1
    huntingLog.costTotal += costPerShot