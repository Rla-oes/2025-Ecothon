import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. 데이터 불러오기
df = pd.read_csv("Data/synthetic_users_allAIusers.csv")

# 2. 사용할 변수 선택
features = ['avg_use_time_min', 'utility_score', 'leisure_score']
X = df[features]

# 3. 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. KMeans 군집화 (4개로 나눔)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

# 5. 사용자 유형 분류 함수 정의
def classify_user(row):
    if row['utility_score'] >= 6.0 and row['avg_use_time_min'] >= 40:
        return 'Strong Utilitarian'
    elif row['utility_score'] >= 6.0 and row['avg_use_time_min'] < 40:
        return 'Utilitarian'
    elif row['leisure_score'] >= 6.0 and row['avg_use_time_min'] >= 40:
        return 'Strong Overconsuming'
    elif row['leisure_score'] >= 6.0 and row['avg_use_time_min'] < 40:
        return 'Overconsuming'
    else:
        return 'Unclassified'

# 6. 사용자 분류 적용
df['classified_type'] = df.apply(classify_user, axis=1)

# 7. 결과 저장
df.to_csv("kmeans_classified_users.csv", index=False, encoding='utf-8-sig')