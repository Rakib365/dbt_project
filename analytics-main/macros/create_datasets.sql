{% macro create_datasets() %}
  {% set datasets = [
    'dbt_uautomation',
    'dbt_uautomation_raw',
    'dbt_uautomation_staging',
    'dbt_uautomation_transformation',
    'dbt_uautomation_reporting'
  ] %}

  {% for dataset in datasets %}
    {% set create_dataset_query %}
      CREATE SCHEMA IF NOT EXISTS `{{ target.project }}.{{ dataset }}`
    {% endset %}
    {% do run_query(create_dataset_query) %}
  {% endfor %}
{% endmacro %}
