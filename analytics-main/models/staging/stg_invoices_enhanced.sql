{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
WHERE i.brand_id = 1