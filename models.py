from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Manufacturer(Base):
    __tablename__ = "manufacturers"

    manufacturer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    registration_stats = relationship("RegistrationStat", back_populates="manufacturer")


class VehicleCategory(Base):
    __tablename__ = "vehicle_categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)  # '2W', '3W', '4W'

    registration_stats = relationship("RegistrationStat", back_populates="category")


class RegistrationStat(Base):
    __tablename__ = "registration_stats"

    stat_id = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.manufacturer_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("vehicle_categories.category_id"), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    registration_count = Column(Integer, nullable=False)

    manufacturer = relationship("Manufacturer", back_populates="registration_stats")
    category = relationship("VehicleCategory", back_populates="registration_stats")

    __table_args__ = (
        UniqueConstraint("manufacturer_id", "category_id", "year", "quarter", name="uq_registration_unique"),
    )
