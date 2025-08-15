import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_month(driver, month_str: str):
    """
    Select the month in the month dropdown.

    Parameters:
    - driver: Selenium WebDriver instance (should be the same session).
    - month_str: Month as a 3-letter uppercase string, e.g. "JAN", "FEB", ..., "DEC".

    Assumes the page is already loaded with year, y-axis, x-axis set, and refresh clicked.
    """
    wait = WebDriverWait(driver, 10)

    # Map month strings to 1-based index matching dropdown options
    month_map = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4,
        "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
        "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
    }

    if month_str not in month_map:
        raise ValueError(f"Invalid month string '{month_str}'. Must be one of {list(month_map.keys())}")

    month_index = month_map[month_str]

    try:
        time.sleep(1)
        print("Clicking Month dropdown label to open options...")
        month_dropdown_label = wait.until(EC.element_to_be_clickable((By.ID, "groupingTable:selectMonth_label")))
        month_dropdown_label.click()
        time.sleep(1)

        month_option_id = f"groupingTable:selectMonth_{month_index}"
        print(f"Selecting month '{month_str}' with option id {month_option_id}...")
        month_option = wait.until(EC.element_to_be_clickable((By.ID, month_option_id)))
        month_option.click()
        time.sleep(1)
        print(f"Successfully selected month '{month_str}'.")

    except Exception as e:
        print(f"Error selecting month dropdown option: {e}")
        print("Dumping page source snippet for debug:")
        print(driver.page_source[:1000])
        raise

def run_full_flow(year: int, month_str: str, output_csv: str):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)
    driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")

    try:
        # YEAR DROPDOWN
        print("Clicking Year dropdown label to open options...")
        year_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#selectedYear_label")))
        year_dropdown.click()
        time.sleep(1)

        num = (2025 - year) + 2
        year_option_selector = f"#selectedYear_{num}"

        print(f"Selecting year {year} with selector {year_option_selector}...")
        year_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, year_option_selector)))
        year_option.click()
        time.sleep(1)
        print(f"Successfully selected year {year}.")

        # Y-AXIS DROPDOWN
        print("Clicking Y-axis dropdown label to open options...")
        y_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#yaxisVar_label")))
        y_dropdown.click()
        time.sleep(1)

        print("Clicking 'Maker' option in Y-axis dropdown...")
        maker_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(text(),'Maker')]")
        ))
        maker_option.click()
        time.sleep(1)
        print("Successfully selected 'Maker' in Y-axis dropdown.")

        # X-AXIS DROPDOWN
        print("Clicking X-axis dropdown label to open options...")
        x_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#xaxisVar_label")))
        x_dropdown.click()
        time.sleep(1)

        print("Clicking 'Vehicle Category' option in X-axis dropdown...")
        option = wait.until(EC.element_to_be_clickable((By.ID, "xaxisVar_0")))
        option.click()
        time.sleep(1)
        print("Successfully selected 'Vehicle Category' in X-axis dropdown.")

        # REFRESH BUTTON
        print("Waiting for the Refresh button to be clickable...")
        refresh_button = wait.until(EC.element_to_be_clickable((By.ID, "j_idt66")))

        print("Clicking the Refresh button...")
        refresh_button.click()
        print("Refresh button clicked successfully.")
        time.sleep(2)  # wait for refresh to complete

        # MONTH SELECTION
        select_month(driver, month_str)
        time.sleep(1)  # wait after month selection

        # SCRAPE TABLE
        print("Waiting for the table data area to load...")
        wait.until(EC.presence_of_element_located((By.ID, "groupingTable_data")))
        time.sleep(1)
        # Define static headers
        headers = [
            "S No", "Maker", "2WIC", "2WN", "2WT",
            "3WIC", "3WN", "3WT",
            "4WIC", "HGV", "HMV", "HPV",
            "LGV", "LMV", "LPV", "MGV", "MMV", "MPV",
            "OTH", "TOTAL"
        ]

        print(f"Using static headers: {headers}")

        with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            while True:
                print("Scraping current page rows...")
                time.sleep(1)
                rows = driver.find_elements(By.CSS_SELECTOR, "#groupingTable_data tr")
                time.sleep(1)
                for row in rows:
                    cols = [col.text.strip() for col in row.find_elements(By.TAG_NAME, "td")]
                    if cols:  # only write rows with data
                        writer.writerow(cols)

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "#groupingTable_paginator_bottom a.ui-paginator-next")
                    if "ui-state-disabled" in next_button.get_attribute("class"):
                        print("Reached last page of the table.")
                        break

                    print("Clicking next page button...")
                    time.sleep(1)  # slow before click
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(1)  # slow after click

                except Exception:
                    print("Next button not found or error encountered, stopping pagination.")
                    break

        print(f"Data saved successfully to {output_csv}")

    except Exception as e:
        print(f"Error during full flow: {e}")
        print(driver.page_source[:1000])

    finally:
        driver.quit()
        print("Browser closed.")

# if __name__ == "__main__":
#     run_full_flow(year=2022, month_str="MAY", output_csv="2022_MAY.csv")
