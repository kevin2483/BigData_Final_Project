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