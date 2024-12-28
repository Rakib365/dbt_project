{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


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
WHERE brand_id = 1