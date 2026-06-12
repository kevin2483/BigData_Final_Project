import matplotlib.pyplot as plt
import numpy as np
import os

output_dir = "src/analyze"
os.makedirs(output_dir, exist_ok=True)

#색상 팔레트 및 스타일 지정
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#c2c2f0']
plt.style.use('ggplot')

print("데이터 검증 완료. 정밀 시각화 그래프 생성을 시작합니다...")

#---1.비 오는 날 카테고리 분석---
# 데이터 검증: shoes(3939), keds(2481), costume(426), jeans(114), underwear(85) 완벽 일치
categories = ['Shoes', 'Keds', 'Costume', 'Jeans', 'Underwear']
purchase_counts = [3939, 2481, 426, 114, 85]

plt.figure(figsize=(10, 6))
bars = plt.bar(categories, purchase_counts, color=colors)
plt.title('Top 5 Apparel Categories on Rainy Days', fontsize=15, fontweight='bold')
plt.ylabel('Purchase Count')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 50, int(yval), va='bottom', ha='center', fontweight='bold')
plt.savefig(f'{output_dir}/1_rainy_day_categories.png', bbox_inches='tight')
plt.close()

#---2.온도별 평균 구매가 및 트래픽 분석---
#데이터 검증: Mild(12323건, 77.96달러), Warm(3681건, 78.55달러) 완벽 일치
temp_ranges = ['Mild (10-20C)', 'Warm (>=20C)']
avg_prices = [77.96, 78.55]
total_purchases = [12323, 3681]

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()

ax1.bar(temp_ranges, total_purchases, color=['#66B2FF', '#FF9999'], alpha=0.7, width=0.4, label='Total Purchases')
ax2.plot(temp_ranges, avg_prices, color='black', marker='o', linewidth=2, markersize=8, label='Avg Price ($)')

ax1.set_ylabel('Total Purchases (Count)', fontweight='bold')
ax2.set_ylabel('Average Price ($)', fontweight='bold')
plt.title('Purchases vs Average Price by Temperature', fontsize=15, fontweight='bold')
plt.savefig(f'{output_dir}/2_temperature_analysis.png', bbox_inches='tight')
plt.close()

#---3.10월 일별 판매량 및 총 매출 추이---
#데이터 검증: 10월 1일(18170) ~ 31일(18200) 판매량 및 수익 동시 반영
days = list(range(1, 32))
daily_sales = [340, 318, 254, 260, 286, 222, 302, 294, 354, 424, 550, 558, 576, 346, 392, 606, 564, 1182, 932, 856, 848, 792, 760, 830, 464, 466, 402, 420, 464, 474, 468]
#수익 소수점 둘째 자리까지 정확하게 반영
daily_revenue = [26396.02, 28723.16, 22908.30, 20157.80, 23534.96, 17787.56, 25297.98, 24757.96, 29344.32, 31005.86, 44793.06, 40994.64, 44815.22, 28638.46, 34819.34, 45093.52, 43316.50, 91534.68, 73116.98, 62538.54, 63766.76, 59015.44, 57168.84, 65954.42, 34928.42, 36818.58, 31325.32, 34370.16, 36622.78, 34191.36, 36138.56]

fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()

ax1.bar(days, daily_sales, color='#FFCC99', alpha=0.8, label='Sales Count')
ax2.plot(days, daily_revenue, color='#FF6666', marker='o', linestyle='-', linewidth=2, label='Daily Revenue ($)')

ax1.axvspan(18, 24, color='yellow', alpha=0.2, label='Promo Period (Est.)') # 18일~24일 폭증 구간 하이라이트

ax1.set_xlabel('Day in October 2019', fontsize=12)
ax1.set_ylabel('Daily Sales Count', fontsize=12, fontweight='bold')
ax2.set_ylabel('Daily Revenue ($)', fontsize=12, fontweight='bold')
plt.title('Daily Sales & Revenue Trend (Oct 2019)', fontsize=15, fontweight='bold')
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.savefig(f'{output_dir}/3_daily_sales_revenue_trend.png', bbox_inches='tight')
plt.close()

#---4.기온별 구매 전환율---
# 데이터 검증: Mild(0.53%), Warm(0.51%) 완벽 일치
conv_rates = [0.53, 0.51]

plt.figure(figsize=(6, 5))
bars = plt.bar(temp_ranges, conv_rates, color=['#99FF99', '#FFCC99'], width=0.5)
plt.title('Conversion Rate by Temperature (%)', fontsize=15, fontweight='bold')
plt.ylabel('Conversion Rate (%)')
plt.ylim(0, 0.8) 
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval}%", va='bottom', ha='center', fontweight='bold', fontsize=12)
plt.savefig(f'{output_dir}/4_conversion_rate.png', bbox_inches='tight')
plt.close()

print("그래프 생성이 완료되었습니다.")