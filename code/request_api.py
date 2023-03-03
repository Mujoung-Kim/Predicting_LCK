# enviroment_values
from dotenv import load_dotenv
import os

# request API
import requests

# etc
from tqdm import tqdm
import pandas as pd
import json
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
# TODO base user_id or user_name 조회 및 thunder client로 연결해서 api 결과확인.
base_url = 'https://kr.api.riotgames.com'

# master 등급 솔랭 플레이한 플레이어의 summoner_id 추출
def summoner_export(base_url, tier) :
	url = f'{base_url}/lol/league/v4/{tier}/by-queue/RANKED_SOLO_5x5?api_key={riot_key}'
	summoner_id = {}
	count = 0

	response = requests.get(url)
	# 발급 받고 바로 사용해서 유요한 key임을 등록
	response = response.json()['entries']

	for i in response :
		summoner_id[i['summonerName']] = i['summonerId']
		count += 1

	return summoner_id.values(), summoner_id.keys()

# summoner_id를 통한 puuid 추출
def summoner_infomation() :
	summoner_id, summoner_name = summoner_export(base_url, 'masterleagues')
	puuid = {}

	for i, j in zip(tqdm(summoner_id), summoner_name) :
		url = f'{base_url}/lol/summoner/v4/summoners/{i}?api_key={riot_key}'
		response = requests.get(url)

		if response.status_code == 200 :
			pass
		elif response.status_code == 429 :
			print('\napi cost full : infinite loop start')
			print(f'loop location : {i}')

			start_time = time.time()

			while True :
				if response.status_code == 429 :
					print('try 120 second wait time')

					time.sleep(120)
					response = requests.get(url)
					print(response.status_code)

				elif response.status_code == 200 :
					print(f'total wait time : {time.time() - start_time}')
					print('recovery api cost')
					break

	df_puuid = pd.DataFrame(puuid, index = [0])
	df_puuid = df_puuid.T
	df_puuid = df_puuid.reset_index()
	puuid.columns = ['id', 'puuid']

	return df_puuid

# 최근 5게임의 match_id 추출
def export_five_match_id() :
	match_id = []

	for i in tqdm(summoner_infomation()['puuid']) :
		url = f'{base_url}/lol/match/v5/matches/by-puuid/{i}/ids?start=1&count=5&api_key={riot_key}'
		response = requests.get(url)

		if response.status_code == 200 :
			pass
		
		elif response.status_code == 429 :
			print('\napi cost full : infinite loop start')
			print(f'loop location : {i}')
			start_time = time.time()

		match_id.extend(requests.get(url).json())
	
	len(match_id)
	match_set = set(match_id)
	match_list = list(match_set)
	len(match_list)

	return match_list


# 호출 결과값 파일로 저장
# with open('./data/test.txt', 'w') as ft:
# 	json.dump(test_data.json(), ft)

# test area
if __name__ == '__main__' : 
	# print(summoner_export(base_url, 'masterleagues'))
	print(summoner_infomation())