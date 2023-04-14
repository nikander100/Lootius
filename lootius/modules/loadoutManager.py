from models.databaseModel import Weapons, Sights, Scopes, EnhancerClass, WeaponAbsorbers, WeaponLoadout, ScopeLoadout, EnhancerLoadout, WeaponAmps
from database import db
from typing import List, Tuple, Dict, Union
from sqlalchemy.orm import joinedload

Session = db.DB.getSession()

def setLoadout(selectedName, selectedWeapon, selectedAmp, selectedAbs, selectedScope, selectedScopeSight, selectedSight, selectedEnhancers):
    with Session.begin() as session:

        weaponLoadout = WeaponLoadout(
            name=selectedName,
            weaponID=selectedWeapon,
            WeaponAmpID=selectedAmp,
            sightID=selectedSight,
            absorberID=selectedAbs
        )
        session.add(weaponLoadout)
        session.flush()

        newEnhancerLoadouts = []
        for enhancer in selectedEnhancers:
            if enhancer[1] is not None and enhancer[2] != 0:
                newEnhancerLoadouts.append(EnhancerLoadout(
                weaponLoadoutID=weaponLoadout.id,
                socket=enhancer[0],
                enhancerClassID=enhancer[1],
                amount=enhancer[2],
                ))
    
        session.add_all(newEnhancerLoadouts)
        session.flush()
        
        if selectedScope is not None:
            newScopeLoadout = ScopeLoadout(
                weaponLoadoutID=weaponLoadout.id,
                scopeID=selectedScope,
                sightID=selectedScopeSight
            )
            session.add(newScopeLoadout)
            session.flush()



def getWeapons(weaponType: int = None) -> Tuple[List[str], List[int]]:
    with Session() as session:
        query = session.query(Weapons)
        if weaponType is not None:
            query = query.filter(Weapons.weaponTypeID == weaponType)
        weapons = query.all()
        names = [weapon.name for weapon in weapons]
        ids = [weapon.id for weapon in weapons]
    return names, ids

def getScopes() -> Tuple[List[str], List[int]]:
    with Session() as session:
        scopes = session.query(Scopes).all()
        names = [scope.name for scope in scopes]
        ids = [scope.id for scope in scopes]
    return names, ids

def getSights() -> Tuple[List[str], List[int]]:
    with Session() as session:
        sights = session.query(Sights).all()
        names = [sight.name for sight in sights]
        ids = [sight.id for sight in sights]
    return names, ids

def getEnhancers() -> Tuple[List[str], List[int]]:
    with Session() as session:
        enhancers = session.query(EnhancerClass).filter(EnhancerClass.enhancerTypeID == 3).all()
        names = [enhancer.enhancerTypeName.name for enhancer in enhancers]
        ids = [enhancer.id for enhancer in enhancers]
    return names, ids

def getAbsorbers(weaponType: int = None) -> Tuple[List[str], List[int]]:
    with Session() as session:
        query = session.query(WeaponAbsorbers)
        if weaponType is not None:
            query = query.filter(WeaponAbsorbers.weaponTypeID == weaponType)
        absorbers = query.all()
        names = [absorber.name for absorber in absorbers]
        ids = [absorber.id for absorber in absorbers]
    return names, ids

def getAmplifiers(weaponType: int = None) -> Tuple[List[str], List[int]]:
    with Session() as session:
        query = session.query(WeaponAmps)
        if weaponType is not None:
            query = query.filter(WeaponAmps.weaponTypeID == weaponType)
        amplifiers = query.all()
        names = [amplifier.name for amplifier in amplifiers]
        ids = [amplifier.id for amplifier in amplifiers]
    return names, ids

def getSelectedWeapon(selectedWeaponID: int) -> Dict[str, Union[Weapons, List[Tuple[int, str]]]]:
    with Session() as session:
        selectedWeapon = session.query(Weapons).options(joinedload(Weapons.type)).filter_by(id=selectedWeaponID).first()
        ampNames = [amp.name for amp in selectedWeapon.type.amps]
        ampIds = [amp.id for amp in selectedWeapon.type.amps]
        amps = (ampNames, ampIds)
    return {"weapon": selectedWeapon, "amps": amps}