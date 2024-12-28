{{ config(
    schema='dbt_uautomation_staging_views',
    materialized='view'
) }}


SELECT
    hl.id,
    hl.hook_id,
    hl.object_client_id,
    hl.object_account_id,
    hl.object_reseller_account_id,
    hl.object_user_id,
    hl.object_brand_id,
    hl.object_id,
    hl.object_class,
    hl.object_type,
    hl.access_uid,
    hl.access_role,
    hl.access_user_type,
    hl.access_user_id,
    hl.access_ip,
    hl.access_connection_id,
    hl.created_at,
    hl.updated_at,
    hl.context_params,
    h.name as hook_name,
    h.code as hook_code,
    h.event as hook_event,
    h.internal as hook_internal,
    h.notifiable as hook_notifiable,
    h.webhookable as hook_webhookable
FROM {{ ref('raw_hook_logs') }} hl
LEFT JOIN {{ ref('raw_hooks') }} h 
    ON hl.hook_id = h.id