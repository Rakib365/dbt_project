{{ config(
    schema='dbt_uautomation_raw_tables',
    materialized='table'
) }}


SELECT *
FROM {{ source('upmind_rds_tp_upmind', 'account_types') }}