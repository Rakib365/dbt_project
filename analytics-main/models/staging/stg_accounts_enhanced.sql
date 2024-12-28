{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}

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
    acc_status.id AS acc_status_id,
    acc_status.status,
    acc_types.id AS acc_type_id,
    acc_types.name AS account_type_name,
    acc_types.code AS account_type_code,
    acc_types.description AS account_type_description
FROM {{ ref('raw_accounts') }} accounts
LEFT JOIN {{ ref('raw_accounts_statuses') }} acc_status 
    ON accounts.status_id = acc_status.id
LEFT JOIN {{ ref('raw_account_types') }} acc_types 
    ON accounts.account_type_id = acc_types.id
