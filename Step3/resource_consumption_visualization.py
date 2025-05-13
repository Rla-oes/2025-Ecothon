import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 데이터 불러오기
df = pd.read_csv("Step3/synthetic_users_with_carbon_footprint.csv")

# 사용자 유형별 평균 탄소 배출량 계산
grouped = df.groupby('classified_type')['total_carbon_emission'].mean().sort_index()

# 인덱스 및 값 준비
labels = grouped.index.tolist()
values = grouped.values
x = np.arange(len(labels))

# 그래프 생성
fig, ax = plt.subplots(figsize=(10, 10))
bars = ax.bar(x, values, color='tab:red', alpha=0.7)

# 축 설정
#사용자 유형 1명이 하루에 발생시키는 평균 탄소 배출량 (kg CO₂) = y축
ax.set_title("Carbon Emission per User Type")
ax.set_xlabel("User Type")
ax.set_ylabel("Carbon Emission (kg CO₂)")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=15)

ax.ticklabel_format(style='plain', axis='y')

#막대 위에 수치 표시 (소수점 6자리까지)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2,
            height + height * 0.01,
            f"{height:.6f}", ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig("Step3/user_type_carbon_only_bar_chart_labeled_fixed.png", dpi=300)
plt.close()