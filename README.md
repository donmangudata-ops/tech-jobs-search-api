# Tech Jobs Search API for Python and MCP: AI, startup and remote tech jobs

Search the open jobs of 824 startups and tech, AI, remote-first and European companies by title, place, remote work, seniority, salary and posted date, from Python, curl or an AI agent.

The jobs come from [Tech Jobs Search](https://apify.com/conserving_celerytop/tech-jobs-search), a hosted Actor on Apify. Each search reads the companies' career pages when you run it, so every result is open that day. This repo holds a Python quick start, a curl example and MCP setup for 5 AI clients. There is no scraper code here. The example code is MIT licensed.

## What it returns

One row per matching job, newest first:

```json
{
  "rowType": "job",
  "companyName": "Linear",
  "title": "Senior Backend Engineer",
  "location": "Remote (Europe)",
  "countryCode": null,
  "workplaceType": "remote",
  "seniority": "senior",
  "jobFunction": "engineering",
  "salaryAnnualMin": null,
  "postedAt": "2026-09-24T14:03:00.000Z",
  "url": "https://..."
}
```

- The same fields as the Actor [ATS Jobs API](https://apify.com/conserving_celerytop/live-career-page-jobs-api), so code written for one reads the other.
- Five company lists, all picked by default: `ai-companies` (179), `tech-companies` (311), `remote-first` (90), `europe-tech` (65) and `startups` (250). A company in two lists is read once: 824 companies in all. The lists are refreshed monthly.
- Filters: `titleIncludes`, `titleExcludes`, `location`, `remoteOnly`, `workplaceTypes`, `seniorities`, `jobFunctions`, `employmentTypes`, `hasSalary`, `minAnnualSalary`, `postedSince`.
- `maxResults` (default 200, up to 10,000) caps the rows, and with them the price.
- A search of all five lists takes about 3 minutes.

## Python quick start

You need an Apify account and its API token (Apify Console > **Settings** > **API & Integrations**).

```bash
pip install "apify-client>=3.2,<4"
export APIFY_TOKEN=<YOUR_APIFY_TOKEN>
```

```python
import os
from decimal import Decimal
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("conserving_celerytop/tech-jobs-search").call(
    run_input={"titleIncludes": ["machine learning"], "remoteOnly": True, "postedSince": "7 days", "maxResults": 50},
    max_total_charge_usd=Decimal("0.10"),
)
for job in client.dataset(run.default_dataset_id).iterate_items():
    print(job["companyName"], "|", job["title"], "|", job["location"], "|", job["url"])
```

50 jobs cost at most $0.06. The full script is [examples/quickstart.py](examples/quickstart.py): it takes the title words as arguments and saves the jobs to `jobs.csv`.

```bash
pip install -r examples/requirements.txt
python examples/quickstart.py "data engineer"
```

## curl

This request starts a search, waits up to 300 seconds and returns the rows.

```bash
curl -X POST "https://api.apify.com/v2/acts/conserving_celerytop~tech-jobs-search/run-sync-get-dataset-items?maxTotalChargeUsd=0.12" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titleIncludes": ["product designer"], "location": "Berlin", "postedSince": "30 days", "maxResults": 100}'
```

Add `&format=csv` to the URL for CSV.

## Use it as an MCP tool in Claude, Cursor, VS Code or ChatGPT

Apify hosts the MCP server. This URL adds only this Actor as a tool:

```
https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/tech-jobs-search
```

On first use, the client opens a browser window to sign in to Apify (OAuth). Searches are charged to your Apify account at the price below.

**Claude Code**

```bash
claude mcp add --transport http tech-jobs-search "https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/tech-jobs-search"
```

Then run `/mcp` in Claude Code and sign in.

**Claude (desktop app and claude.ai)**

**Settings** > **Connectors** > **Add custom connector**. Name: `Tech Jobs Search`. URL: the URL above.

**Cursor** (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "tech-jobs-search": {
      "url": "https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/tech-jobs-search"
    }
  }
}
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "tech-jobs-search": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=fetch-actor-details,conserving_celerytop/tech-jobs-search"
    }
  }
}
```

**ChatGPT** (Developer mode on)

**Settings** > **Apps & Connectors** > **Create**. MCP Server URL: the URL above. Authentication: OAuth.

To use a token instead of OAuth, send the header `Authorization: Bearer <YOUR_APIFY_TOKEN>`. Then ask, for example: "Find remote senior Python jobs at AI companies posted this week, at most 30."

## Pricing

$1.15 per 1,000 matching jobs you receive ($1.15 on Starter, $1.05 on Scale, $1.00 on Business), so 100 jobs cost $0.115, with no Apify platform usage fees on top. Companies with no matching job cost nothing, and a search that finds nothing costs only Apify's start event. `maxResults` and `max_total_charge_usd` both cap the price of a run: when the limit is reached, the run stops and you receive only the jobs you paid for. The [Store page](https://apify.com/conserving_celerytop/tech-jobs-search) has the current price.

## Guides

Step-by-step guides with full Python code:

- [Hiring signals for sales: score your account list from job postings](https://donmangudata-ops.github.io/hiring-signals-for-sales/)
- [Greenhouse jobs API in Python](https://donmangudata-ops.github.io/greenhouse-jobs-api-python/)
- [Lever postings API in Python](https://donmangudata-ops.github.io/lever-postings-api-python/)
- [Ashby job board API in Python](https://donmangudata-ops.github.io/ashby-job-board-api-python/)

## Related

- [ATS Jobs API](https://apify.com/conserving_celerytop/live-career-page-jobs-api): every open job at the companies you name, from 22 job boards, priced per company (see its Store page).
- [Live Jobs HTTP API](https://apify.com/conserving_celerytop/live-jobs-http-api): the same job data in one GET or POST request.

Missing a company? Tell us on the **Issues** tab of the [Actor's page](https://apify.com/conserving_celerytop/tech-jobs-search).

## Not affiliated

This repo and the Actor are not affiliated with or endorsed by Greenhouse, Lever, Ashby, Workday or any other job board, or by the companies in the lists. Their names are trademarks of their owners. The Actor reads only job postings that companies publish on public job boards, with no login.

## License

MIT. See [LICENSE](LICENSE). Made by Don Mangu.
