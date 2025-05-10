import pandas as pd
import numpy as np

# 1. 데이터 불러오기 (CSV 파일들 필요)
gender_df = pd.read_csv("Data/Data - gender.csv")
age_df = pd.read_csv("Data/Data - age_group.csv")
edu_df = pd.read_csv("Data/Data - edu_level.csv")
income_df = pd.read_csv("Data/Data - personal_income.csv")

# 2. 확률 분포 계산
gender_df['prob'] = gender_df['sample_count'] / gender_df['sample_count'].sum()
age_df['prob'] = age_df['sample_count'] / age_df['sample_count'].sum()
edu_df['prob'] = edu_df['sample_count'] / edu_df['sample_count'].sum()
income_df['prob'] = income_df['sample_count'] / income_df['sample_count'].sum()

# 3. 사용자 수 설정
N = 1000

# 4. 항목별 무작위 샘플링
genders = np.random.choice(gender_df['gender'], size=N, p=gender_df['prob'])
ages = np.random.choice(age_df['age_group'], size=N, p=age_df['prob'])
edus = np.random.choice(edu_df['edu_level'], size=N, p=edu_df['prob'])
incomes = np.random.choice(income_df['personal_income'], size=N, p=income_df['prob'])

# 5. 사용자 생성
users = []

for i in range(N):
    user = {
        'gender': genders[i],
        'age_group': ages[i],
        'edu_level': edus[i],
        'personal_income': incomes[i]
    }

    # 해당 항목별 점수 불러오기
    g = gender_df[gender_df['gender'] == user['gender']].iloc[0]
    a = age_df[age_df['age_group'] == user['age_group']].iloc[0]
    e = edu_df[edu_df['edu_level'] == user['edu_level']].iloc[0]
    inc = income_df[income_df['personal_income'] == user['personal_income']].iloc[0]

    # 기본 평균값
    avg_time = np.mean([g['avg_use_time'], a['avg_use_time'], e['avg_use_time'], inc['avg_use_time']])
    leisure = np.mean([g['leisure_score'], a['leisure_score'], e['leisure_score'], inc['leisure_score']])
    utility = np.mean([g['utility_score'], a['utility_score'], e['utility_score'], inc['utility_score']])

    # 6. 일부 사용자에게 편향 부여
    mode = np.random.choice(['utility', 'leisure', 'balanced'], p=[0.3, 0.3, 0.4])
    if mode == 'utility':
        utility += np.random.normal(10, 3)
        leisure -= np.random.normal(5, 2)
    elif mode == 'leisure':
        leisure += np.random.normal(10, 3)
        utility -= np.random.normal(5, 2)

    # 음수 방지
    leisure = max(leisure, 0)
    utility = max(utility, 0)

    user['avg_use_time_min'] = avg_time
    user['leisure_score'] = leisure
    user['utility_score'] = utility

    users.append(user)

# 7. 저장
df = pd.DataFrame(users)
df.to_csv("synthetic_users_allAIusers.csv", index=False, encoding='utf-8-sig')

