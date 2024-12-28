{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


SELECT
    id,
    bounced,
    created_at,
    updated_at,
    bounced_at,
    interface_language_id,
    document_language_id,
    enabled_2fa,
    provider_2fa_id,
    org_id,
    verified,
    admin,
    active,
    last_login,
    failed_login_attempts,
    notifications_disabled,
    api_user,
    deleted_at
FROM {{ ref('raw_users') }}