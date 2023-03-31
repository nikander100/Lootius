from sqlalchemy import TEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

"""
# default type mapping, deriving the type for mapped_column()
# from a Mapped[] annotation
type_map: Dict[Type[Any], TypeEngine[Any]] = {
    bool: types.Boolean(),
    bytes: types.LargeBinary(),
    datetime.date: types.Date(),
    datetime.datetime: types.DateTime(),
    datetime.time: types.Time(),
    datetime.timedelta: types.Interval(),
    decimal.Decimal: types.Numeric(),
    float: types.Float(),
    int: types.Integer(),
    str: types.String(),
    uuid.UUID: types.Uuid(),
}"""

"""
New database setup based on ORM to keep sql in code to a minimum.
"""
class Base(DeclarativeBase):
    pass

"""
Weapons related tables
"""

# Raw data
class WeaponTypes(Base):
    __tablename__ = "WeaponTypes"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] =  mapped_column(TEXT)

class Weapons(Base):
    __tablename__ = "Weapons"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(TEXT)
    damage: Mapped[int] = mapped_column(default=0)
    firerate: Mapped[int] = mapped_column(default=0)
    decay: Mapped[float] = mapped_column(default=0)
    ammoBurn: Mapped[int] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

class Sights(Base):
    __tablename__ = "Sights"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(TEXT)
    decay: Mapped[float] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

class Scopes(Base):
    __tablename__ = "Scopes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(TEXT)
    decay: Mapped[float] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

class WeaponAmps(Base):
    __tablename__ = "WeaponAmps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(TEXT)
    decay: Mapped[float] = mapped_column(default=0)
    ammoBurn: Mapped[int] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

class WeaponAbsorbers(Base):
    __tablename__ = "WeaponAbsorbers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(TEXT)
    decay: Mapped[float] = mapped_column(default=0)
    absorbPercent: Mapped[float] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

# Loadout
class ScopeLoadout(Base):
    __tablename__ = "ScopeLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    scopeID: Mapped[int] = mapped_column(ForeignKey("Scopes.id"))
    sightID: Mapped[int] = mapped_column(ForeignKey("Sights.id"))

class WeaponLoadout(Base):
    __tablename__ = "WeaponLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(TEXT,unique=True)
    weaponID: Mapped[int] = mapped_column(ForeignKey("Weapons.id"))
    socketsID: Mapped[int] = mapped_column(ForeignKey("Sockets.id"))
    WeaponAmpID: Mapped[int] = mapped_column(ForeignKey("WeaponAmps.id"))
    scopeLoadoutID: Mapped[int] = mapped_column(ForeignKey("ScopeLoadout.id"))
    sightID: Mapped[int] = mapped_column(ForeignKey("Sights.id"))
    absorberID: Mapped[int] = mapped_column(ForeignKey("WeaponAbsorbers.id"))

"""
Enhancer tables
"""

class EnhancerEffects(Base):
    __tablename__ = "EnhancerEffects"

    id: Mapped[int] = mapped_column(primary_key=True)
    decayAmount: Mapped[float] = mapped_column(default=0)
    bonusAmount: Mapped[float] = mapped_column(default=0)

class EnhancerNames(Base):
    __tablename__ = "EnhancerNames"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)

class EnhancerTypeNames(Base):
    __tablename__ = "EnhancerTypeNames"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)

class EnhancerTypes(Base):
    __tablename__ = "EnhancerTypes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(TEXT)

class EnhancerClass(Base):
    __tablename__ = "EnhancerClass"

    id: Mapped[int] = mapped_column(primary_key=True)
    enhancerNameID: Mapped[int] = mapped_column(ForeignKey("EnhancerNames.id"))
    enhancerTypeNameID: Mapped[int] = mapped_column(ForeignKey("EnhancerTypeNames.id"))
    enhancerEffectID: Mapped[int] = mapped_column(ForeignKey("EnhancerEffects.id"), default=1)
    enhancerTypeID: Mapped[int] = mapped_column(ForeignKey("EnhancerTypes.id"))

class EnhancerLoadout(Base):
    __tablename__ = "EnhancerLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    enhancerClassID: Mapped[int] = mapped_column(ForeignKey("EnhancerClass.id"))
    amount: Mapped[int] = mapped_column(default=0)

class Sockets(Base):
    __tablename__ = "Sockets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    enhancerOneID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerTwoID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerThreeID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerFourID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerFiveID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerSixID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerSevenID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerEightID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerNineID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))
    enhancerTenID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"))

    """
    Combat moddule tables
    """
    