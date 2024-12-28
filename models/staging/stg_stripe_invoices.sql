WITH source AS (
    SELECT * FROM {{ source('paymentprovider_stripe', 'invoice') }}
)
SELECT
    id as invoice_id,
    customer_id,
    charge_id,
    currency,
    status,
    total,
    subtotal,
    tax,
    amount_due,
    amount_paid,
    amount_remaining,
    created as created_at,
    due_date,
    paid,
    period_start,
    period_end
FROM source