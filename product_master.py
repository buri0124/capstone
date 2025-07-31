# # Product Master
#
# ### Product Master Metadata Logic  
# This section creates a metadata table `product_master_df` for each unique VC product derived from fund-level data.  
# Each product represents a group of funds sharing the same **strategy** and **region**, and is enriched with human-readable names, vehicle structure, and share class tags.
#
# ---
#
# ### Processing Steps
#
# | Step | Description |
# |------|-------------|
# | 1 | Derive unique `(strategy, region)` combinations from `portfolio_general_info_df` |
# | 2 | Map strategy abbreviations (e.g., `EARLY`) to full strategy names (e.g., `Early Stage`) |
# | 3 | Assign product codes in the format `VC_{STRATEGY_ABBR}_{REGION_BLOCK}` |
# | 4 | Randomly assign vehicle type and determine vehicle category |
# | 5 | Generate product name (e.g., `Assette Growth Equity Fund IV`) |
# | 6 | Assign share class as Institutional or Offshore |
# | 7 | Store output in `product_master_df` with 1 row per product group |
#
# ---
#
# ### Output Schema: `product_master_df`
#
# | Column           | Description |
# |------------------|-------------|
# | `PRODUCTCODE`    | Internal product code (e.g., `VC_EARLY_NA`) |
# | `PRODUCTNAME`    | Human-readable product name (e.g., `Assette Growth Equity Fund II`) |
# | `STRATEGY`       | Full strategy name (e.g., `Early Stage`, `Venture Capital`, `Growth Equity`) |
# | `VEHICLETYPE`    | Structure type (e.g., `Separate Account`, `Commingled Fund`) |
# | `VEHICLECATEGORY`| Segregation level (`Segregated` or `Pooled`) |
# | `ASSETCLASS`     | Always set to `Venture Capital` |
# | `SHARECLASS`     | Assigned as `Institutional` or `Offshore` |
# | `REGION_BLOCK`   | Regional classification (e.g., `NA`, `EU`, `AS`, or `GL`)

import pandas as pd
import random

# 1. Strategy & Region Mapping
strategy_abbr = {"Early Stage": "EARLY", "General": "GEN", "Later Stage": "LATE"}
strategy_name_map = {
    "EARLY": "Early Stage",
    "GEN": "Venture Capital",
    "LATE": "Growth Equity"
}
region_map = {
    "United States": "NA", "Canada": "NA",
    "United Kingdom": "EU", "Germany": "EU", "France": "EU",
    "Japan": "AS", "South Korea": "AS"
}

# 2. Add derived columns to portfolio
portfolio_general_info_df["STRATEGY_ABBR"] = portfolio_general_info_df["STRATEGY"].map(strategy_abbr)
portfolio_general_info_df["REGION_BLOCK"] = portfolio_general_info_df["COUNTRY"].map(region_map).fillna("GL")
portfolio_general_info_df["PRODUCT_GROUP"] = (
    portfolio_general_info_df["STRATEGY_ABBR"] + "_" + portfolio_general_info_df["REGION_BLOCK"]
)

# 3. Assign PRODUCTCODEs per group
unique_groups = portfolio_general_info_df["PRODUCT_GROUP"].unique()
productcode_lookup = {
    group: f"VC_{group}" for group in sorted(unique_groups)
}
portfolio_general_info_df["PRODUCTCODE"] = portfolio_general_info_df["PRODUCT_GROUP"].map(productcode_lookup)

# 4. Generate Product Master
vehicle_types = ["Separate Account", "Commingled Fund"]
vehicle_categories = {"Separate Account": "Segregated", "Commingled Fund": "Pooled"}

def assign_shareclass(vt):
    return "Institutional" if "SEPARATE" in vt.upper() else random.choice(["Institutional", "Offshore"])

def generate_product_name(strategy_abbr):
    firm = "Assette"
    label = strategy_name_map[strategy_abbr]
    suffix = random.choice(["Fund I", "Fund II", "Fund III", "Fund IV"])
    return f"{firm} {label} {suffix}"

product_rows = []
for group_key, product_code in productcode_lookup.items():
    strategy_abbr, region = group_key.split("_")
    vt = random.choice(vehicle_types)
    product_rows.append({
        "PRODUCTCODE": product_code,
        "PRODUCTNAME": generate_product_name(strategy_abbr),
        "STRATEGY": strategy_name_map[strategy_abbr],
        "VEHICLECATEGORY": vehicle_categories[vt],
        "VEHICLETYPE": vt,
        "ASSETCLASS": "Venture Capital",
        "SHARECLASS": assign_shareclass(vt),
        "REGION_BLOCK": region
    })

product_master_df = pd.DataFrame(product_rows)
product_master_df



# #Exit
#
# ### Exit Generation Logic
#
# The exit event simulator creates `vc_exit_df` by **linking directly to actual holdings data** from `holdings_df` (e.g., generated via `holdings.py`).  
# It samples real companies held by each fund to simulate exits.
#
# ---
#
# ### Processing Steps
#
# | Step | Description |
# |------|-------------|
# | 1    | For each fund in `portfolio_general_info_df`, filter corresponding holdings from `holdings_df` |
# | 2    | Skip funds with no holdings (only active portfolios are eligible) |
# | 3    | Randomly select ~20% of funds to simulate exits |
# | 4    | Sample 1–5 existing companies from the fund's holdings to simulate exit events |
# | 5    | For each exited company: Assign exit type (IPO, Acquisition, Write-off), Generate exit date 3–9 years after fund close  
# | 6    | Construct one row per exit and append to `vc_exit_df` |
#
# ---
#
# ### Output Schema: `vc_exit_df`
#
# | Column | Description |
# |--------|-------------|
# | PORTFOLIOCODE | VC fund identifier (from portfolio) |
# | TICKER | Company ID (from holdings) |
# | COMPANY | Company name (from holdings) |
# | EXITTYPE | Type of exit (IPO, Acquisition, Write-off) |
# | ACQUIRERTYPE | Strategic or Financial Sponsor |
# | MOIC | Multiple on Invested Capital |
# | EXITVALUE_MILLION_USD | Exit proceeds in millions of USD |
# | EXITDATE | Exit completion date |
#
# ---

# Exit-Holdings Integration
# This updated exit event generator links directly to the holdings_df

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Exit settings
exit_types = ['IPO', 'Acquisition', 'Write-off']
acquirer_types = ['Strategic', 'Financial Sponsor']
today = datetime.today()

vc_exit_events = []

# Load or generate holdings_df (should already exist in pipeline)
# Example: holdings_df = pd.read_csv("synthetic_holdings.csv")
# Must contain: PORTFOLIOCODE, TICKER, ISSUENAME

for _, row in portfolio_general_info_df.iterrows():
    fund_id = row["PORTFOLIOCODE"]
    close_date = datetime.strptime(str(row["CLOSE_DATE"]), "%Y-%m-%d")

    # Filter holdings belonging to this fund
    fund_holdings = holdings_df[holdings_df["PORTFOLIOCODE"] == fund_id]

    # Skip if no holdings available
    if fund_holdings.empty:
        continue

    # ~20% of funds have exits
    if random.random() > 0.8:  # Keep ~20%
        num_exits = random.randint(1, 5)

        # Prevent sampling more exits than companies
        num_exits = min(num_exits, len(fund_holdings))

        # Randomly select companies to exit
        exited_companies = fund_holdings.sample(n=num_exits)

        for _, company_row in exited_companies.iterrows():
            company_id = company_row["TICKER"]
            company_name = company_row["ISSUENAME"]

            # Generate realistic exit date
            exit_years = int(np.random.choice(
                [3, 4, 5, 6, 7, 8, 9],
                p=[0.05, 0.1, 0.2, 0.25, 0.25, 0.1, 0.05]
            ))
            exit_date = close_date + timedelta(days=exit_years * 365)

            # Cap to today if in future
            if exit_date > today:
                exit_date = today - timedelta(days=random.randint(0, 365))

            exit_type = random.choice(exit_types)

            if exit_type == "Write-off":
                moic = 0.0
                exit_value = 0.0
            else:
                moic = round(np.random.uniform(0.5, 5.0), 2)
                exit_value = round(np.random.uniform(10, 500), 2)

            exit_event = {
                "PORTFOLIOCODE": fund_id,
                "TICKER": company_id,
                "COMPANY": company_name,
                "EXITTYPE": exit_type,
                "ACQUIRERTYPE": random.choice(acquirer_types),
                "MOIC": moic,
                "EXITVALUE_MILLION_USD": exit_value,
                "EXITDATE": exit_date.strftime("%Y-%m-%d")
            }

            vc_exit_events.append(exit_event)

# Convert to DataFrame
vc_exit_df = pd.DataFrame(vc_exit_events)


if __name__ == "__main__":
    # Generate product master metadata and export to CSV
    product_master_df = pd.DataFrame(product_rows)
    product_master_df.to_csv("product_master.csv", index=False)
