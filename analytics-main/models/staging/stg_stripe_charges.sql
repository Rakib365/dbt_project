WITH source AS (
    SELECT * FROM {{ source('paymentprovider_stripe', 'charge') }}
)

SELECT
    id as charge_id,
    amount,
    amount_refunded,
    currency,
    created as created_at,
    status,
    paid,
    customer_id,
    payment_intent_id,
    payment_method_id,  -- Make sure this field exists
    invoice_id,
    billing_detail_email,
    billing_detail_name,
    receipt_email,
    failure_code,
    failure_message,
    metadata
FROM source