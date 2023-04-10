from sqlalchemy import TEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional

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

    id: Mapped[int] = mapped_column(primary_key=True)
    scopeID: Mapped[int] = mapped_column(ForeignKey("Scopes.id"))
    sightID: Mapped[int] = mapped_column(ForeignKey("Sights.id"), nullable=True)

class WeaponLoadout(Base):
    __tablename__ = "WeaponLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(TEXT,unique=True)
    weaponID: Mapped[int] = mapped_column(ForeignKey("Weapons.id"))
    socketLoadoutID: Mapped[int] = mapped_column(ForeignKey("SocketLoadout.id"), nullable=True)
    socketLoadout: Mapped[Optional["SocketLoadout"]] = relationship(
        back_populates="bp_weaponLoadout",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )
    WeaponAmpID: Mapped[int] = mapped_column(ForeignKey("WeaponAmps.id"), nullable=True)
    scopeLoadoutID: Mapped[int] = mapped_column(ForeignKey("ScopeLoadout.id"), nullable=True)
    sightID: Mapped[int] = mapped_column(ForeignKey("Sights.id"), nullable=True)
    absorberID: Mapped[int] = mapped_column(ForeignKey("WeaponAbsorbers.id"), nullable=True)

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

    def getTypeName(self):
        return f"{self.enhancerTypeName.name}"

class EnhancerLoadout(Base):
    __tablename__ = "EnhancerLoadout"

    id: Mapped[int] = mapped_column(primary_key=True)
    enhancerClassID: Mapped[int] = mapped_column(ForeignKey("EnhancerClass.id"))
    amount: Mapped[int] = mapped_column(default=0)

    # enhancerClass = relationship("EnhancerClass", back_populates="enhancerLoadout")

class SocketLoadout(Base):
    __tablename__ = "SocketLoadout"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    bp_weaponLoadout: Mapped["WeaponLoadout"] = relationship(
        back_populates="socketLoadout",
    )
    enhancerOneID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerTwoID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerThreeID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerFourID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerFiveID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerSixID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerSevenID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerEightID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerNineID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)
    enhancerTenID: Mapped[int] = mapped_column(ForeignKey("EnhancerLoadout.id"), nullable=True)

    # enhancerOne = relationship("EnhancerLoadout", foreign_keys=[enhancerOneID], backref="socketLoadoutOne", cascade="all, delete")
    # enhancerTwo = relationship("EnhancerLoadout", foreign_keys=[enhancerTwoID], backref="socketLoadoutTwo", cascade="all, delete")
    # enhancerThree = relationship("EnhancerLoadout", foreign_keys=[enhancerThreeID], backref="socketLoadoutThree", cascade="all, delete")
    # enhancerFour = relationship("EnhancerLoadout", foreign_keys=[enhancerFourID], backref="socketLoadoutFour", cascade="all, delete")
    # enhancerFive = relationship("EnhancerLoadout", foreign_keys=[enhancerFiveID], backref="socketLoadoutFive", cascade="all, delete")
    # enhancerSix = relationship("EnhancerLoadout", foreign_keys=[enhancerSixID], backref="socketLoadoutSix", cascade="all, delete")
    # enhancerSeven = relationship("EnhancerLoadout", foreign_keys=[enhancerSevenID], backref="socketLoadoutSeven", cascade="all, delete")
    # enhancerEight = relationship("EnhancerLoadout", foreign_keys=[enhancerEightID], backref="socketLoadoutEight", cascade="all, delete")
    # enhancerNine = relationship("EnhancerLoadout", foreign_keys=[enhancerNineID], backref="socketLoadoutNine", cascade="all, delete")
    # enhancerTen = relationship("EnhancerLoadout", foreign_keys=[enhancerTenID], backref="socketLoadoutTen", cascade="all, delete")

    # @property
    # def enhancers(self):
    #     return [self.enhancerOne, self.enhancerTwo, self.enhancerThree,
    #             self.enhancerFour, self.enhancerFive, self.enhancerSix,
    #             self.enhancerSeven, self.enhancerEight, self.enhancerNine,
    #             self.enhancerTen]

    """
    Combat moddule tables
    """
    