"""Search open tech, AI, startup and remote jobs at 824 companies, saved to jobs.csv.

Uses Tech Jobs Search, a hosted Actor on Apify.

Install: pip install -r requirements.txt
Run:     APIFY_TOKEN=<YOUR_APIFY_TOKEN> python quickstart.py [title words ...]
Example: APIFY_TOKEN=<YOUR_APIFY_TOKEN> python quickstart.py "data engineer" "analytics engineer"

Your token is in Apify Console > Settings > API & Integrations.
Price: $1.15 per 1,000 matching jobs, with no usage fees.
MAX_RESULTS = 100 caps this run at $0.115.
"""

import csv
import os
import sys
from decimal import Decimal

from apify_client import ApifyClient

ACTOR_ID = "conserving_celerytop/tech-jobs-search"
MAX_RESULTS = 100
MAX_CHARGE_USD = Decimal("0.12")
COLUMNS = [
    "companyName", "title", "department", "location", "countryCode", "workplaceType",
    "seniority", "jobFunction", "salaryAnnualMin", "salaryAnnualMax", "salaryCurrency",
    "postedAt", "url",
]


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first, for example: APIFY_TOKEN=<YOUR_APIFY_TOKEN> python quickstart.py")

    run_input = {
        # Lists: ai-companies, tech-companies, remote-first, europe-tech, startups (all five by default).
        "companyLists": ["ai-companies", "tech-companies", "remote-first", "europe-tech", "startups"],
        "titleIncludes": sys.argv[1:] or ["engineer"],
        "postedSince": "7 days",
        "maxResults": MAX_RESULTS,
    }

    client = ApifyClient(token)
    # Starts the search and waits until it finishes (about 3 minutes for all five lists).
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=MAX_CHARGE_USD)
    if run is None or run.status != "SUCCEEDED":
        sys.exit(f"The run did not succeed: {run.status if run else 'no run'}")

    saved = 0
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for job in client.dataset(run.default_dataset_id).iterate_items():
            if job.get("rowType") == "job":
                writer.writerow(job)
                saved += 1

    print(f"Saved {saved} jobs to jobs.csv, newest first")


if __name__ == "__main__":
    main()
