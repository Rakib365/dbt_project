WITH payment_data AS (
    SELECT * FROM {{ ref('stripe_payments_enhanced') }}
)

SELECT
    -- Time Dimensions
    DATE_TRUNC(DATE(payment_date), MONTH) as month,
    currency,
    customer_country,
    
    -- Transaction Metrics
    COUNT(*) as total_transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(DISTINCT DATE(payment_date)) as active_days,
    
    -- Amount Metrics
    SUM(amount_in_currency) as total_amount,
    SUM(refunded_amount_in_currency) as total_refunded,
    SUM(amount_in_currency - COALESCE(refunded_amount_in_currency, 0)) as net_revenue,
    AVG(amount_in_currency) as average_transaction_amount,
    
    -- Payment Success Metrics
    SUM(CASE WHEN is_paid THEN 1 ELSE 0 END) as successful_payments,
    SUM(CASE WHEN NOT is_paid THEN 1 ELSE 0 END) as failed_payments,
    ROUND(100.0 * SUM(CASE WHEN is_paid THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as success_rate,
    
    -- Payment Method Analysis
    COUNT(DISTINCT payment_method_type) as payment_methods_used,
    
    -- Customer Metrics
    COUNT(DISTINCT customer_email) as unique_customers_by_email,
    
    -- Calculated Business Metrics
    CASE 
        WHEN COUNT(DISTINCT customer_id) = 0 THEN NULL 
        ELSE SUM(amount_in_currency) / NULLIF(COUNT(DISTINCT customer_id), 0) 
    END as average_revenue_per_customer,
    
    CASE 
        WHEN COUNT(DISTINCT DATE(payment_date)) = 0 THEN NULL 
        ELSE SUM(amount_in_currency) / NULLIF(COUNT(DISTINCT DATE(payment_date)), 0) 
    END as average_daily_revenue

FROM payment_data
GROUP BY 
    DATE_TRUNC(DATE(payment_date), MONTH),
    currency,
    customer_country
ORDER BY 
    month DESC,
    currency,
    customer_country