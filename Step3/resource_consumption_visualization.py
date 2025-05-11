import pandas as pd 
import matplotlib.pyplot as plt

# 1. 데이터 불러오기
df = pd.read_csv("Step3/synthetic_users_with_carbon_and_water_footprint.csv")

# 2. 사용자 유형별 평균 탄소/물 소비량 계산
grouped = df.groupby('classified_type')[['total_carbon_emission', 'total_water_footprint']].mean()

# 3. 순서 정렬 (선택)
grouped = grouped.sort_index()

# ================================================
# 첫 번째 그래프: Dual Axis (bar + line)
# ================================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

# 첫 번째 Y축: Carbon Emission (bar)
ax1.bar(grouped.index, grouped['total_carbon_emission'],
        color='tab:red', alpha=0.6, label='Carbon Emission (kg CO₂)')
ax1.set_xlabel("User Type")
ax1.set_ylabel("Carbon Emission (kg CO₂)", color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

# 두 번째 Y축: Water Footprint (line)
ax2 = ax1.twinx()
ax2.plot(grouped.index, grouped['total_water_footprint'],
         color='tab:blue', marker='o', linewidth=2, label='Water Footprint (L)')
ax2.set_ylabel("Water Footprint (L)", color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

# 제목 및 저장
plt.title("Carbon and Water Footprint per User Type (Dual Axis)")
fig1.tight_layout()
plt.savefig("Step3/user_type_resource_dual_axis.png", dpi=300)
plt.close()

# ================================================
# 두 번째 그래프: Multi Bar Chart
# ================================================
fig2, ax3 = plt.subplots(figsize=(10, 6))

grouped.plot(kind='bar', ax=ax3, color=['tab:red', 'tab:blue'], alpha=0.7)
plt.title("Carbon and Water Footprint per User Type")
plt.xlabel("User Type")
plt.ylabel("Resource Usage")
plt.xticks(rotation=15)
plt.legend(["Carbon Emission (kg CO₂)", "Water Footprint (L)"])

plt.tight_layout()
plt.savefig("Step3/user_type_resource_bar_chart.png", dpi=300)
plt.close()

print("✅ 사용자 유형 기준 그래프 2종 저장 완료 (Step3)")
