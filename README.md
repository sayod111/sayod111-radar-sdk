# Sayod 111 Intelligence Radar SDKs (Python & JavaScript/TypeScript)

Zero-dependency official clients for **Sayod 111 Commercial Intelligence Radar** (`https://sayod111.com/`):
- **Agency E-Com Growth Radar** (Shopify Paid Ads + Missing Klaviyo + ATS Hiring)
- **Cyber/GRC Deal Radar** (existing SaaS records and public trust-center metadata)
- **WealthPulse SEC Form ADV RIAs** (12,019+ indexed U.S. RIAs with AUM & disclosure indicators)
- **Biotech & MedTech Federal Radar** (NIH RePORTER Grants, ClinicalTrials.gov v2, openFDA 510(k))

## Quick Links
- Zero-Login Live Auditors & Portal: https://sayod111.com/
- Shareable Executive Dossier: https://sayod111.com/report.html?domain=coros.com&mode=shopify
- Interactive API Playground: https://sayod111.com/playground.html
- API Docs & OpenAPI 3.1.0: https://sayod111.com/docs.html
- Bulk Cloud Engines on Apify Store: https://apify.com/sayod111

## Python quick start

From a clone of this repository, run `python -m pip install ./python` with Python 3.10 or newer.
```python
from sayod111_radar import RadarClient

client = RadarClient(api_key="dp_live_YOUR_KEY")  # omit api_key for free public routes
print(client.health())
print(client.live_audit("coros.com", mode="shopify"))
print(client.ria_search(q="vanguard", limit=5))
print(client.biotech_search(q="a", limit=5))
```

## JavaScript / TypeScript Quick Start (Node 18+ / Browser ESM)
```js
import { RadarClient } from "./javascript/index.mjs";

const client = new RadarClient({ apiKey: process.env.SAYOD111_API_KEY });
console.log(await client.health());
console.log(await client.liveAudit("coros.com", "shopify"));
```
