from sqlalchemy import Text, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional, List
from decimal import Decimal

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
    type: Mapped[str] =  mapped_column(Text)

class Weapons(Base):
    __tablename__ = "Weapons"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(Text)
    damage: Mapped[int] = mapped_column(default=0)
    firerate: Mapped[int] = mapped_column(default=0)
    decay: Mapped[Decimal] = mapped_column(Numeric, default=0)
    ammoBurn: Mapped[int] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

    type: Mapped["WeaponTypes"] = relationship(backref="weapons")

class Sights(Base):
    __tablename__ = "Sights"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(Text)
    decay: Mapped[Decimal] = mapped_column(Numeric, default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

    type: Mapped["WeaponTypes"] = relationship(backref="sights")

class Scopes(Base):
    __tablename__ = "Scopes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(Text)
    decay: Mapped[Decimal] = mapped_column(Numeric, default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

    type: Mapped["WeaponTypes"] = relationship(backref="scopes")

class WeaponAmps(Base):
    __tablename__ = "WeaponAmps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(Text)
    decay: Mapped[Decimal] = mapped_column(Numeric, default=0)
    ammoBurn: Mapped[int] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

    type: Mapped["WeaponTypes"] = relationship(backref="amps")

class WeaponAbsorbers(Base):
    __tablename__ = "WeaponAbsorbers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(Text)
    decay: Mapped[Decimal] = mapped_column(Numeric, default=0)
    absorbPercent: Mapped[float] = mapped_column(default=0)
    weaponTypeID: Mapped[int] = mapped_column(ForeignKey("WeaponTypes.id"))

    type: Mapped["WeaponTypes"] = relationship(backref="absorbers")

# Loadout
class ScopeLoadout(Base):
    __tablename__ = "ScopeLoadout"

    weaponLoadoutID: Mapped[int] = mapped_column(ForeignKey("WeaponLoadout.id"), primary_key=True)
    scopeID: Mapped[int] = mapped_column(ForeignKey("Scopes.id"))
    sightID: Mapped[Optional[int]] = mapped_column(ForeignKey("Sights.id"), nullable=True)

    bp_weaponLoadout: Mapped["WeaponLoadout"] = relationship(
        back_populates="scopeLoadout",
    )

    scope: Mapped[Optional["Scopes"]] = relationship(
        foreign_keys=[scopeID]
    )

    sight: Mapped[Optional["Sights"]] = relationship(
        foreign_keys=[sightID])

class WeaponLoadout(Base):
    __tablename__ = "WeaponLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)
    weaponID: Mapped[int] = mapped_column(ForeignKey("Weapons.id"))
    amplifierID: Mapped[Optional[int]] = mapped_column(ForeignKey("WeaponAmps.id"), nullable=True)
    sightID: Mapped[Optional[int]] = mapped_column(ForeignKey("Sights.id"), nullable=True)
    absorberID: Mapped[Optional[int]] = mapped_column(ForeignKey("WeaponAbsorbers.id"), nullable=True)

    weapon: Mapped["Weapons"] = relationship(
        foreign_keys=[weaponID])
    
    amplifier: Mapped[Optional["WeaponAmps"]] = relationship(
        foreign_keys=[amplifierID])
    
    absorber: Mapped[Optional["WeaponAbsorbers"]] = relationship(
        foreign_keys=[absorberID])
    
    sight: Mapped[Optional["Sights"]] = relationship(
        foreign_keys=[sightID])
    
    enhancerLoadout: Mapped[Optional[List["EnhancerLoadout"]]] = relationship(
        back_populates="bp_weaponLoadout",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

    scopeLoadout: Mapped[Optional["ScopeLoadout"]] = relationship(
        back_populates="bp_weaponLoadout",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

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
    name: Mapped[str] = mapped_column(Text)


class EnhancerTypeNames(Base):
    __tablename__ = "EnhancerTypeNames"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)


class EnhancerTypes(Base):
    __tablename__ = "EnhancerTypes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Text)


class EnhancerClass(Base):
    __tablename__ = "EnhancerClass"

    id: Mapped[int] = mapped_column(primary_key=True)
    enhancerNameID: Mapped[int] = mapped_column(ForeignKey("EnhancerNames.id"))
    enhancerTypeNameID: Mapped[int] = mapped_column(ForeignKey("EnhancerTypeNames.id"))
    enhancerEffectID: Mapped[int] = mapped_column(ForeignKey("EnhancerEffects.id"), default=1)
    enhancerTypeID: Mapped[int] = mapped_column(ForeignKey("EnhancerTypes.id"))
    ttValue: Mapped[float] = mapped_column(Numeric)

    type: Mapped["EnhancerTypeNames"] = relationship(foreign_keys=[enhancerTypeNameID])
    effect: Mapped["EnhancerEffects"] = relationship(foreign_keys=[enhancerEffectID])

class EnhancerLoadout(Base):
    __tablename__ = "EnhancerLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    weaponLoadoutID: Mapped[int] = mapped_column(ForeignKey("WeaponLoadout.id"))
    socket: Mapped[int] = mapped_column()
    enhancerClassID: Mapped[int] = mapped_column(ForeignKey("EnhancerClass.id"))
    amount: Mapped[int] = mapped_column(default=0)

    enhancer: Mapped["EnhancerClass"] = relationship(foreign_keys=[enhancerClassID])
    bp_weaponLoadout: Mapped["WeaponLoadout"] = relationship(
        back_populates="enhancerLoadout",
    )

    """
    HuntingRun tables
    """

class LoggingRun(Base):
    __tablename__ = "LoggingRun"

    id: Mapped[int] = mapped_column(primary_key=True)
    timeStart: Mapped[int] = mapped_column()
    timeStop: Mapped[int] = mapped_column()
    notes: Mapped[str] = mapped_column(Text)
    globalcount: Mapped[int] = mapped_column(default=0)
    hofcount: Mapped[int] = mapped_column(default=0)
    costTotal: Mapped[int] = mapped_column(default=0)
    costExtraSpend: Mapped[int] = mapped_column(default=0)
    totalHeals: Mapped[int] = mapped_column(default=0)
    totalHealed: Mapped[float] = mapped_column(default=0.0)
    totalAttacks: Mapped[int] = mapped_column(default=0)
    totalDamage: Mapped[float] = mapped_column(default=0.0)
    totalCrits: Mapped[int] = mapped_column(default=0)
    totalMisses: Mapped[int] = mapped_column(default=0)
    skillProcs: Mapped[int] = mapped_column(default=0)

    lootedItems: Mapped[Optional[List["LootItem"]]] = relationship(
        back_populates="bp_loggingRun",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

    skillGains: Mapped[Optional[List["SkillItem"]]] = relationship(
        back_populates="bp_loggingRun",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

    enhancerBreaks: Mapped[Optional[List["EnhancerItem"]]] = relationship(
        back_populates="bp_loggingRun",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

    multiplierGraph: Mapped[Optional[List["MultiplierGraphData"]]] = relationship(
        back_populates="bp_loggingRun",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

    returnOverTimeGraph: Mapped[Optional[List["ReturnOverTimeGraphData"]]] = relationship(
        back_populates="bp_loggingRun",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )


class LootItem(Base):
    __tablename__ = "LootItem"

    __table_args__ = (
        UniqueConstraint('LoggingRunID', 'name', name='uq_loggingRunID_name'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    LoggingRunID: Mapped[int] = mapped_column(ForeignKey("LoggingRun.id"))
    name: Mapped[int] = mapped_column(Text)
    amount: Mapped[int] = mapped_column(default=0)
    value: Mapped[float] = mapped_column(default=0.0)

    bp_loggingRun: Mapped["LoggingRun"] = relationship(
        back_populates="lootedItems",
    )

class SkillItem(Base):
    __tablename__ = "SkillItem"

    __table_args__ = (
        UniqueConstraint('LoggingRunID', 'name', name='uq_loggingRunID_name'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    LoggingRunID: Mapped[int] = mapped_column(ForeignKey("LoggingRun.id"))
    name: Mapped[int] = mapped_column(Text)
    value: Mapped[float] = mapped_column(default=0.0)
    procs: Mapped[int] = mapped_column()

    bp_loggingRun: Mapped["LoggingRun"] = relationship(
        back_populates="skillGains",
    )

class EnhancerItem(Base):
    __tablename__ = "EnhancerItem"

    __table_args__ = (
        UniqueConstraint('LoggingRunID', 'name', name='uq_loggingRunID_name'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    LoggingRunID: Mapped[int] = mapped_column(ForeignKey("LoggingRun.id"))
    name: Mapped[int] = mapped_column(Text)
    socket: Mapped[int] = mapped_column()

    bp_loggingRun: Mapped["LoggingRun"] = relationship(
        back_populates="enhancerBreaks",
    )

# graphs from runs
class MultiplierGraphData(Base):
    __tablename__ = "MultiplierGraphData"


    id: Mapped[int] = mapped_column(primary_key=True)
    LoggingRunID: Mapped[int] = mapped_column(ForeignKey("LoggingRun.id"))
    lootInstanceCost: Mapped[float] = mapped_column(default=0)
    lootInstanceValue: Mapped[float] = mapped_column(default=0)

    bp_loggingRun: Mapped["LoggingRun"] = relationship(
        back_populates="multiplierGraph",
    )

class ReturnOverTimeGraphData(Base):
    __tablename__ = "ReturnOverTimeGraphData"


    id: Mapped[int] = mapped_column(primary_key=True)
    LoggingRunID: Mapped[int] = mapped_column(ForeignKey("LoggingRun.id"))
    returnOverTime: Mapped[float] = mapped_column(default=0)

    bp_loggingRun: Mapped["LoggingRun"] = relationship(
        back_populates="returnOverTimeGraph",
    )