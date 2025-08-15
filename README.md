
# Investor Dashboard - Data Scraping and Storage

This repository contains the scripts and configurations for scraping vehicle registration data from the Vahan Dashboard, processing it, and storing it in a PostgreSQL database using Supabase.
This is just a part of the whole investor dashboard project: **[Investor Dashboard Project](https://github.com/akr-38/investors-dashboard-project/blob/main/README.md)**

## ⚙️ Tech Stack

  * **Language:** Python
  * **Database:** PostgreSQL (Supabase)
  * **Libraries:** `alembic`, `sqlalchemy`, `pandas`, `selenium`, `psycopg2`, `python-dotenv`

-----

## 🔍 Data Retrieval and Processing Logic

This project uses an automated pipeline to handle data from the Vahan Dashboard and prepare it for the database. The process is as follows:
<img width="923" height="283" alt="{3A9F71E8-4D94-47E7-AFEF-566161BEDE9C}" src="https://github.com/user-attachments/assets/ec919161-3ce9-4771-9174-0427d9426290" />

1.  **Web Scraping:** The script uses **Selenium** to programmatically navigate the Vahan Dashboard. It selects specific values for the `Y-Axis` (Maker) and `X-Axis` (Vehicle Category), chooses the `Year`, and then iterates through each month.
2.  **Data Extraction:** After selecting each month and clicking the "Refresh" button, **Selenium** is used to extract the relevant data from the webpage.
3.  **Local Storage:** The extracted data for each month is temporarily stored as a CSV file in the repository's directory.
4.  **Data Processing:** The script then reads the CSVs and processes the raw data. It aggregates the registration counts for various categories (e.g., summing all `2W` sub-categories into a single `2W` count).
5.  **Quarterly Aggregation:** Monthly data is grouped into quarters, with the final aggregated count for `2W`, `3W`, and `4W` registrations for that quarter.
6.  **Database Insertion:** The cleaned, aggregated quarterly data is then inserted into the `registration_stats` table in the PostgreSQL database.

This fully automated process ensures a consistent and reliable data source for the backend API.

-----

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

  * **Python 3.9+**
  * **A web browser** (e.g., Google Chrome or Firefox)
  * **The corresponding web driver** for your browser (e.g., ChromeDriver or GeckoDriver)

## 🚀 Getting Started

Follow these steps to set up the database and populate it with data.

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/akr-38/investor-dashboard-scraping-and-storing.git
cd investor-dashboard-scraping-and-storing
```

### Step 2: Set up the Python Environment

Create and activate a virtual environment to manage project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install all the required Python libraries using the `pip` command.

```bash
pip install alembic sqlalchemy pandas selenium beautifulsoup4 psycopg2 python-dotenv
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project's root directory and add your Supabase/PostgreSQL connection details. These variables are used by the `database.py` file to establish a connection.

```ini
# .env
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_HOST=<your_database_host>
DB_PORT=<your_database_port>
DB_NAME=<your_database_name>
```

### Step 5: Set up the Database Schema

This project uses `alembic` for database migrations. Run the migration scripts to create the necessary tables.

```bash
alembic upgrade head
```

Next, seed the `vehicle_categories` table with the initial data.

```bash
python scripts/seed_categories.py
```

### Step 6: Update the Scraper Configuration

To ensure the scraper works correctly, you need to update a specific line of code in the `fetching_and_storing_csv.py` file with the correct element ID of the refresh button from the Vahan Dashboard.

  * Open the Vahan Dashboard website.
  * Inspect the "Refresh" button and copy its element ID.
  * Paste this ID into **line 101** of `scraping/fetching_and_storing_csv.py`.

### Step 7: Run the Scraper

Once the database is set up and the scraper is configured, you can run the main script to start the scraping and data storage process.

```bash
python main.py
```

The script will handle the scraping and store the processed data in the `registration_stats` table of your database.
