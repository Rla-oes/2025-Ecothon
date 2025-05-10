import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Step3/synthetic_users_with_carbon_and_water_footprint.csv")  

# 2. 군집별로 자원 소비량(탄소 배출량, 물 소모 발자국) 평균 구하기
grouped = df.groupby('cluster')[['total_carbon_emission', 'total_water_footprint']].mean()

# ================================================
# 첫 번째 그래프: 두 Y축을 사용한 그래프 (탄소 배출량과 물 소모 발자국)
# ================================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

# 탄소 배출량 (첫 번째 Y축)
ax1.bar(grouped.index, grouped['total_carbon_emission'], color='tab:red', alpha=0.6, label='탄소 배출량 (kg CO₂)')
ax1.set_xlabel("Cluster")
ax1.set_ylabel("탄소 배출량 (kg CO₂)", color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

# 두 번째 Y축 (물 소모 발자국)
ax2 = ax1.twinx()  # 두 번째 Y축
ax2.plot(grouped.index, grouped['total_water_footprint'], color='tab:blue', marker='o', label='물 소모 발자국 (L)')
ax2.set_ylabel("물 소모 발자국 (L)", color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

# 그래프 제목
plt.title("군집별 탄소 배출량과 물 소모 발자국 비교")
fig1.tight_layout()  # 레이아웃 조정
plt.show()  # 첫 번째 그래프 표시

# ================================================
# 두 번째 그래프: 다중 막대 그래프 (탄소 배출량과 물 소모 발자국)
# ================================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

# 다중 막대 그래프
grouped.plot(kind='bar', figsize=(10, 6), color=['tab:red', 'tab:blue'], ax=ax2, alpha=0.7)

# 그래프 제목
plt.title("군집별 탄소 배출량과 물 소모 발자국 비교")
plt.xlabel("Cluster")
plt.ylabel("Consumption")
plt.xticks(rotation=0)

plt.show()  # 두 번째 그래프 표시