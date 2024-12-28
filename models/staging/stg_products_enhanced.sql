{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
    ON p.category_id = pc.id