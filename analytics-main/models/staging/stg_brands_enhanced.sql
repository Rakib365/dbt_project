{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
    ON brands.language_id = bl.id