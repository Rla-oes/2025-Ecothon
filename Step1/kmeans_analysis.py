import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv("../Data/synthetic_users.csv")

features = ['ai_use_rate', 'avg_use_time_min', 'leisure_score', 'utility_score']

# 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# 최적 k 찾기 
inertia = []
K = range(2, 8)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(K, inertia, marker='o')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.grid()
plt.show()

# 플롯을 보고 적절한 k 선택 후 아래 코드에 대입
k_opt = 3
kmeans = KMeans(n_clusters=k_opt, n_init=10, random_state=42, verbose= 1)
df['cluster'] = kmeans.fit_predict(X_scaled)

print(df[features].info())
print(df[features].isnull().sum())

# 결과 저장
df.to_csv("synthetic_users_with_clusters.csv", index=False)
print(f"{k_opt}개 군집으로 분류 완료! 'cluster' 열 추가됨")