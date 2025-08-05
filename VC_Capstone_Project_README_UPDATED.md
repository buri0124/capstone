# VC_Capstone_Project

This project simulates a synthetic venture capital (VC) investment ecosystem from the perspective of institutional Limited Partners (LPs). It is aligned with Assette’s Snowflake schema and supports automated fact sheet generation, benchmarking, and performance reporting.

The dataset includes portfolios, investor accounts, fund-manager relationships, holdings, exits, product classifications, and performance metrics. Data is generated using modular Python scripts, enriched with metadata from real-world APIs (country, currency, and sector), and exported as structured CSV/JSON files.

All final outputs are Snowflake-ready and designed to mirror institutional data pipelines.

---

## UML Class Diagram

The following UML diagram visualizes the structure and relationships among core tables such as PORTFOLIO_GENERAL_INFO, ACCOUNT, PERFORMANCE, HOLDINGS, Benchmark and PRODUCT_MASTER.

![ERD](./UML.png)

---

## Project Structure

```
VC_Capstone_Project/
├── README.md                  Quick-start guide (this file)
├── UML.png                    Visual ERD diagram

├── APIs/                      API-based data enrichment
│   ├── countries_api.py
│   ├── extract_currency_api.py
│   ├── sectors.py
│   └── manager_json.py

├── JSON/                      Cached API results (lookups)
│   ├── synthetic_countries.json
│   ├── currency_lookup.json
│   └── sectors.json, gics.json

├── portfolio/                 Core entity generators
│   ├── account.py
│   ├── fund_manager.py
│   ├── portfolio_general_info.py
│   ├── portfolio_account_association.py
│   ├── performance.py
│   └── product_master.py

├── holdings/                  Holdings and exit logic
│   ├── holdings.py
│   ├── exit.py
│   └── holdings_metrics.py

├── CSVs/                      Final export tables (for Snowflake)
│   ├── accounts.csv
│   ├── holdings.csv
│   ├── holdings_metrics.csv
│   ├── portfolio_general_info.csv
│   ├── portfolio_account_map.csv
│   └── product_master.csv

└── __pycache__/               Python bytecode cache
```

---

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run core modules in order:
- APIs (to generate JSON)
- portfolio/
- holdings/
- Export to CSVs

3. Upload CSV outputs to Snowflake.

---

## Notes

- All code follows a modular structure and naming aligned with institutional conventions.
- JSON outputs ensure reproducibility and offline access to metadata.
