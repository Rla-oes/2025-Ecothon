import pandas as pd
import numpy as np

gender_df = pd.read_csv("Data - gender.csv")
age_df = pd.read_csv("Data - age_group.csv")
edu_df = pd.read_csv("Data - edu_level.csv")
income_df = pd.read_csv("Data - personal_income.csv")

gender_df['prob'] = gender_df['sample_count'] / gender_df['sample_count'].sum()
age_df['prob'] = age_df['sample_count'] / age_df['sample_count'].sum()
edu_df['prob'] = edu_df['sample_count'] / edu_df['sample_count'].sum()
income_df['prob'] = income_df['sample_count'] / income_df['sample_count'].sum()

N = 1000

genders = np.random.choice(gender_df['gender'], size=N, p=gender_df['prob'])
ages = np.random.choice(age_df['age_group'], size=N, p=age_df['prob'])
edus = np.random.choice(edu_df['edu_level'], size=N, p=edu_df['prob'])
incomes = np.random.choice(income_df['personal_income'], size=N, p=income_df['prob'])

users = []

for i in range(N):
    user = {
        "gender": genders[i],
        "age_group": ages[i],
        "edu_level": edus[i],
        "personal_income": incomes[i],
    }

    g = gender_df[gender_df['gender'] == user['gender']].iloc[0]
    a = age_df[age_df['age_group'] == user['age_group']].iloc[0]
    e = edu_df[edu_df['edu_level'] == user['edu_level']].iloc[0]
    inc = income_df[income_df['personal_income'] == user['personal_income']].iloc[0]

    user["ai_use_rate"] = np.mean([g['ai_use_rate'], a['ai_use_rate'], e['ai_use_rate'], inc['ai_use_rate']])
    user["avg_use_time_min"] = np.mean([g['avg_use_time'], a['avg_use_time'], e['avg_use_time'], inc['avg_use_time']])
    user["leisure_score"] = np.mean([g['leisure_score'], a['leisure_score'], e['leisure_score'], inc['leisure_score']])
    user["utility_score"] = np.mean([g['utility_score'], a['utility_score'], e['utility_score'], inc['utility_score']])

    users.append(user)

# 결과 저장
df = pd.DataFrame(users)
df.to_csv("synthetic_users.csv", index=False, encoding='utf-8-sig')

print("생성 완료!")