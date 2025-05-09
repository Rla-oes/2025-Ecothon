import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. CSV 파일 불러오기
df = pd.read_csv("Step1/kmeans_classified_users.csv")

# 2. 3D 시각화 준비
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 3. 색상은 사용자 유형(classified_type)에 따라 다르게 지정
colors = pd.Categorical(df['classified_type']).codes
scatter = ax.scatter(
    df['avg_use_time_min'],
    df['utility_score'],
    df['leisure_score'],
    c=colors,
    cmap='Set2',
    s=60,
    alpha=0.8
)

# 4. 축 및 제목 설정
ax.set_xlabel("Average Use Time")
ax.set_ylabel("Utility Score")
ax.set_zlabel("Leisure Score")
ax.set_title("3D Visualization of KMeans-Classified Users")

# 5. 범례 생성 (수정)
legend_labels = pd.Categorical(df['classified_type']).categories.tolist()
handles, _ = scatter.legend_elements()
ax.legend(handles=handles, labels=legend_labels, title="User Type")

# 6. 이미지 저장
plt.tight_layout()
plt.savefig("kmeans_classified_users_3d.png", dpi=300)
plt.close()
