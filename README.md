# Sayod 111 Intelligence Radar SDKs (Python & JavaScript/TypeScript)

Zero-dependency official clients for **Sayod 111 Commercial Intelligence Radar** (`https://sayod111.com/`):
- **Agency E-Com Growth Radar** (Shopify Paid Ads + Missing Klaviyo + ATS Hiring)
- **Cyber/GRC Deal Radar** (existing SaaS records and public trust-center metadata)
- **WealthPulse SEC Form ADV RIAs** (12,019+ indexed U.S. RIAs with AUM & disclosure indicators)
- **Biotech & MedTech Federal Radar** (NIH RePORTER Grants, ClinicalTrials.gov v2, openFDA 510(k))

## Python quick start

From a clone of this repository, run `python -m pip install ./python` with Python 3.10 or newer.
```python
from sayod111_radar import RadarClient

client = RadarClient()
print(client.health())
print(client.freshness())
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

## Public resources

- [SAYOD 111](https://sayod111.com/)
- [Data room and sample exports](https://sayod111.com/data-room)
- [Three-domain batch audit](https://sayod111.com/batch-audit)
- [Remote MCP endpoint](https://mcp.sayod111.com/mcp)

## Research tools and reference

| Tool | Use |
| --- | --- |
| [SEC adviser lookup](https://sayod111.com/sec-lookup) | Search Form ADV advisers and export matching rows. |
| [Federal recompete finder](https://sayod111.com/recompete-finder) | Filter awards by agency, NAICS and obligated amount. |
| [DMARC scorecard](https://sayod111.com/dmarc-scorecard) | Inspect public DNS and homepage evidence. |
| [Clay configuration generator](https://sayod111.com/clay-generator) | Copy a client configuration for one of eight networks. |

Review sample records in the [institutional data room](https://sayod111.com/data-room). Integrations can use the [API specification](https://sayod111.com/openapi.json), [AI search guide](https://sayod111.com/llms.txt) and [hosted MCP endpoint](https://mcp.sayod111.com/mcp).
