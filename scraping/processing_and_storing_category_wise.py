import pandas as pd
import os

def process_vehicle_csv(filename):
    # Read the original CSV
    df = pd.read_csv(filename)

    # Identify numeric columns (everything except S No and Maker)
    numeric_cols = df.columns.drop(["S No", "Maker"])

    # Remove commas and convert to int
    for col in numeric_cols:
        df[col] = df[col].replace({',': ''}, regex=True).astype(int)

    # Create new category columns
    df["2W"] = df["2WIC"] + df["2WN"] + df["2WT"]
    df["3W"] = df["3WIC"] + df["3WN"] + df["3WT"]
    df["4W"] = df["4WIC"] + df["LMV"] + df["MMV"] + df["HMV"]

    # Keep only the required columns (drop 'S No')
    df = df[["Maker", "2W", "3W", "4W"]]

    # Remove rows where all 2W, 3W, and 4W are 0
    df = df[~((df["2W"] == 0) & (df["3W"] == 0) & (df["4W"] == 0))]

    # Prepare new filename
    new_filename = f"{os.path.splitext(filename)[0]}_processed.csv"

    # Save to new CSV
    df.to_csv(new_filename, index=False)

    # Delete original file
    os.remove(filename)

    print(f"✅ Processed file saved as: {new_filename}")
    print(f"🗑️ Original file '{filename}' deleted.")

# Example usage:
# process_vehicle_csv("2022_MAY.csv")
