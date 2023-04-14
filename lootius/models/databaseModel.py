from sqlalchemy import TEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional, List

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

    type = relationship("WeaponTypes", backref="weapons")

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

    type = relationship("WeaponTypes", backref="amps")

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

    weaponLoadoutID: Mapped[int] = mapped_column(ForeignKey("WeaponLoadout.id"), primary_key=True)
    scopeID: Mapped[int] = mapped_column(ForeignKey("Scopes.id"))
    sightID: Mapped[Optional[int]] = mapped_column(ForeignKey("Sights.id"), nullable=True)

    bp_weaponLoadout: Mapped["WeaponLoadout"] = relationship(
        back_populates="scopeLoadout",
    )

class WeaponLoadout(Base):
    __tablename__ = "WeaponLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(TEXT,unique=True)
    weaponID: Mapped[int] = mapped_column(ForeignKey("Weapons.id"))
    WeaponAmpID: Mapped[Optional[int]] = mapped_column(ForeignKey("WeaponAmps.id"), nullable=True)
    sightID: Mapped[Optional[int]] = mapped_column(ForeignKey("Sights.id"), nullable=True)
    absorberID: Mapped[Optional[int]] = mapped_column(ForeignKey("WeaponAbsorbers.id"), nullable=True)

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

    enhancerTypeName = relationship("EnhancerTypeNames", foreign_keys=[enhancerTypeNameID])

class EnhancerLoadout(Base):
    __tablename__ = "EnhancerLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    weaponLoadoutID: Mapped[int] = mapped_column(ForeignKey("WeaponLoadout.id"))
    socket: Mapped[int] = mapped_column()
    enhancerClassID: Mapped[int] = mapped_column(ForeignKey("EnhancerClass.id"))
    amount: Mapped[int] = mapped_column(default=0)

    bp_weaponLoadout: Mapped["WeaponLoadout"] = relationship(
        back_populates="enhancerLoadout",
    )

    """
    Combat moddule tables
    """