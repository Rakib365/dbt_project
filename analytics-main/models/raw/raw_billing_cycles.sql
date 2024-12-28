{{ config(
    schema='dbt_uautomation_raw_tables',
    materialized='table'
) }}
select *
from {{ source("upmind_rds_tp_upmind", "billing_cycles") }}
