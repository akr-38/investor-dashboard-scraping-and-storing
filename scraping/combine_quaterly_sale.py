import pandas as pd
from pathlib import Path
import os

def combine(year: int, quarter: int, months: list = [], output_dir: str = "."):
    """
    Combine monthly sales CSVs into a quarterly total file.
    
    Args:
        year (int): The year (e.g., 2021)
        quarter (int): The quarter number (1-4)
        months (list): List of month names in uppercase (e.g., ["JAN", "FEB", "MAR"])
        output_dir (str): Folder where the output file should be stored.
    """
    month_data = {
        1: ["JAN", "FEB", "MAR"],
        2: ["APR", "MAY", "JUN"],
        3: ["JUL", "AUG", "SEP"],
        4: ["OCT", "NOV", "DEC"]
    }
    months = month_data[quarter]
    dfs = []

    # Read each month file
    for month in months:
        file_name = f"{year}_{month}_processed.csv"
        file_path = Path(file_name)

        if not file_path.exists():
            print(f"❌ Skipping {file_name} — file not found.")
            continue

        df = pd.read_csv(file_path)
        dfs.append(df)

    if not dfs:
        print("❌ No files found to process.")
        return

    # Combine and sum values per Maker
    combined_df = pd.concat(dfs)
    quarterly_df = combined_df.groupby("Maker", as_index=False)[["2W", "3W", "4W"]].sum()

    # Save as quarterly CSV
    output_file = Path(output_dir) / f"{year}_Q{quarter}.csv"
    quarterly_df.to_csv(output_file, index=False)

    for month in months:
        filename = f"{year}_{month}_processed.csv"
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{filename} deleted")
        else:
            print(f"{filename} not found in current directory")

    print(f"✅ Quarterly sales saved to {output_file}")

# Example usage:
#combine_quarterly_sales(2021, 1)
