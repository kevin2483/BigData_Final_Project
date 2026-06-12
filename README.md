# 대용량 이커머스 행동 로그와 기상 공공데이터를 결합한 패션 수요 패턴 및 전환율 분석 파이프라인
(60211675 안정재)

## 1. 문제 정의 (Problem Definition)
현대 패션 이커머스 시장에서는 단순한 조회수를 넘어, 실제 구매로 이어지는 전환율을 최적화하는 것이 핵심 비즈니스 과제이다. 특히 의류 소비는 기상 변화(기온, 강수량 등)에 매우 민감하게 반응한다.
본 프로젝트는 대용량의 유저 행동 로그와 기상청 공공데이터를 결합하여, 날씨 변화에 따른 카테고리별 유저 수요 패턴을 파악하고 구매 전환율을 분석하는 빅데이터 처리 파이프라인을 직접 설계하고 구현하는 것을 목표로 한다.


## 2. 기술 스택 
본 프로젝트는 데이터 수집부터 최종 시각화까지의 과정을 파이프라인화하며, 강의에서 다룬 다중 분산 처리 프레임워크를 결합하여 구성한다.

**데이터 출처:**
  * 이커머스 행동 로그: Kaggle 공개 데이터셋 (대용량 CSV)
  * 기상 데이터: 기상청 Open API 호출
    
**데이터 수집 및 자동화:**
  * Python과 Linux Crontab을 활용하여 매일 HDFS로 데이터를 주기적으로 적재하는 파이프라인 구축
  
**데이터 저장:** HDFS

**데이터 처리 및 분석:**
  * Apache Spark: 성격이 다른 두 데이터(유저 로그 + 기상 데이터)를 날짜 기준으로 조인하고 결측치 처리 등 분산 전처리 연산 수행
  * Apache Hive: 전처리가 끝난 데이터를 테이블로 적재한 후, HiveQL를 이용해 데이터 집계 수행

**결과 시각화:** Python을 활용하여 분석 결과를 알아보기 쉽게 시각화


## 3. 구현 계획 
5주간의 프로젝트 일정을 다음과 같이 계획.

* 11주차: 프로젝트 주제 선정, GitHub repo 초기 구조 세팅 및 README 작성
* 12주차: 데이터 수집 스크립트 작성 및 HDFS/Spark 실습 환경(GCP Sandbox) 셋업 완료
* 13주차: Spark를 활용한 핵심 데이터 조인 및 전처리 파이프라인 로직 구현
* 14주차: HiveQL 분석 쿼리 수행 및 시각화 코드 작성, 보고서 초안 정리
* 15주차: 최종 분석 결과 요약, 2분 발표 슬라이드 제작 및 최종 산출물 제출

## AI Tool Usage
-gemini: 프로젝트 기술 스택 조합 브레인스토밍, 문장 교정


### -------------------------------------------------- ###


## 대용량 이커머스 행동 로그와 기상 공공데이터를 결합한 패션 수요 패턴 및 전환율 분석 파이프라인

**빅데이터 프로그래밍 최종 결과물 (60211675 / 안정재)**

본 프로젝트는 대규모 이커머스 유저 행동 로그(Kaggle)와 기상청 공공 데이터를 결합하여, 날씨 변화에 따른 패션 카테고리별 수요 패턴 및 구매 전환율(CVR)의 상관관계를 다중 분산 환경에서 분석한 End-to-End 빅데이터 파이프라인입니다.

---

## 1. 문제 정의 (Problem Definition)
현대 패션 이커머스 시장에서는 단순 조회수를 넘어, 실제 구매로 이어지는 전환율을 최적화하는 것이 핵심 과제이다. 특히 의류 소비는 기상 변화(기온, 강수량 등)에 민감하다는 가설을 바탕으로, 데이터를 통해 실제 상관관계를 분석하고 비즈니스 인사이트를 도출하고자 한다.

## 2. 시스템 아키텍처 및 기술 스택
본 시스템은 데이터 수집부터 분석까지 분산 처리 프레임워크를 활용하여 자동화된 파이프라인으로 구성되었다.

- **인프라**: GCP Compute Engine (CentOS 7) + HDP Sandbox v2.6.5
- **수집/자동화**: Python (Kaggle API, Open API), Linux Crontab, Bash
- **저장**: HDFS (Hadoop Distributed File System)
- **처리/분석**: Apache Spark (PySpark), Apache Hive (HiveQL)



---

## 3. 하둡 파이프라인 구동 가이드

### Step 0: 환경 설정
GCP 인스턴스에 접속하여 HDP 샌드박스 환경을 준비합니다.

```bash
# GCP 인스턴스 SSH 접속
ssh -i ~/.ssh/gcp_key jeongjae2483@<GCP_EXTERNAL_IP>

# HDP Sandbox maria_dev 계정 진입
ssh maria_dev@localhost -p 2222



### Step1: 데이터수집 및 자동화
# Kaggle 대용량 데이터를 청크 단위로 스트리밍 처리하고 기상청 API와 결합하여 HDFS에 적재한다.

# 매일 새벽 2시 자동 적재 스케줄러 등록
crontab -e

# [등록 명령어]
0 2 * * * /bin/bash /home/maria_dev/fashion-pipeline/src/ingest/daily_ingestion.sh >> /home/maria_dev/fashion-pipeline/src/ingest/ingestion.log 2>&1

# 수동 테스트 실행
python3 src/ingest/weather_ingestion.py



### Step 2: Spark 분산 데이터 전처리 (Processing)
이기종 데이터를 날짜(dt) 기준으로 조인하고, Parquet 및 Snappy 압축을 적용하여 저장 효율을 최적화합니다.

# PySpark 전처리 스크립트 실행
spark-submit --master local[*] src/pipeline/spark_preprocess.py


### Step 3: Hive 분석 마트 구축 및 분석 (Analysis)
Ranger 보안 제약을 우회하여 HDFS 데이터를 연결하고 최종 분석을 수행합니다.

# HDFS 권한 개방
hdfs dfs -chmod -R 777 /user/maria_dev/processed_data/

# Beeline을 통한 분석 쿼리 수행
beeline -u jdbc:hive2://localhost:10000 -n hive -f src/analyze/hive_analysis.sql


## 분석 결과 및 인사이트
# 악천후 유인 효과
비 오는 날 shoes 카테고리 트래픽이 급증하여 악천후 시 특수 수요가 발생함을 확인.

# 트래픽 vs 전환율
날씨에 따라 트래픽은 3배까지 변동하나, 구매 전환율(CVR)은 0.5%로 일정하게 유지됨.

# 매출 결정타
날씨보다 프로모션 기간(10월 18일~24일)에 매출이 폭증함을 확인, 날씨는 유인 요인일 뿐 실질적인 구매 동인은 플랫폼 프로모션임을 검증.
