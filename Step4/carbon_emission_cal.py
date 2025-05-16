import pandas as pd

# 1. 전력소모량 데이터 불러오기
power_data = pd.read_csv("Data/Data - power_usage.csv")

# 2. CO2 배출 계수 (톤/kWh) - 발전단 기준 (국내 기준으로 사용)
carbon_emission_per_kWh = 0.424 / 1000  # 0.424 kgCO2/kWh → 0.000424 tCO2/kWh

power_consumption_col = 'power_usage' 

# 4. 탄소 배출량 계산 (단위: 톤)
power_data['total_carbon_emission'] = power_data[power_consumption_col] * carbon_emission_per_kWh

# 5. 결과 확인
print(power_data[['Year', 'total_carbon_emission']].head())

# 6. 결과 CSV 저장
power_data.to_csv("Step4/carbon_emission_kr.csv", index=False)