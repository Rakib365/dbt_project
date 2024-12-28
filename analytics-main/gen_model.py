import os

# List of all tables
tables = [
    "account_types",
    "accounts",
    "accounts_statuses",
    "billing_cycles",
    "brand_language",
    "brands",
    "card_types",
    "clients",
    "clients_accounts",
    "contracts",
    "contracts_products",
    "countries",
    "credit_debit_transactions",
    "currencies",
    "gateway_providers",
    "gateways",
    "gateways_brands",
    "gateways_card_type",
    "gateways_currencies",
    "hook_logs",
    "hooks",
    "invoice_contracts",
    "invoice_numbers",
    "invoice_payments",
    "invoice_products",
    "invoices",
    "invoices_categories",
    "languages",
    "lead_client_imports",
    "leads",
    "organisation_stats",
    "organisations",
    "products",
    "products_categories",
    "statuses",
    "users",
    "payments_log",
    "payment_types"
]

# Create models directory if it doesn't exist
os.makedirs("models/raw", exist_ok=True)

# Generate raw model SQL files
for table in tables:
    model_name = f"raw_{table}"
    file_content = f"""{{{{ config(
    materialized='table',
    schema='analytics_raw'
) }}}}

SELECT *
FROM {{{{ source('upmind_rds_tp_upmind', '{table}') }}}}"""
    
    with open(f"models/raw/{model_name}.sql", "w") as f:
        f.write(file_content)

# Generate schema.yml
schema_content = """version: 2

sources:
  - name: upmind_rds_tp_upmind
    database: upmind-datawarehouse
    schema: upmind_rds_tp_upmind
    tables:"""

for table in tables:
    schema_content += f"""
      - name: {table}
        description: Raw data from {table} table"""

with open("models/raw/schema.yml", "w") as f:
    f.write(schema_content)

print("Generated raw models and schema.yml successfully!")