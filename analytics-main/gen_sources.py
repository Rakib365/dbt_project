import os

def generate_sources_yml():
    sources_content = """version: 2

sources:
  - name: upmind_rds_tp_upmind
    database: upmind-datawarehouse
    schema: upmind_rds_tp_upmind
    loader: fivetran
    loaded_at_field: _fivetran_synced
    tables:"""

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

    for table in tables:
        sources_content += f"""
      - name: {table}
        identifier: {table}
        freshness:
          warn_after: {{count: 24, period: hour}}
          error_after: {{count: 48, period: hour}}
        columns:
          - name: id
            description: Primary key of {table}
            tests:
              - unique
              - not_null"""

    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Write the sources.yml file
    with open("models/sources.yml", "w") as f:
        f.write(sources_content)

    print("Generated sources.yml successfully!")

if __name__ == "__main__":
    generate_sources_yml()