"""
loadoutManager module.

This module provides functions to manage loadouts, which are combinations of weapons, scopes, sights, enhancers, and
other items in lootius.

Functions
---------
def setLoadout(selectedName: str, selectedWeapon: int,
               selectedAmp: Optional[int],
               selectedAbs: Optional[int],
               selectedScope: Optional[int],
               selectedScopeSight: Optional[int],
               selectedSight: Optional[int],
               selectedEnhancers: Optional[List]):
    Set the current loadout with the specified items.

def getWeapons(weaponType: int = None) -> Tuple[List[str], List[int]]:
    Get the available weapons.
def getScopes() -> Tuple[List[str], List[int]]:
    Get the available sights.
def getSights() -> Tuple[List[str], List[int]]:
    Get the available sights.
def getEnhancers(enhancerType: int = None) -> Tuple[List[str], List[int]]:
    Get the available enhancers.
def getAbsorbers(weaponType: int = None) -> Tuple[List[str], List[int]]:
    Get the available absorbers.
def getAmplifiers(weaponType: int = None) -> Tuple[List[str], List[int]]:
    Get the available amplifiers.
def getSelectedWeapon(selectedWeaponID: int) -> Dict[str, Union[Weapons, List[Tuple[int, str]]]]:
    Get the selected weapon, including its type, attachments, and stats.
"""
from models.databaseModel import Weapons, Sights, Scopes, EnhancerClass, WeaponAbsorbers, WeaponLoadout, ScopeLoadout, EnhancerLoadout, WeaponAmps
from database.db import LocalSession
from typing import List, Tuple, Dict, Union, Optional
from decimal import Decimal
from sqlalchemy.orm import joinedload

"""
    TODO: (click me)
    Split up function in classes for x type loadout, and have shared fucntions not in class
"""


def setLoadout(selectedName: str, selectedWeapon: int,
               selectedAmp: Optional[int],
               selectedAbs: Optional[int],
               selectedScope: Optional[int],
               selectedScopeSight: Optional[int],
               selectedSight: Optional[int],
               selectedEnhancers: Optional[List]):
    """Add a new weapon loadout to the database.

    Parameters
    ----------
    selectedName : str
        The name of the new weapon loadout.
    selectedWeapon : int
        The ID of the weapon for the new loadout, or None if no weapon is selected.
    selectedAmp : int or None
        The ID of the weapon amp for the new loadout, or None if no weapon amp is selected.
    selectedAbs : int or None
        The ID of the weapon absorber for the new loadout, or None if no weapon absorber is selected.
    selectedScope : int or None
        The ID of the scope for the new loadout, or None if no scope is selected.
    selectedScopeSight : int or None
        The ID of the scope sight for the new loadout, or None if no scope sight is selected.
    selectedSight : int or None
        The ID of the sight for the new loadout, or None if no sight is selected.
    selectedEnhancers : list
        A list of lists, each containing the socket number (int), the enhancer ID (int or None),
        and the amount of the enhancer (int).

    Returns
    -------
    None
        This function does not return anything.

    """
    weaponLoadout = WeaponLoadout(
        name=selectedName,
        weaponID=selectedWeapon,
        amplifierID=selectedAmp,
        sightID=selectedSight,
        absorberID=selectedAbs
    )
    LocalSession.add(weaponLoadout)
    LocalSession.flush()

    newEnhancerLoadouts = []
    for enhancer in selectedEnhancers:
        if enhancer[1] is not None and enhancer[2] != 0:
            newEnhancerLoadouts.append(EnhancerLoadout(
            weaponLoadoutID=weaponLoadout.id,
            socket=enhancer[0],
            enhancerClassID=enhancer[1],
            amount=enhancer[2],
            ))

    LocalSession.add_all(newEnhancerLoadouts)
    LocalSession.flush()
    
    if selectedScope is not None:
        newScopeLoadout = ScopeLoadout(
            weaponLoadoutID=weaponLoadout.id,
            scopeID=selectedScope,
            sightID=selectedScopeSight
        )
        LocalSession.add(newScopeLoadout)
        LocalSession.flush()
    LocalSession.commit()



def getWeapons(weaponType: int = None) -> Tuple[List[str], List[int]]:
    """Retrieve a list of weapons names and their corresponding IDs from the database.

    Parameters
    ----------
    weaponType : int, optional
        The weapon type ID to filter by, by default None (no filtering is applied).

    Returns
    -------
    Tuple[List[str], List[int]]
        A tuple containing two lists:
        - A list of weapon names.
        - A list of weapon IDs, where the ID at each index corresponds to the name at the same index in the names list.

    Notes
    -----
    Only used for the UI code!
    """
    query = LocalSession.query(Weapons)
    if weaponType is not None:
           query = query.filter(Weapons.weaponTypeID == weaponType)
    weapons = query.all()
    names = [weapon.name for weapon in weapons]
    ids = [weapon.id for weapon in weapons]

    return names, ids

def getScopes() -> Tuple[List[str], List[int]]:
    """Get a list of all scope names and IDs.

    Returns
    -------
    Tuple[List[str], List[int]]
        - A list of scope names.
        - A list of scope IDs, where the ID at each index corresponds to the name at the same index in the names list.

    Notes
    -----
    Only used for the UI code!
    """
    scopes = LocalSession.query(Scopes).all()
    names = [scope.name for scope in scopes]
    ids = [scope.id for scope in scopes]

    return names, ids

def getSights() -> Tuple[List[str], List[int]]:
    """Get a list of all sight names and IDs.

    Returns
    -------
    Tuple[List[str], List[int]]
        - A list of sight names.
        - A list of sight IDs, where the ID at each index corresponds to the name at the same index in the names list.

    Notes
    -----
    Only used for the UI code!
    """
    sights = LocalSession.query(Sights).all()
    names = [sight.name for sight in sights]
    ids = [sight.id for sight in sights]
    return names, ids

def getEnhancers(enhancerType: int = None) -> Tuple[List[str], List[int]]:
    """Get a list of all enhancer names and IDs.

    Parameters
    ----------
    enhancerType : int, optional
        The ID of the enhancer type to filter by, by default None

    Returns
    -------
    Tuple[List[str], List[int]]
        - A list of enhancer names.
        - A list of enhancer IDs, where the ID at each index corresponds to the name at the same index in the names list.

    Notes
    -----
    Only used for the UI code!
    """
    query = LocalSession.query(EnhancerClass)
    if enhancerType is not None:
        query = query.filter(EnhancerClass.enhancerTypeID == enhancerType)
    enhancers = query.all()
    names = [enhancer.type.name for enhancer in enhancers]
    ids = [enhancer.id for enhancer in enhancers]

    return names, ids

def getAbsorbers(weaponType: int = None) -> Tuple[List[str], List[int]]:
    """Get a list of all absorber names and IDs.

    Parameters
    ----------
    weaponType : int, optional
        The ID of the weapon type to filter by, by default None

    Returns
    -------
    Tuple[List[str], List[int]]
        - A list of absorber names.
        - A list of absorber IDs, where the ID at each index corresponds to the name at the same index in the names list.

    Notes
    -----
    Only used for the UI code!
    """
    query = LocalSession.query(WeaponAbsorbers)
    if weaponType is not None:
        query = query.filter(WeaponAbsorbers.weaponTypeID == weaponType)
    absorbers = query.all()
    names = [absorber.name for absorber in absorbers]
    ids = [absorber.id for absorber in absorbers]

    return names, ids

def getAmplifiers(weaponType: int = None) -> Tuple[List[str], List[int]]:
    """
    Get a list of amplifiers with their names and IDs.

    Parameters
    ----------
    weaponType : int, optional
        If specified, only amplifiers for the specified weapon type will be returned. 
        The default value is None, which means all amplifiers will be returned.

    Returns
    -------
    Tuple[List[str], List[int]]
        A tuple containing two lists:
        - A list of amplifier names.
        - A list of amplifier IDs, where the ID at each index corresponds to the name at the same index in the names list.
    
    Notes
    -----
    Only used for the UI code!

    """
    query = LocalSession.query(WeaponAmps)
    if weaponType is not None:
        query = query.filter(WeaponAmps.weaponTypeID == weaponType)
    amplifiers = query.all()
    names = [amplifier.name for amplifier in amplifiers]
    ids = [amplifier.id for amplifier in amplifiers]

    return names, ids

def getSelectedWeapon(selectedWeaponID: int) -> Dict[str, Union[Weapons, List[Tuple[int, str]]]]:
    """
    Get the selected weapon with its associated amplifiers.

    Parameters
    ----------
    selectedWeaponID : int
        The ID of the selected weapon.

    Returns
    -------
    Dict[str, Union[Weapons, List[Tuple[int, str]]]]
        A dictionary containing two key-value pairs:
        - "weapon": the selected weapon object
        - "amps": a tuple containing two lists:
            - a list of amplifier names
            - a list of amplifier IDs, where the ID at each index corresponds to the name at the same index in the names list.

    Notes
    -----
    Only used for the UI code!

    """
    selectedWeapon = LocalSession.query(Weapons).filter_by(id=selectedWeaponID).first()
    ampNames = [amp.name for amp in selectedWeapon.type.amps]
    ampIds = [amp.id for amp in selectedWeapon.type.amps]
    amps = (ampNames, ampIds)

    return {"weapon": selectedWeapon, "amps": amps}

# TODO (long term) eventually also keep track of weapons that can reach over 100 attacks / min. as the game has a hard cap on 100 attacks per minute and then decay and ammo burn goes up.
def getCostPerShot(loadout: Union[WeaponLoadout, int]):
    """
    Calculate the cost per shot for a given WeaponLoadout.

    Parameters
    ----------
    loadout : Union[WeaponLoadout, int]
        The WeaponLoadout for which to calculate the cost per shot. If an integer is passed, it will be treated as the id of the WeaponLoadout in the database.

    Returns
    -------
    Decimal
        The cost per shot in PEDs (Project Entropia Dollars).

    Notes
    -----
    The cost per shot is calculated as follows:
        - Calculate the enhancer multiplier based on the number of damage enhancers and economy enhancers in the loadout.
        - Calculate the actual decay and ammo burn of the weapon based on the enhancer multiplier.
        - Add the decay and ammo burn of any attached amplifiers, sights, and scopes.
        - Calculate the cost per shot in PEDs as the sum of ammo burn, decay, and enhancer breaking cost.

    Examples
    --------
    >>> loadout = WeaponLoadout(id=1, weapon=Weapon(id=1, decay=1.0, ammoBurn=10), enhancerLoadout=[EnhancerLoadout(id=1, enhancer=Enhancer(id=1, type=EnhancerType(name='Damage'), ttValue=2.5))])
    >>> getCostPerShot(loadout)
    Decimal('0.1100')

    >>> getCostPerShot(1)
    Decimal('0.1100')
    """
    costPerShot = None
    selectedLoadout = loadout if isinstance(loadout, WeaponLoadout) else LocalSession.query(WeaponLoadout).filter_by(id=loadout.id).first()

    weaponDecay = None
    weaponAmmoBurn = None
    damageEnhancers = 0
    economyEnhancers = 0
    enhancerValue = 0

    for enhancers in selectedLoadout.enhancerLoadout:
        if enhancers.enhancer.type.name == "Damage":
            damageEnhancers += 1
        if enhancers.enhancer.type.name == "Economy":
            economyEnhancers += 1
        enhancerValue += enhancers.enhancer.ttValue
    
    enhancerMultiplier = 1 + ((0.1 * damageEnhancers) - (0.01 * economyEnhancers))

    weaponDecay = selectedLoadout.weapon.decay * Decimal(enhancerMultiplier)
    weaponAmmoBurn = selectedLoadout.weapon.ammoBurn * enhancerMultiplier

    if selectedLoadout.amplifier is not None:
        weaponDecay += selectedLoadout.amplifier.decay
        weaponAmmoBurn += selectedLoadout.amplifier.ammoBurn

    if selectedLoadout.sight is not None:
        weaponDecay += selectedLoadout.sight.decay

    if selectedLoadout.scopeLoadout is not None:
        weaponDecay += selectedLoadout.scopeLoadout.scope.decay
        if selectedLoadout.scopeLoadout.sight is not None:
            weaponDecay += selectedLoadout.scopeLoadout.sight.decay

    # calc costpershot (also include price of enahncer braking based on the 2500 brake rate of the wiki and tt value of enhancers)
    costPerShot = (Decimal(weaponAmmoBurn) / Decimal(10000)) + (weaponDecay / Decimal(100)) + Decimal(enhancerValue / 2500)

    return costPerShot
