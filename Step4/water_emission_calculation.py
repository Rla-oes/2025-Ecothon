import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.rcParams['font.family'] = 'Malgun Gothic'  # Mac 사용자는 'AppleGothic', Windows는 'Malgun Gothic'

# === 설정 ===
GPT_USER_SCALING_FACTOR = 0.1  # GPT 사용자 수의 10%만 실제 냉각수 사용한다고 가정
COOLING_UNIT_CONVERSION = 1_000_000  # mL → m³

# === 데이터 로드 ===
water_data = pd.read_csv("Data/Data - water_usage.csv")
user_data = pd.read_csv("Step3/synthetic_users_with_carbon_footprint.csv")

# === 연도별 GPT 사용자 수 ===
gpt_users_by_year = {
    2022: 0,
    2023: 720000,
    2024: 3500000,
    2025: 12000000,
    2026: 14000000,
    2027: 16000000,
    2028: 18000000,
    2029: 20000000,
    2030: 22000000
}

# === 1인당 연간 냉각수 사용량 계산 (m³ 기준) ===
daily_ml = user_data["total_cooling_consumed"].mean()
annual_m3 = (daily_ml / COOLING_UNIT_CONVERSION) * 365

# === GPT 사용량 반영 ===
adjusted_gpt_emissions = {
    year: users * GPT_USER_SCALING_FACTOR * annual_m3
    for year, users in gpt_users_by_year.items()
}

# === 기존 예측 (선형회귀) ===
X = water_data[["year"]]
y = water_data["water_consumption"]
model = LinearRegression()
model.fit(X, y)

future_years = np.arange(2010, 2031).reshape(-1, 1)
predicted = model.predict(future_years)
adjusted = predicted.copy()
future_years_flat = future_years.flatten()

# GPT 사용 반영
for i, year in enumerate(future_years_flat):
    if year in adjusted_gpt_emissions:
        adjusted[i] += adjusted_gpt_emissions[year]

# === 시각화 ===
plt.figure(figsize=(12, 7))
plt.plot(future_years, predicted, label="기존 예측", color="blue")
plt.plot(future_years, adjusted, label="GPT 사용 포함 예측", color="red", linestyle="--")
plt.scatter(water_data["year"], water_data["water_consumption"], color="black", label="실측값")
plt.xlabel("year")
plt.ylabel("water consumption (m³)")
plt.title("Water Usage Forecast with GPT Scenario (2022–2030)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()

# 그래프 저장
plt.savefig("water_consumption_simulation_gpt.png", dpi=300)
plt.show()
# 수치 저장 (GPT 영향 요약)
with open("gpt_water_impact_summary.txt", "w", encoding="utf-8") as f:
    for year in range(2023, 2031):
        if year in adjusted_gpt_emissions:
            idx = np.where(future_years_flat == year)[0][0]
            base = predicted[idx]
            new = adjusted[idx]
            diff = new - base
            rate = (diff / base) * 100
            f.write(f"{year}년: 기존 {base:,.2f} → GPT 추가 후 {new:,.2f} (+{rate:.4f}%)\n")
