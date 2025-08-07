## 📂 Project Structure

```
VC_Capstone_Project/
├── README.md                     # Quick-start guide
├── UML.png                       # Visual UML class diagram

├── APIs/                         # API-based data enrichment
│   ├── countries_api.py
│   ├── extract_currency_api.py
│   ├── manager_json.py
│   └── sectors.py

├── benchmarks/                   # Benchmark fund & performance modules
│   ├── benchmarck_characteristics.py
│   ├── benchmark_account_association.py
│   ├── benchmark_general_information.py
│   └── benchmark_performance.py

├── holdings/                     # Holdings and exit logic
│   ├── exit.py
│   ├── holdings.py
│   └── holdings_metrics.py

├── portfolio/                    # Core portfolio entity generation
│   ├── account.py
│   ├── fund_manager.py
│   ├── portfolio_account_association.py
│   └── portfolio_general_info.py

├── product/                      # Product & performance logic
│   ├── performance.py
│   └── product_master.py

├── JSON/                         # Cached API responses
│   ├── currency_lookup.json
│   ├── gics.json
│   ├── manager_data.json
│   ├── sectors.json
│   └── synthetic_countries.json

├── CSVs/                         # Final export tables (for Snowflake)
│   ├── accounts.csv
│   ├── df_benchmark_account_association.csv
│   ├── df_benchmark_characteristics.csv
│   ├── df_benchmark_general.csv
│   ├── df_benchmark_performance.csv
│   ├── fund_managers.csv
│   ├── holdings.csv
│   ├── holdings_metrics.csv
│   ├── portfolio_account_map.csv
│   ├── portfolio_general_info.csv
│   └── product_master.csv

└── __pycache__/                  # Python bytecode cache
```
