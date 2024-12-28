{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


SELECT
    s.id,
    s.org_id,
    s.brand_id,
    s.code,
    s.value,
    s.date,
    s.created_at,
    s.updated_at,
    s.deleted_at,
    o.name as org_name,
    o.verified as org_verified,
    o.completed as org_completed
FROM {{ ref('raw_organisation_stats') }} s
LEFT JOIN {{ ref('raw_organisations') }} o 
    ON s.org_id = o.id