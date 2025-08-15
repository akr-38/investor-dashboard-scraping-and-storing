# scripts/seed_categories.py

import os
import sys

from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Ensure root path is in sys.path so imports work when running script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import VehicleCategory

load_dotenv()

def seed_categories():
    session: Session = SessionLocal()

    try:
        categories_to_seed = ["2W", "3W", "4W"]
        category_ids = {}

        for code in categories_to_seed:
            category = session.query(VehicleCategory).filter_by(code=code).first()
            if not category:
                category = VehicleCategory(code=code)
                session.add(category)
                session.commit()  # commit so ID is generated
                session.refresh(category)
            category_ids[code] = category.category_id

        # Make sure utils directory exists
        utils_dir = os.path.join(os.path.dirname(__file__), "..", "utils")
        os.makedirs(utils_dir, exist_ok=True)

        # Write IDs to utils/category_ids.py
        category_ids_path = os.path.join(utils_dir, "category_ids.py")
        with open(category_ids_path, "w") as f:
            f.write(f"CATEGORY_ID_2W = {category_ids.get('2W')}\n")
            f.write(f"CATEGORY_ID_3W = {category_ids.get('3W')}\n")
            f.write(f"CATEGORY_ID_4W = {category_ids.get('4W')}\n")

        print("✅ Categories seeded and IDs saved in utils/category_ids.py")

    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding categories: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_categories()
