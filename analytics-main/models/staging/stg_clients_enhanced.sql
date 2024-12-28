{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}

SELECT
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
WHERE c.brand_id = 1