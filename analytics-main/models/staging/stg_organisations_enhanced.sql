{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
    ON o.id = s.org_id