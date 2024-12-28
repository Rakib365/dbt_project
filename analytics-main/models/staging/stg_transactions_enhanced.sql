{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
WHERE i.brand_id = 1