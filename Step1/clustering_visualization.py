import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv("Step1/synthetic_users_with_clusters.csv") 
features = ['ai_use_rate', 'avg_use_time_min', 'leisure_score', 'utility_score']
X = df[features]

# 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA 2D 변환
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# 군집 예측 
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X_scaled)  


plt.figure(figsize=(8, 6))

# Decision Boundary 만들기
x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500),
                     np.linspace(y_min, y_max, 500))
grid = np.c_[xx.ravel(), yy.ravel()]

# PCA 기준으로 재학습한 kmeans로 predict (주의: pca 말고 X_scaled 기반이면 좌표 일치 안됨)
# grid는 PCA 공간이므로 kmeans도 X_pca 기준으로 다시 fit 해야 정확함
kmeans_pca = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_pca)
Z = kmeans_pca.predict(grid)
Z = Z.reshape(xx.shape)

# 경계선 
plt.contourf(xx, yy, Z, alpha=0.2, cmap='Set2')

# 클러스터 점 시각화
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['cluster'], palette='Set2', s=60)
plt.title("KMeans Clustering with Decision Boundaries")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.grid(True)
plt.legend(title="Cluster")
plt.savefig("Step1/cluster_visualization.png", dpi=300)  # 파일명과 경로, 해상도 지정
plt.tight_layout()
plt.show()
