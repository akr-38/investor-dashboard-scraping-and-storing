import fetching_and_storing_csv
import processing_and_storing_category_wise


def find(year: int, quarter: int):
    month_data = {
        1: ["JAN", "FEB", "MAR"],
        2: ["APR", "MAY", "JUN"],
        3: ["JUL", "AUG", "SEP"],
        4: ["OCT", "NOV", "DEC"]
    }
    months = month_data[quarter]
    for month in months:
        output_csv = f"{year}_{month}.csv"
        print(f"\n=== Running flow for {year} {month} ===")
        
        # Step 1: Scrape and save CSV
        fetching_and_storing_csv.run_full_flow(year, month, output_csv)
        
        # Step 2: Process the scraped CSV
        processing_and_storing_category_wise.process_vehicle_csv(output_csv)

