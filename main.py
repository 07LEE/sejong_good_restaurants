#%%
import pandas as pd
import numpy as np
import os, re
import category_kakao as kakao
import prepro_data as ppdata

API_KEY = kakao.get_API()
fname = input('Enter the name of the file : ')
file = f'data\\{fname}.xlsx'
df = pd.read_excel(file, sheet_name=None)

df = ppdata.preprocess_excel_files('prepro_data')
df = ppdata.reset_and_drop_index(df)
df = ppdata.rename_and_reindex_columns(df)

remove_list = ['조치원점', '조치원지점', '대평점', '전의점', '세종점', '보람점', '본점', '반곡점', '새롬점', '시청점', '시청스카이점', '나성점', '신흥점', '(주)', '(세종)', ' 세종', '(LeBeef)', '(stay)', r'\(\)', '㈜신화케이푸드', ' ', '외1건','외1개소', '외1']

for i in remove_list:
    ppdata.re_rename(df, 'name', i, '')

ppdata.re_rename(df, 'name', '그릴200도씨', '그릴200도')
ppdata.re_rename(df, 'name', '그릴 200℃', '그릴200도')

df = ppdata.drop_null(df)
ppdata.drop_cost_comma(df)

try:
    kakao.get_category(df, API_KEY)
except:
    print('can not get category. check API')

df['name'] = df['name'].replace('-', '')
df['people'] = df['people'].replace('다수', '').replace('-', '')
df = df[df['name'] != '']
df = df[df['people'] != '']
df['people'] = df['people'].astype(int)

# 파일 저장
if not os.path.exists('output_data'):
    os.makedirs('output_data')

df.to_csv(f'output_data\\{fname}.csv', encoding='UTF-8')
df.to_json(f'output_data\\{fname}.json', orient='records', indent=4, force_ascii=False)