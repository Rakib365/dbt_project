{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
WHERE c.brand_id = 1