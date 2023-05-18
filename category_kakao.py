import requests
import pandas as pd

def get_API():
    with open('kakaomap.txt') as f:
        api = f.read()
    return api

def get_category(df, API_KEY):

    categories = []

    for index, row in df.iterrows():
        SEARCH_WORD = '세종시 ' + row["name"]

        URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query={}".format(SEARCH_WORD)
        HEADERS = {"Authorization": "KakaoAK {}".format(API_KEY)}

        response = requests.get(URL, headers=HEADERS)

        # 응답 확인
        if response.status_code == 200:
            results = response.json()["documents"]
            if results:
                try:
                    categories.append(results[0]["category_name"].split('>')[1])
                except:
                    categories.append(results[0]["category_name"].split('>')[0])
            else:
                categories.append("미분류")
        else:
            print("Error:", response.status_code)

    # 카테고리 열 생성
    df["category"] = categories