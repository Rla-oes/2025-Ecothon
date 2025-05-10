import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 1. Step 1에서 생성된 CSV 파일 경로 수정
df = pd.read_csv("../Step1/kmeans_classified_users.csv") 

# 2. 자원 소비량 추정에 사용할 변수 선택 (프롬프트 수 예측을 위한 변수들)
features = ['ai_use_rate', 'avg_use_time_min', 'leisure_score', 'utility_score']

# 3. 데이터 정규화 (StandardScaler 사용)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# 4. 하루 예상 프롬프트 수 예측
# (가정 예시: 평균 1.5분에 1프롬프트를 사용한다고 가정)
df['daily_prompt_count'] = df['avg_use_time_min'] / 1.5

# 5. 자원 소비량 계산 (프롬프트 수 * 자원 소모량)
# 예시 값: 1프롬프트당 전력, 냉각수
power_per_prompt = 0.005  # kWh
cooling_per_prompt = 500  # mL

# 자원 소비량 계산
df['total_power_consumed'] = df['daily_prompt_count'] * power_per_prompt  # kWh
df['total_cooling_consumed'] = df['daily_prompt_count'] * cooling_per_prompt  # mL

# 6. 결과 저장 (Step 2 폴더 안에 저장)
df.to_csv("../Step2/synthetic_users_with_resource_consumption.csv", index=False)

# 7. 확인 메시지 출력
print("자원 소비량 계산 완료! 👉 'synthetic_users_with_resource_consumption.csv' 저장됨")
