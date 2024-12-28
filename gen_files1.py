import os

class DbtStagingGenerator:
    def __init__(self):
        self.staging_models = {
            "accounts_enhanced": {
                "description": "Enhanced accounts data with status and type information",
                "sql": """
SELECT
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
    ON accounts.account_type_id = acc_types.id""",
                "tests": ["unique", "not_null"]
            },
            
            "brands_enhanced": {
                "description": "Enhanced brands data with language information",
                "sql": """
SELECT
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
    bl.id AS brand_language_id,
    bl.brand_id AS brand_language_brand_id,
    bl.language_id AS brand_language_language_id
FROM {{ ref('raw_brands') }} brands
LEFT JOIN {{ ref('raw_brand_language') }} bl 
    ON brands.language_id = bl.id""",
                "tests": ["unique", "not_null"]
            },
            
            "contracts_enhanced": {
                "description": "Enhanced contracts data with products information",
                "sql": """
SELECT
    c.id,
    c.name,
    c.start_date,
    c.end_date,
    c.next_due_date,
    c.next_invoice_date,
    c.cancellation_date,
    c.cancellation_reason,
    c.activation_date,
    c.status_id,
    c.total_recurrent_amount,
    c.total_amount,
    c.account_id,
    c.user_id,
    c.brand_id,
    c.billing_cycle_months,
    c.currency_id,
    cp.id as contract_product_id,
    cp.product_id,
    cp.status_id as product_status_id,
    cp.trial_end_date,
    cp.amount as product_amount,
    cp.quantity as product_quantity
FROM {{ ref('raw_contracts') }} c
LEFT JOIN {{ ref('raw_contracts_products') }} cp 
    ON c.id = cp.contract_id
WHERE c.brand_id = 1""",
                "tests": ["unique", "not_null"]
            },

            "transactions_enhanced": {
                "description": "Enhanced credit/debit transactions with invoice details",
                "sql": """
SELECT
    t.id,
    t.credit,
    t.debit,
    t.invoice_id,
    t.client_id,
    t.account_id,
    t.user_id,
    t.transaction_id,
    t.reason,
    t.created_at,
    t.updated_at,
    t.payment_log_id,
    t.captured,
    t.currency_id,
    t.transaction_type,
    t.refunded,
    t.amount_refunded,
    t.gateway_id,
    t.amount_captured,
    i.number as invoice_number,
    i.status_id as invoice_status_id,
    i.total_amount as invoice_total_amount,
    i.paid_amount as invoice_paid_amount
FROM {{ ref('raw_credit_debit_transactions') }} t
LEFT JOIN {{ ref('raw_invoices') }} i 
    ON t.invoice_id = i.id
WHERE i.brand_id = 1""",
                "tests": ["unique", "not_null"]
            },

            "invoices_enhanced": {
                "description": "Enhanced invoices with category information",
                "sql": """
SELECT
    i.id,
    i.number,
    i.brand_id,
    i.account_id,
    i.client_id,
    i.gateway_id,
    i.status_id,
    i.created_at,
    i.updated_at,
    i.create_datetime,
    i.due_date,
    i.paid_datetime,
    i.total_amount,
    i.currency_id,
    i.total_discount_amount,
    i.net_amount,
    i.tax_amount,
    i.paid_amount,
    i.contract_id,
    ic.name as category_name,
    ic.slug as category_slug
FROM {{ ref('raw_invoices') }} i
LEFT JOIN {{ ref('raw_invoices_categories') }} ic 
    ON i.category_id = ic.id
WHERE i.brand_id = 1""",
                "tests": ["unique", "not_null"]
            },

            "products_enhanced": {
                "description": "Enhanced products with category information",
                "sql": """
SELECT
    p.id,
    p.name,
    p.short_description,
    p.code,
    p.billing_cycle_months,
    p.clients_can_order,
    p.available_for_sales,
    p.created_at,
    p.updated_at,
    p.brand_id,
    p.user_id,
    p.product_type,
    p.order_type,
    p.unit_quantity,
    p.contract_type,
    p.currency_id,
    p.trial_supported,
    p.trial_duration,
    pc.id as category_id,
    pc.name as category_name,
    pc.description as category_description,
    pc.level as category_level
FROM {{ ref('raw_products') }} p
LEFT JOIN {{ ref('raw_products_categories') }} pc 
    ON p.category_id = pc.id""",
                "tests": ["unique", "not_null"]
            },

            "users_enhanced": {
                "description": "Enhanced users data",
                "sql": """
SELECT
    id,
    bounced,
    created_at,
    updated_at,
    bounced_at,
    interface_language_id,
    document_language_id,
    enabled_2fa,
    provider_2fa_id,
    org_id,
    verified,
    admin,
    active,
    last_login,
    failed_login_attempts,
    notifications_disabled,
    api_user,
    deleted_at
FROM {{ ref('raw_users') }}""",
                "tests": ["unique", "not_null"]
            },

            "leads_enhanced": {
                "description": "Enhanced leads data",
                "sql": """
SELECT
    id,
    is_main,
    is_hidden,
    phone_code,
    phone_country_code,
    client_id,
    assigned_client_at,
    created_at,
    updated_at,
    deleted_at,
    user_id,
    brand_id,
    org_id,
    bounced,
    bounced_at,
    notifications_disabled
FROM {{ ref('raw_leads') }}
WHERE brand_id = 1""",
                "tests": ["unique", "not_null"]
            },


# Add these to the staging_models dictionary in the previous code

            "hook_logs_enhanced": {
                "description": "Enhanced hook logs with hook details",
                "sql": """
SELECT
    hl.id,
    hl.hook_id,
    hl.object_client_id,
    hl.object_account_id,
    hl.object_reseller_account_id,
    hl.object_user_id,
    hl.object_brand_id,
    hl.object_id,
    hl.object_class,
    hl.object_type,
    hl.access_uid,
    hl.access_role,
    hl.access_user_type,
    hl.access_user_id,
    hl.access_ip,
    hl.access_connection_id,
    hl.created_at,
    hl.updated_at,
    hl.context_params,
    h.name as hook_name,
    h.code as hook_code,
    h.event as hook_event,
    h.internal as hook_internal,
    h.notifiable as hook_notifiable,
    h.webhookable as hook_webhookable
FROM {{ ref('raw_hook_logs') }} hl
LEFT JOIN {{ ref('raw_hooks') }} h 
    ON hl.hook_id = h.id""",
                "tests": ["unique", "not_null"]
            },

            "organisations_enhanced": {
                "description": "Enhanced organisations data",
                "sql": """
SELECT
    o.id,
    o.name,
    o.code,
    o.created_at,
    o.updated_at,
    o.affiliate_id,
    o.verified,
    o.pricelist_id,
    o.completed,
    o.upmind_client_id,
    o.upmind_account_id,
    o.share_accounts,
    o.upmind_package_id,
    o.status_id,
    o.upmind_impersonation_enabled,
    o.upmind_impersonation_expiry,
    o.db_connection_id,
    s.code as stat_code,
    s.value as stat_value,
    s.date as stat_date,
    s.brand_id as stat_brand_id
FROM {{ ref('raw_organisations') }} o
LEFT JOIN {{ ref('raw_organisation_stats') }} s 
    ON o.id = s.org_id""",
                "tests": ["unique", "not_null"]
            },

            "organisation_stats_enhanced": {
                "description": "Enhanced organisation stats with additional details",
                "sql": """
SELECT
    s.id,
    s.org_id,
    s.brand_id,
    s.code,
    s.value,
    s.date,
    s.created_at,
    s.updated_at,
    s.deleted_at,
    o.name as org_name,
    o.verified as org_verified,
    o.completed as org_completed
FROM {{ ref('raw_organisation_stats') }} s
LEFT JOIN {{ ref('raw_organisations') }} o 
    ON s.org_id = o.id""",
                "tests": ["unique", "not_null"]
            },


            "payments_enhanced": {
                "description": "Enhanced payments data with payment types",
                "sql": """
SELECT
    pl.id,
    pl.brand_id,
    pl.account_id,
    pl.user_id,
    pl.client_id,
    pl.payment_details_type,
    pl.status,
    pl.transaction_id,
    pl.invoice_id,
    pl.currency_id,
    pl.amount,
    pl.gateway_id,
    pl.transaction_type,
    pl.created_at,
    pl.currency_exchange_rate,
    pl.result,
    pt.name as payment_type_name
FROM {{ ref('raw_payments_log') }} pl
LEFT JOIN {{ ref('raw_payment_types') }} pt 
    ON pl.payment_details_type = pt.id
WHERE pl.brand_id = 1""",
                "tests": ["unique", "not_null"]
            }
        }

    def generate_model_file(self, model_name, model_info):
        """Generate individual model SQL file"""
        os.makedirs("models/staging", exist_ok=True)
        
        model_content = f"""{{{{ config(
    materialized='view',
    schema='analytics_staging'
) }}}}

{model_info['sql']}"""
        
        with open(f"models/staging/stg_{model_name}.sql", "w") as f:
            f.write(model_content)

    def generate_schema_file(self):
        """Generate schema.yml file for all models"""
        schema_content = """version: 2

models:"""
        
        for model_name, model_info in self.staging_models.items():
            schema_content += f"""
  - name: stg_{model_name}
    description: "{model_info['description']}"
    columns:
      - name: id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: created_at
        description: "Record creation timestamp"
      - name: updated_at
        description: "Record last update timestamp"
"""
            
            # Add additional tests based on model specifics
            if 'client_id' in model_info['sql']:
                schema_content += """      - name: client_id
        description: "Foreign key to clients"
        tests:
          - relationships:
              to: ref('raw_clients')
              field: id
"""
            
            if 'currency_id' in model_info['sql']:
                schema_content += """      - name: currency_id
        description: "Foreign key to currencies"
        tests:
          - relationships:
              to: ref('raw_currencies')
              field: id
"""
        
        with open("models/staging/schema.yml", "w") as f:
            f.write(schema_content)

    def generate_all(self):
        """Generate all staging models and schema"""
        print("Generating staging models...")
        for model_name, model_info in self.staging_models.items():
            self.generate_model_file(model_name, model_info)
            print(f"Generated stg_{model_name}.sql")
        
        print("\nGenerating schema.yml...")
        self.generate_schema_file()
        print("Generated schema.yml")
        
        print("\nGeneration complete!")

if __name__ == "__main__":
    generator = DbtStagingGenerator()
    generator.generate_all()