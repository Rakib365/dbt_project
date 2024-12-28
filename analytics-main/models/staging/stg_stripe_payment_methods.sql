WITH source AS (
    SELECT 
        pm.*,
        pmc.brand as card_brand,
        pmc.funding as card_funding
    FROM {{ source('paymentprovider_stripe', 'payment_method') }} pm
    LEFT JOIN {{ source('paymentprovider_stripe', 'payment_method_card') }} pmc 
        ON pm.id = pmc.payment_method_id
)

SELECT
    id as payment_method_id,
    customer_id,
    type,
    created as created_at,
    card_brand,
    card_funding,
    billing_detail_email,
    billing_detail_name,
    billing_detail_phone,
    billing_detail_address_country,
    billing_detail_address_city,
    billing_detail_address_line_1,
    billing_detail_address_postal_code,
    metadata
FROM source