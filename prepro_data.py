import pandas as pd
import numpy as np
import os

def decompose_excel(df, excel_files_dir):
  if not os.path.exists(excel_files_dir):
    os.makedirs(excel_files_dir)

  for sheet in df.keys():
    df_sheet = df[sheet]
    df_sheet.to_excel(f"{excel_files_dir}\\{sheet}.xlsx")


def preprocess_excel_files(excel_files_dir):
  df_list = []

  for excel_file_name in os.listdir(excel_files_dir):
    if excel_file_name.endswith('.xlsx'):
      df = pd.read_excel(os.path.join(excel_files_dir, excel_file_name), skiprows=3, usecols=[2, 4, 5, 6], header=None)
      df['department'] = excel_file_name[:-5]
      df_list.append(df)

  df = pd.concat(df_list)
  return df


def reset_and_drop_index(df):
  df = df.reset_index()
  df = df.drop('index', axis=1)
  return df


def rename_and_reindex_columns(df):
  df = df.rename(columns={2: 'date', 4: 'cost', 5: 'name', 6: 'people'})
  df = df.reindex(columns=['department', 'name', 'cost', 'people', 'date'])
  df['name'] = df['name'].str.split(',').str[0]
  df['name'] = df['name'].str.split('/').str[0]
  return df


def re_rename(df, a, word, rename):
  df[a] = df[a].str.replace(word, rename, regex=False)


def drop_cost_comma(df):
  df['cost'] = df['cost'].astype(str)
  df['cost'] = df['cost'].str.replace(',', '').str.replace('[^0-9]', '', regex=False)
  df['cost'] = df['cost'].astype(int)


def drop_null(df):
  for i in df.columns:
    df = df[df[i].notnull()]
  return df


def clean_df(df):
  df['name'] = df['name'].replace('-', '')
  df['people'] = df['people'].replace('다수', '').replace('-', '')
  df['people'] = df['people'].replace('여명', '')
  df = df[df['name'] != '']
  df = df[df['people'] != '']
  df['people'] = df['people'].astype(int)

  return df