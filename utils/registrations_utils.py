# utils.py

import os
from sqlalchemy.orm import Session
from models import Manufacturer, VehicleCategory, RegistrationStat
from database import SessionLocal
from .category_ids import CATEGORY_ID_2W, CATEGORY_ID_3W, CATEGORY_ID_4W

def get_or_create_manufacturer_id(session: Session, name: str) -> int:
    """
    Returns manufacturer_id, creates it if not exists.
    """
    manufacturer = session.query(Manufacturer).filter_by(name=name).first()
    if manufacturer:
        return manufacturer.manufacturer_id

    new_manufacturer = Manufacturer(name=name)
    session.add(new_manufacturer)
    session.commit()
    session.refresh(new_manufacturer)
    return new_manufacturer.manufacturer_id


def insert_into_registrations(
    session: Session,
    manufacturer_name: str,
    vehicle_category_code: str,
    year: int,
    quarter: int,
    registration_count: int
):
    """
    Insert a row into registration_stats using manufacturer_name and category_code.
    """
    # Get manufacturer_id (create if not exists)
    manufacturer_id = get_or_create_manufacturer_id(session, manufacturer_name)

    # Map category code to stored global IDs
    category_map = {
        "2W": CATEGORY_ID_2W,
        "3W": CATEGORY_ID_3W,
        "4W": CATEGORY_ID_4W
    }

    category_id = category_map.get(vehicle_category_code)
    if not category_id:
        raise ValueError(f"Invalid category code: {vehicle_category_code}")

    new_record = RegistrationStat(
        manufacturer_id=manufacturer_id,
        category_id=category_id,
        year=year,
        quarter=quarter,
        registration_count=registration_count
    )
    session.add(new_record)
    session.commit()
    print(f"✅ Inserted registration for {manufacturer_name} ({vehicle_category_code}) - {year} Q{quarter}")

