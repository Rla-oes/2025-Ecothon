import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'  # Mac 사용자는 'AppleGothic', Windows는 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ----------------------------------
# 1. 데이터 불러오기
# ----------------------------------
carbon_data = pd.read_csv("Step4/carbon_emission_kr.csv")
gpt_data = pd.read_csv("Step3/synthetic_users_with_carbon_footprint.csv")

# ----------------------------------
# 2. GPT 사용자 수 (연도별)
# ----------------------------------
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

# ----------------------------------
# 3. 샘플 사용자 1인의 연간 평균 탄소배출량 계산 (일간 값 × 365)
# ----------------------------------
daily_mean_emission_per_user = gpt_data['total_carbon_emission'].mean()
annual_mean_emission_per_user = daily_mean_emission_per_user * 365
print(f"샘플 사용자 연간 평균 탄소배출량: {annual_mean_emission_per_user:.10f} tons")

# 연도별 GPT 총 배출량 계산
gpt_emissions_by_year = {
    year: users * annual_mean_emission_per_user for year, users in gpt_users_by_year.items()
}

# ----------------------------------
# 4. 기존 탄소배출량 선형회귀 예측
# ----------------------------------
X = carbon_data[['Year']]
y = carbon_data['total_carbon_emission']

model = LinearRegression()
model.fit(X, y)

# 2010년부터 2030년까지 예측
all_years = np.arange(2010, 2031).reshape(-1, 1)
predicted_emission = model.predict(all_years)

# ----------------------------------
# 5. GPT 추가 탄소배출량 반영
# ----------------------------------
adjusted_emission = predicted_emission.copy()
all_years_flat = all_years.flatten()

for i, year in enumerate(all_years_flat):
    if year in gpt_emissions_by_year:
        adjusted_emission[i] += gpt_emissions_by_year[year]

# ----------------------------------
# 6. 그래프 시각화 및 저장
# ----------------------------------
plt.figure(figsize=(12, 7))
plt.plot(all_years, predicted_emission, label='기존 예측 탄소배출량', color='blue', linewidth=2)
plt.plot(all_years, adjusted_emission, label='GPT 사용 포함 예측', color='red', linestyle='--', linewidth=2)
plt.scatter(carbon_data['Year'], carbon_data['total_carbon_emission'], color='black', label='실제 측정값', zorder=5)

plt.xlabel('연도', fontsize=13)
plt.ylabel('탄소배출량 (tons)', fontsize=13)
plt.title('GPT 사용에 따른 탄소배출량 증가 시뮬레이션 (2022~2030)', fontsize=15)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# PNG 파일 저장
plt.savefig("Step4/carbon_emission_simulation_2022_2030.png", dpi=300)

# ----------------------------------
# 7. 비율 분석 출력 및 파일 저장
# ----------------------------------

output_lines = []
output_lines.append("\n📊 GPT 추가 탄소배출량 영향 분석 (2023~2030)\n")

for year in range(2023, 2031):
    if year in gpt_emissions_by_year:
        idx = np.where(all_years_flat == year)[0][0]
        base = predicted_emission[idx]
        new = adjusted_emission[idx]
        increase = new - base
        percent_increase = (increase / base) * 100
        line = f"{year}년: 기존 {base:.2f} tons → GPT 추가 후 {new:.2f} tons (+{percent_increase:.6f}%)"
        print(line)
        output_lines.append(line)

# 텍스트 파일로 저장
with open("Step4/carbon_emission_gpt_analysis.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))