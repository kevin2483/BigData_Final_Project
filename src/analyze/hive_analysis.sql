--Parquet SerDe 설정--
SET hive.execution.engine=tez;

--테이블 생성--
CREATE EXTERNAL TABLE IF NOT EXISTS fashion_weather_mart (
    event_time STRING,
    event_type STRING,
    product_id STRING,
    category_code STRING,
    price FLOAT,
    user_id STRING,
    dt STRING,
    avg_temp FLOAT,
    rainfall FLOAT
)
STORED AS PARQUET
LOCATION '/user/maria_dev/processed_data/';


--1.비 오는 날의 패션 구매 패턴 (강수량 > 0 인 날의 카테고리별 구매 Top 10)--
SELECT category_code, COUNT(*) as purchase_count
FROM fashion_weather_mart
WHERE rainfall > 0.0 AND event_type = 'purchase'
GROUP BY category_code
ORDER BY purchase_count DESC
LIMIT 10;


--2.날씨에 따른 가격 민감도 분석--
SELECT 
    CASE 
        WHEN avg_temp < 10 THEN '1_Cold (<10C)'
        WHEN avg_temp >= 10 AND avg_temp < 20 THEN '2_Mild (10-20C)'
        ELSE '3_Warm (>=20C)' 
    END as temp_range,
    AVG(price) as avg_price,
    COUNT(*) as total_purchases
FROM fashion_weather_mart
WHERE event_type = 'purchase'
GROUP BY 
    CASE 
        WHEN avg_temp < 10 THEN '1_Cold (<10C)'
        WHEN avg_temp >= 10 AND avg_temp < 20 THEN '2_Mild (10-20C)'
        ELSE '3_Warm (>=20C)' 
    END
ORDER BY temp_range;


--3.10월 일별 총 매출 및 판매량 추이--
SELECT dt, COUNT(*) as daily_sales_count, SUM(price) as daily_revenue
FROM fashion_weather_mart
WHERE event_type = 'purchase'
GROUP BY dt
ORDER BY dt;


--4.기온 구간별 조회 대비 구매 전환율 분석
SELECT 
    CASE 
        WHEN avg_temp < 10 THEN '1_Cold (<10C)'
        WHEN avg_temp >= 10 AND avg_temp < 20 THEN '2_Mild (10-20C)'
        ELSE '3_Warm (>=20C)' 
    END as temp_range,
    SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) as view_cnt,
    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) as purchase_cnt,
    ROUND((SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) / SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END)) * 100, 2) as conversion_rate_pct
FROM fashion_weather_mart
GROUP BY 
    CASE 
        WHEN avg_temp < 10 THEN '1_Cold (<10C)'
        WHEN avg_temp >= 10 AND avg_temp < 20 THEN '2_Mild (10-20C)'
        ELSE '3_Warm (>=20C)' 
    END
ORDER BY temp_range;