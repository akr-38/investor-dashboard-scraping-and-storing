import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.registrations_utils import insert_into_registrations

# insert_from_csv_full.py
import pandas as pd
from database import SessionLocal

def push(year: int, quarter: int):
    filename = f"{year}_Q{quarter}.csv"
    # Read CSV
    df = pd.read_csv(filename)
    
    if df.empty:
        print("CSV file is empty. Nothing to insert.")
        return

    # Start DB session
    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            maker_name = str(row["Maker"]).strip('"')  # remove stray quotes
            
            # Insert each category if it's > 0
            if row["2W"] > 0:
                insert_into_registrations(session, maker_name, "2W", year, quarter, int(row["2W"]))
            if row["3W"] > 0:
                insert_into_registrations(session, maker_name, "3W", year, quarter, int(row["3W"]))
            if row["4W"] > 0:
                insert_into_registrations(session, maker_name, "4W", year, quarter, int(row["4W"]))
        
        print(f"✅ Inserted all rows from {filename} into DB.")
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{filename} deleted")
        else:
            print(f"{filename} not found in current directory")
    finally:
        session.close()

# if __name__ == "__main__":
#     push("2021_Q1.csv", 2021, 1)

