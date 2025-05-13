import pandas as pd

# Step 2에서 생성된 CSV 파일 경로
df = pd.read_csv("Step2/synthetic_users_with_resource_consumption.csv")

# 1kWh당 CO₂ 배출량 (발전단 기준)
carbon_emission_per_kWh = 0.424  # CO₂ 배출 계수 (발전단)

# 전력 소비량을 바탕으로 탄소 배출량 계산
df['total_carbon_emission'] = df['total_power_consumed'] * carbon_emission_per_kWh / 1000  # t CO₂

# 결과 저장
df.to_csv("Step3/synthetic_users_with_carbon_footprint.csv", index=False)