import pandas as pd
import os

#원본 데이터 경로 설정
input_file = "/kaggle/input/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store/2019-Oct.csv"
output_dir = "/kaggle/working/daily_apparel"
os.makedirs(output_dir, exist_ok=True)

print("=== 시작: 의류(Apparel) 카테고리 일별 분할 추출 ===")

#대용량 처리를 위한 청크 설정
chunk_size = 1000000 
chunk_count = 0

for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    chunk_count += 1
    
    #의류 데이터만 필터링
    apparel_data = chunk[chunk['category_code'].str.startswith('apparel', na=False)].copy()
    
    if not apparel_data.empty:
        #이벤트 시간에서 날짜만 추출
        apparel_data['date'] = apparel_data['event_time'].str[:10]
        
        #날짜별로 그룹화하여 각각의 CSV로 누적 저장
        for date, group in apparel_data.groupby('date'):
            output_file = f"{output_dir}/ecommerce_apparel_{date}.csv"
            
            #파일이 이미 있으면 내용만 추가, 없으면 헤더 포함 새로 생성
            if os.path.exists(output_file):
                group.drop(columns=['date']).to_csv(output_file, mode='a', index=False, header=False)
            else:
                group.drop(columns=['date']).to_csv(output_file, mode='w', index=False, header=True)
                
    if chunk_count % 5 == 0:
        print(f"{chunk_count * chunk_size}행 처리 완료...")

print("=== 완료: 일별 분할 저장 성공 ===")