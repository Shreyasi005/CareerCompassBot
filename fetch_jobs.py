"""
Fetch real job postings from the Adzuna API and save them in the same
format as jobs.csv, so you can merge them into your dataset.

SETUP (one-time):
1. Go to https://developer.adzuna.com/ and sign up for a free account.
2. Create an "App" — you'll get an APP_ID and APP_KEY.
3. Paste them into the two variables below.

USAGE:
    python fetch_jobs.py
This will create a file called fetched_jobs.csv with real postings you can
review and then copy/merge into jobs.csv.
"""

import requests
import pandas as pd

APP_ID = "YOUR_APP_ID_HERE"     # <-- replace with your Adzuna app id
APP_KEY = "YOUR_APP_KEY_HERE"   # <-- replace with your Adzuna app key

COUNTRY = "in"          # "in" = India. Adzuna also supports "gb", "us", etc.
SEARCH_TERM = "software developer"
RESULTS_PER_PAGE = 20
PAGE = 1                # Adzuna paginates results; increase to get more


def fetch_jobs():
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{PAGE}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": SEARCH_TERM,
        "content-type": "application/json",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()   # will raise a clear error if the key is wrong
    data = response.json()

    rows = []
    for job in data.get("results", []):
        rows.append({
            "job_title": job.get("title", "").strip(),
            "company": job.get("company", {}).get("display_name", "Unknown"),
            "description": job.get("description", "").strip()[:400],  # trim long text
            "required_skills": "",  # Adzuna doesn't give a clean skills list —
                                     # fill this in by hand after reviewing
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    if APP_ID == "YOUR_APP_ID_HERE":
        print("Please add your Adzuna APP_ID and APP_KEY before running this.")
    else:
        df = fetch_jobs()
        df.to_csv("fetched_jobs.csv", index=False)
        print(f"Saved {len(df)} postings to fetched_jobs.csv — review before merging into jobs.csv")
