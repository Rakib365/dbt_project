WITH source AS (
    SELECT * FROM {{ source('paymentprovider_stripe', 'customer') }}
)
SELECT
    id as customer_id,
    email,
    name,
    created as created_at,
    currency,
    delinquent,
    description,
    phone,
    address_city,
    address_country,
    address_line_1,
    address_line_2,
    address_postal_code,
    address_state,
    metadata
FROM source