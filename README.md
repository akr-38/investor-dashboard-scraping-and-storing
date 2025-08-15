
# Investor Dashboard - Data Scraping and Storage

This repository contains the scripts and configurations for scraping vehicle registration data from the Vahan Dashboard, processing it, and storing it in a PostgreSQL database using Supabase.
This is just a part of the whole investor dashboard project: **[Investor Dashboard Project](https://github.com/akr-38/investors-dashboard-project/blob/main/README.md)**

## ⚙️ Tech Stack

  * **Language:** Python
  * **Database:** PostgreSQL (Supabase)
  * **Libraries:** `alembic`, `sqlalchemy`, `pandas`, `selenium`, `beautifulsoup4`, `psycopg2`, `python-dotenv`

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
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
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

This will populate the database with vehicle categories, as shown in this table:

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

The script will handle the scraping and store the processed data in the `registration_stats` table of your database. The final data schema will look like this:
A sample of the stored data is shown below:
