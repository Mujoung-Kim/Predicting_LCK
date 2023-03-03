# enviroment_values
from dotenv import load_dotenv
import os

# request API
import requests

# etc
from tqdm import tqdm
import json
import pandas as pd
import time

# load env setting
load_dotenv()

# request value
user_id = 'anenfdl'
nick_name = 'Arvens'
champion_rotations = 'lol/platform/v3/champion-rotations'
champion = f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{user_id}'
ranked = '/lor/ranked/v1/leaderboards'

# api key 및 받아올 데이터 변수
riot_key = os.environ.get('api_key')
skill = 'http://ddragon.leagueoflegends.com/cdn/13.4.1/data/en_US/champion.json'
test = 'http://ddragon.leagueoflegends.com/cdn/13.4.1/data/ko_KR/champion.json'

# request api
# base 401 권한 없음 -> postman 이용해서
# TODO base user_id or user_name 조회 및 postman 연결 진행해봐야됨.
base_url = f'https://kr.api.riotgames.com/{champion}?api_key={riot_key}'
base_data = requests.get(base_url)
test_data = requests.get(skill)

# 호출 결과값 파일로 저장
# with open('./data/test.txt', 'w') as ft:
# 	json.dump(test_data.json(), ft)

# test area
if __name__ == '__main__' : 
	print(test_data.json())