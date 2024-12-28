WITH payment_data AS (
    SELECT * FROM {{ ref('stripe_payments_enhanced') }}
)

SELECT
    DATE(payment_date) as date,
    currency,
    -- Transaction Metrics
    COUNT(*) as total_transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(CASE WHEN is_paid THEN 1 ELSE 0 END) as successful_payments,
    SUM(CASE WHEN NOT is_paid THEN 1 ELSE 0 END) as failed_payments,
    
    -- Amount Metrics
    SUM(amount_in_currency) as total_amount,
    SUM(refunded_amount_in_currency) as total_refunded,
    AVG(amount_in_currency) as average_transaction_amount,
    
    -- Payment Method Metrics
    COUNT(DISTINCT payment_method_type) as payment_methods_used,
    
    -- Customer Geography
    customer_country,
    COUNT(DISTINCT customer_email) as unique_customers_by_email,
    
    -- Success Rates
    ROUND(100.0 * SUM(CASE WHEN is_paid THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate,
    
    -- Revenue After Refunds
    SUM(amount_in_currency - COALESCE(refunded_amount_in_currency, 0)) as net_revenue

FROM payment_data
GROUP BY 
    DATE(payment_date),
    currency,
    customer_country
ORDER BY 
    date DESC,
    currency,
    customer_country