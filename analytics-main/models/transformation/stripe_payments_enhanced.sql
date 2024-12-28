WITH payments AS (
    SELECT * FROM {{ ref('stg_stripe_charges') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_stripe_customers') }}
),

invoices AS (
    SELECT * FROM {{ ref('stg_stripe_invoices') }}
),

payment_methods AS (
    SELECT * FROM {{ ref('stg_stripe_payment_methods') }}
)

SELECT
    -- Payment Information
    p.charge_id,
    p.amount / 100.0 as amount_in_currency,
    p.amount_refunded / 100.0 as refunded_amount_in_currency,
    p.currency,
    p.created_at as payment_date,
    p.status as payment_status,
    p.paid as is_paid,
    p.failure_code,
    p.failure_message,
    
    -- Customer Information
    c.customer_id,
    c.email as customer_email,
    c.name as customer_name,
    c.phone as customer_phone,
    c.address_country as customer_country,
    c.address_city as customer_city,
    
    -- Invoice Information
    i.invoice_id,
    i.total / 100.0 as invoice_total_in_currency,
    i.subtotal / 100.0 as invoice_subtotal_in_currency,
    i.tax / 100.0 as invoice_tax_in_currency,
    i.status as invoice_status,
    i.due_date,
    i.period_start,
    i.period_end,

    -- Payment Method Information
    pm.type as payment_method_type,
    pm.card_brand,
    pm.card_funding

FROM payments p
LEFT JOIN customers c 
    ON p.customer_id = c.customer_id
LEFT JOIN invoices i 
    ON p.invoice_id = i.invoice_id
LEFT JOIN payment_methods pm 
    ON p.payment_intent_id = pm.payment_method_id  -- Changed to use payment_intent_id if that's what's available