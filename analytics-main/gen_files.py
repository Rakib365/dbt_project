import os

class DbtProjectGenerator:
    def __init__(self):
        self.tables = [
            "account_types", "accounts", "accounts_statuses", "billing_cycles",
            "brand_language", "brands", "card_types", "clients", "clients_accounts",
            "contracts", "contracts_products", "countries", "credit_debit_transactions",
            "currencies", "gateway_providers", "gateways", "gateways_brands",
            "gateways_card_type", "gateways_currencies", "hook_logs", "hooks",
            "invoice_contracts", "invoice_numbers", "invoice_payments", "invoice_products",
            "invoices", "invoices_categories", "languages", "lead_client_imports",
            "leads", "organisation_stats", "organisations", "products",
            "products_categories", "statuses", "users", "payments_log", "payment_types"
        ]

    def create_directory_structure(self):
        """Create the basic directory structure for the dbt project"""
        directories = [
            "models",
            "models/raw",
            "models/staging",
            "models/transformation",
            "models/reporting",
            "macros",
            "tests",
            "seeds",
            "analyses"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def generate_raw_models(self):
        """Generate raw models for each table"""
        for table in self.tables:
            model_content = f"""{{{{ config(
    materialized='table',
    schema='analytics_raw'
) }}}}

SELECT *
FROM {{{{ source('upmind_rds_tp_upmind', '{table}') }}}}"""
            
            with open(f"models/raw/raw_{table}.sql", "w") as f:
                f.write(model_content)

    def generate_staging_models(self):
        """Generate staging models"""
        staging_models = {
            "accounts_enhanced": self.get_accounts_enhanced_query(),
            "brands_enhanced": self.get_brands_enhanced_query(),
            "clients_enhanced": self.get_clients_enhanced_query()
        }

        for model_name, query in staging_models.items():
            model_content = f"""{{{{ config(
    materialized='view',
    schema='analytics_staging'
) }}}}

{query}"""
            
            with open(f"models/staging/stg_{model_name}.sql", "w") as f:
                f.write(model_content)

    def generate_schema_files(self):
        """Generate schema.yml files for each directory"""
        # Raw schema
        raw_schema_content = """version: 2

models:"""
        for table in self.tables:
            raw_schema_content += f"""
  - name: raw_{table}
    description: Raw data from {table} table
    columns:
      - name: id
        description: Primary key for {table}
        tests:
          - unique
          - not_null
"""
        
        with open("models/raw/schema.yml", "w") as f:
            f.write(raw_schema_content)

        # Staging schema
        staging_schema_content = """version: 2

models:
  - name: stg_accounts_enhanced
    description: Staged accounts data with enhanced fields
    columns:
      - name: id
        description: Primary key
        tests:
          - unique
          - not_null

  - name: stg_brands_enhanced
    description: Staged brands data with enhanced fields
    columns:
      - name: id
        description: Primary key
        tests:
          - unique
          - not_null

  - name: stg_clients_enhanced
    description: Staged clients data with enhanced fields
    columns:
      - name: id
        description: Primary key
        tests:
          - unique
          - not_null
"""
        
        with open("models/staging/schema.yml", "w") as f:
            f.write(staging_schema_content)

        # Empty schema files for transformation and reporting
        empty_schema = """version: 2

models:
"""
        
        with open("models/transformation/schema.yml", "w") as f:
            f.write(empty_schema)
        
        with open("models/reporting/schema.yml", "w") as f:
            f.write(empty_schema)

    def generate_sources_yml(self):
        """Generate sources.yml file"""
        sources_content = """version: 2

sources:
  - name: upmind_rds_tp_upmind
    database: upmind-datawarehouse
    schema: upmind_rds_tp_upmind
    loader: fivetran
    loaded_at_field: _fivetran_synced
    tables:"""

        for table in self.tables:
            sources_content += f"""
      - name: {table}
        identifier: {table}
        freshness:
          warn_after:
            count: 24
            period: hour
          error_after:
            count: 48
            period: hour
        columns:
          - name: id
            description: Primary key of {table}
            tests:
              - unique
              - not_null
"""
        
        with open("models/sources.yml", "w") as f:
            f.write(sources_content)

    def generate_dbt_project_yml(self):
        """Generate dbt_project.yml file"""
        project_content = """name: 'analytics'
version: '1.0.0'
config-version: 2

profile: 'analytics'

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
analysis-paths: ["analyses"]
macro-paths: ["macros"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  analytics:
    raw:
      +materialized: table
      +schema: analytics_raw
    staging:
      +materialized: view
      +schema: analytics_staging
    transformation:
      +materialized: table
      +schema: analytics_transformation
    reporting:
      +materialized: table
      +schema: analytics_reporting
"""
        
        with open("dbt_project.yml", "w") as f:
            f.write(project_content)

    def get_accounts_enhanced_query(self):
        return """SELECT
  accounts.id,
  accounts.user_id,
  accounts.brand_id,
  accounts.created_at,
  accounts.updated_at,
  accounts.name,
  accounts.status_id,
  accounts.account_type_id,
  accounts.currency_id,
  accounts.pricelist_id,
  accounts.invoice_account_id,
  accounts.multi_currency_balance,
  accounts.topup_enabled,
  accounts.preferred_payment_currency_id,
  acc_status.id AS status_id,
  acc_status.status,
  acc_types.id AS account_type_id,
  acc_types.name AS account_type_name,
  acc_types.code AS account_type_code,
  acc_types.description AS account_type_description
FROM {{ ref('raw_accounts') }} accounts
LEFT JOIN {{ ref('raw_accounts_statuses') }} acc_status 
    ON accounts.status_id = acc_status.id
LEFT JOIN {{ ref('raw_account_types') }} acc_types 
    ON accounts.account_type_id = acc_types.id"""

    def get_brands_enhanced_query(self):
        return """SELECT
  brands.id,
  brands.name,
  brands.created_at,
  brands.updated_at,
  brands.code,
  brands.brand_type,
  brands.currency_id,
  brands.pricelist_id,
  brands.country_id,
  brands.company_name,
  brands.tax_type,
  brands.language_id,
  brands.prefix,
  brands.autoapply,
  brands.payment_days_term,
  brands.create_invoice_term,
  brands.user_id,
  brands.deleted_at,
  brands.org_id,
  brands.wipe_data,
  brands.demo_data_import_id,
  brands.region_id,
  brands.hourly_emails,
  bl.id AS brand_language_id,
  bl.brand_id AS brand_language_brand_id,
  bl.language_id AS brand_language_language_id
FROM {{ ref('raw_brands') }} brands
LEFT JOIN {{ ref('raw_brand_language') }} bl 
    ON brands.language_id = bl.id"""

    def get_clients_enhanced_query(self):
        return """SELECT
  c.id,
  c.credit,
  c.order_template_code,
  c.consolidate_invoice,
  c.last_login,
  c.consolidation_day,
  c.deleted_at,
  c.brand_id,
  c.user_id,
  c.tax_type,
  c.location_town,
  c.org_id,
  c.block_new_tickets_from_email,
  c.fraud_status,
  c.location_country_code,
  c.is_guest,
  c.apply_credit,
  c.created_at,
  c.has_login,
  c.upmind_org_user_id,
  c.updated_at,
  c.interface_language_id,
  c.fraud_policy,
  c.invoice_consolidation_enabled,
  c.never_suspend,
  c.verified,
  c.before_due_date_charge_interval,
  c.ip_address,
  c.document_language_id,
  c.never_close,
  c.reseller_account_id,
  c.invoice_consolidation_base_rule_day_of_week,
  c.provider_2fa_id
FROM {{ ref('raw_clients') }} c
WHERE c.brand_id = 1"""

    def generate_project(self):
        """Generate the complete dbt project"""
        print("Generating dbt project structure...")
        self.create_directory_structure()
        
        print("Generating raw models...")
        self.generate_raw_models()
        
        print("Generating staging models...")
        self.generate_staging_models()
        
        print("Generating schema files...")
        self.generate_schema_files()
        
        print("Generating sources.yml...")
        self.generate_sources_yml()
        
        print("Generating dbt_project.yml...")
        self.generate_dbt_project_yml()
        
        print("Project generation complete!")

if __name__ == "__main__":
    generator = DbtProjectGenerator()
    generator.generate_project()