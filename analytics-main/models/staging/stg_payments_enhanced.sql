{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
WHERE pl.brand_id = 1