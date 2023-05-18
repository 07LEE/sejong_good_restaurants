#%%
import pandas as pd
import numpy as np
import os
import category_kakao as kakao
import prepro_data as ppdata

API_KEY = kakao.get_API()

file = 'data\\2023_03.xlsx'
df = pd.read_excel(file, sheet_name=None)

df = ppdata.preprocess_excel_files('prepro_data')
df = ppdata.reset_and_drop_index(df)
df = ppdata.rename_and_reindex_columns(df)

remove_list = ['조치원점', '조치원지점', '대평점', '전의점', '세종점', '보람점', '본점', '반곡점', '새롬점', '시청점', '시청스카이점', '나성점', '신흥점', '\(주\)', '\(세종\)', ' 세종', '\(LeBeef\)', '\(stay\)', '\(\)', '㈜신화케이푸드', ' ', '외1건','외1개소', '외1']

for i in remove_list:
    ppdata.re_rename(df, 'name', i, '')

ppdata.re_rename(df, 'name', '그릴200도씨', '그릴200도')
ppdata.re_rename(df, 'name', '그릴 200℃', '그릴200도')
df = df[df["name"].notnull()]

kakao.get_category(df, API_KEY)


# %% 파일 저장
# df.to_csv('df.csv', encoding='UTF-8')
# df.to_excel("df_with_category.xlsx")
if not os.path.exists('output_data'):
    os.makedirs('output_data')

df.to_excel('output_data\\df.xlsx')

# %%
