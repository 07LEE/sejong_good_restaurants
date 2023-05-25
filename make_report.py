#%%
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re, os
import category_kakao as kakao

file = 'output_data'
files = [i for i in os.listdir(file) if i.endswith('.csv')]
df = pd.read_csv(f'output_data\\{files[0]}')
df = df.drop(columns=['Unnamed: 0'])

# 업무 추진비 사용 경향

# 업무 추진비 사용 금액
department_cost = df.groupby('department')['cost'].sum()
print(department_cost)

# 부서별 인원수 대비 금액
department_people = df.groupby('department')['people'].sum()
department_cost_per_person = department_cost / department_people
print(round(department_cost_per_person), 1)

# 가장 많이 방문한 가게
name_count = df['name'].value_counts()

# 가장 많은 금액을 쓴 가게
name_cost = df.groupby('name')['cost'].sum()
name_cost = name_cost.sort_values(ascending=False)

# 이름별 비용 합계 계산
name_counts = name_count[name_count >= 2]
cost_count = name_cost/name_counts
cost_count = cost_count.dropna()
cost_count = cost_count.sort_values(ascending=False)

# 다양한 부서가 방문한 가게
depart_name = df.groupby('name')['department'].nunique()
depart_name = depart_name.sort_values(ascending=False)

# # Markdown 문서 생성

header = f"""
# 세종시 업무추진비 맛집 ({files[0]})

업무추진비 URL : https://www.sejong.go.kr/bbs/R0091/list.do
"""

body = f"""
## 업무 추진비 사용 내역

### (1) 많이 방문한 가게

{name_count.head(5).to_markdown()}

### (2) 많은 금액을 지출한 가게

{name_cost.map('{:,.0f}'.format).head(5).to_markdown()}

### (3) 방문 횟수 대비 비용이 큰 가게

{cost_count.map('{:,.0f}'.format).head(5).to_markdown()}

### (4) 다양한 부서가 방문하는 가게

{depart_name.map('{:,.0f}'.format).head(5).to_markdown()}

"""

md_file = header + body

# 파일 작성
if not os.path.exists('report'):
    os.makedirs('report')

with open(f"report\\{files[0]}.md", "w") as f:
  f.write(md_file)