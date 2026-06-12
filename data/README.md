cat > data/README.md << 'EOF'
# 데이터 출처 및 스키마

## raw/ecommerce_apparel_2019-10-01_sample.csv
- 출처: Kaggle "eCommerce Behavior Data from Multi Category Store" (2019-Oct.csv)
- src/ingest/split_ecommerce.py로 category_code가 'apparel'로 시작하는 행만
  필터링하여 날짜별로 분할한 파일 중, 2019-10-01 데이터의 상위 500행 샘플
- 컬럼: event_time, event_type, product_id, category_code, price,
  user_id, dt

> 전체 원본 데이터(약 195MB, 31일치)는 용량 문제로 .gitignore 처리하였으며,
> 위 샘플은 데이터 구조 확인용.
EOF



## raw/weather_sample.csv
- 출처: 기상청 ASOS 일자료 조회 서비스 (AsosDalyInfoService, 지점코드 108-서울)
- src/ingest/weather_ingestion.py 실행 결과, 2019-10-01 ~ 2019-10-31 전체 31일치
- 컬럼: date, avg_temp, rainfall
EOF


cd ~/fashion-pipeline
cat >> data/README.md << 'EOF'

## processed/fashion_weather_mart_sample.csv
- src/pipeline/spark_preprocess.py 실행 결과(Parquet, /user/maria_dev/processed_data/)에서
  상위 500행을 추출한 샘플
- 이커머스 행동 로그와 기상 데이터를 dt=date 기준 Inner Join한 최종 분석 테이블이며,
  hive_analysis.sql의 fashion_weather_mart 테이블과 동일한 스키마
- 컬럼: event_time, event_type, product_id, category_code, price, user_id,
  dt, avg_temp, rainfall
EOF