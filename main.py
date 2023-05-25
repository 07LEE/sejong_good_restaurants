import os
import pandas as pd
import numpy as np
import category_kakao as kakao
import prepro_data as ppdata


def main():

    # Get the API key.
    API_KEY = kakao.get_API()

    # Get the file name.
    fname = input('Enter the name of the file : ')

    # Read the file.
    file = f'data\\{fname}.xlsx'
    df = pd.read_excel(file, sheet_name=None)

    # Preprocess the data.
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
    df = ppdata.clean_df(df)

    # Get the category.
    try:
        kakao.get_category(df, API_KEY)
    except:
        print('can not get category. check API')

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Save the data.
    if not os.path.exists('output_data'):
        os.makedirs('output_data')

    df.to_csv(f'output_data\\{fname}.csv', encoding='UTF-8')
    df.to_json(f'output_data\\{fname}.json', orient='records', indent=4, force_ascii=False)

if __name__ == '__main__':
    main()