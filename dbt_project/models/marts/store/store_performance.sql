{{
    config(
        materialized='table',
        tags=['business', 'daily', 'diagnostics'],
        schema='marts'
    )
}}

-- Core business logic: Identify underperforming stores and probable causes
-- Demonstrates SQL skill without over-engineering

WITH daily_store_metrics AS (
    SELECT
        ds.store_id,
        ds.store_name,
        ds.region,
        dd.date,
        dd.day_of_week,
        dd.is_weekend,
        fs.total_sales,
        fs.transaction_count,
        
        -- Calculate expected sales based on history
        AVG(fs.total_sales) OVER (
            PARTITION BY ds.store_id, dd.day_of_week
            ORDER BY dd.date
            ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING
        ) AS avg_28day_same_day_sales,
        
        -- Promotions
        COALESCE(promo.discount_pct, 0) AS active_promotion_discount,
        CASE WHEN promo.promotion_id IS NOT NULL THEN 1 ELSE 0 END AS has_promotion,
        
        -- Inventory issues (store-level flags)
        MAX(CASE WHEN inv.stockout_flag = TRUE THEN 1 ELSE 0 END) AS has_stockout,
        MAX(CASE WHEN inv.low_stock_flag = TRUE THEN 1 ELSE 0 END) AS has_low_stock
        
    FROM {{ ref('dim_store') }} ds
    CROSS JOIN {{ ref('dim_date') }} dd
    LEFT JOIN {{ ref('fact_daily_sales') }} fs 
        ON ds.store_id = fs.store_id 
        AND dd.date = fs.date
    LEFT JOIN {{ ref('stg_promotions') }} promo
        ON ds.store_id = promo.store_id
        AND dd.date BETWEEN promo.start_date AND promo.end_date
    LEFT JOIN {{ ref('stg_inventory') }} inv
        ON ds.store_id = inv.store_id
        AND dd.date = inv.date
    WHERE dd.date >= DATEADD('day', -90, CURRENT_DATE)
    GROUP BY 1,2,3,4,5,6,7,8,9,10
),

performance_calculation AS (
    SELECT
        *,
        
        -- Performance against expectation
        CASE 
            WHEN avg_28day_same_day_sales > 0 
            THEN (total_sales / avg_28day_same_day_sales) - 1
            ELSE NULL 
        END AS performance_vs_expectation,
        
        -- Define underperformance threshold (20% below expectation)
        CASE 
            WHEN total_sales < avg_28day_same_day_sales * 0.8 
            THEN TRUE 
            ELSE FALSE 
        END AS is_underperforming,
        
        -- Calculate impact (how much below expectation)
        CASE 
            WHEN avg_28day_same_day_sales > 0 
            THEN avg_28day_same_day_sales - total_sales
            ELSE 0 
        END AS performance_gap_dollars
        
    FROM daily_store_metrics
    WHERE total_sales IS NOT NULL
),

probable_causes AS (
    SELECT
        *,
        
        -- Rank probable causes based on available evidence (business heuristics)
        CASE 
            WHEN has_stockout = 1 THEN 'stockout'
            WHEN has_promotion = 0 AND (
                SELECT COUNT(*) 
                FROM {{ ref('stg_promotions') }} p2 
                WHERE p2.store_id = store_id 
                AND date BETWEEN DATEADD('day', -14, CURRENT_DATE) AND CURRENT_DATE
            ) > 0 THEN 'promotion_missing'
            WHEN has_low_stock = 1 THEN 'low_inventory'
            WHEN performance_vs_expectation < -0.3 THEN 'significant_drop'
            WHEN is_weekend = TRUE AND total_sales < avg_28day_same_day_sales * 0.7 
                THEN 'weekend_underperformance'
            ELSE 'investigation_needed'
        END AS probable_cause,
        
        -- Confidence score (simple business logic)
        CASE 
            WHEN has_stockout = 1 THEN 0.9
            WHEN has_promotion = 0 AND (
                SELECT COUNT(*) 
                FROM {{ ref('stg_promotions') }} p2 
                WHERE p2.store_id = store_id 
                AND date BETWEEN DATEADD('day', -14, CURRENT_DATE) AND CURRENT_DATE
            ) > 0 THEN 0.8
            WHEN has_low_stock = 1 THEN 0.7
            ELSE 0.5
        END AS confidence_score
        
    FROM performance_calculation
    WHERE is_underperforming = TRUE
)

SELECT
    date,
    store_id,
    store_name,
    region,
    total_sales,
    avg_28day_same_day_sales AS expected_sales,
    ROUND(performance_vs_expectation, 3) AS performance_vs_expectation,
    ROUND(performance_gap_dollars, 2) AS performance_gap_dollars,
    probable_cause,
    confidence_score,
    has_stockout,
    has_low_stock,
    has_promotion,
    day_of_week,
    is_weekend,
    
    -- For dashboard filtering
    CASE 
        WHEN performance_gap_dollars > 1000 THEN 'high_impact'
        WHEN performance_gap_dollars > 500 THEN 'medium_impact'
        ELSE 'low_impact'
    END AS impact_category,
    
    -- Quick action recommendation
    CASE probable_cause
        WHEN 'stockout' THEN 'Check inventory and expedite restock'
        WHEN 'promotion_missing' THEN 'Verify promotion execution'
        WHEN 'low_inventory' THEN 'Review reorder points'
        WHEN 'weekend_underperformance' THEN 'Check staffing and hours'
        ELSE 'Requires manager investigation'
    END AS recommended_action
    
FROM probable_causes
WHERE date = CURRENT_DATE - 1  -- Yesterday's performance
ORDER BY performance_gap_dollars DESC