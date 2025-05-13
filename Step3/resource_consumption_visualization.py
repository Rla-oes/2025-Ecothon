import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter, MaxNLocator
from matplotlib import rc

# 한글 폰트 설정
rc('font', family='AppleGothic')  

# 그래프 출력할 때, 한글 글자가 깨지지 않게 설정
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df = pd.read_csv("Step3/synthetic_users_with_carbon_footprint.csv")

# 사용자 유형별 평균 탄소 배출량, 냉각수 사용량 계산
grouped = df.groupby('classified_type')[['total_carbon_emission', 'total_cooling_consumed']].mean().sort_index()

# 인덱스 및 값 준비
labels = grouped.index.tolist()
carbon_values = grouped['total_carbon_emission'].values
cooling_values = grouped['total_cooling_consumed'].values
x = np.arange(len(labels))

# 그래프 생성
fig, ax1 = plt.subplots(figsize=(10, 6))

# 첫 번째 Y축: 탄소 배출량 (막대그래프)
bars = ax1.bar(x, carbon_values, color='tab:red', alpha=0.7, label='탄소 배출량 (kg CO₂)')

# 축 설정
ax1.set_xlabel("User Type")
ax1.set_ylabel("탄소 배출량 (kg CO₂)", color='tab:red')
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15)
ax1.tick_params(axis='y', labelcolor='tab:red')

# 두 번째 Y축 (냉각수 사용량)
ax2 = ax1.twinx()  
ax2.plot(x, cooling_values, color='tab:blue', marker='o', label='냉각수 사용량 (mL)')
ax2.set_ylabel("냉각수 사용량 (mL)", color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

ax1.yaxis.set_major_locator(MaxNLocator(integer=True))  
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))  


plt.title("군집별 탄소 배출량과 냉각수 사용량 비교")
plt.tight_layout() 
plt.savefig("Step3/resource_comparison_carbon_and_cooling.png", dpi=300)  