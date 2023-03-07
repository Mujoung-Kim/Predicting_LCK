from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import requests

import pandas as pd

# 상수
modules = '/Modules/chromedriver'
base_url = 'https://lol.fandom.com/wiki/LCK'

# 변수
season = '/2023_Season/Spring_Season'
champion_url = '/Champion_Statistics'
roster_url = '/Team_Rosters'
player_url = '/Player_Statistics'

# requests
driver = webdriver.Chrome(executable_path=modules)
driver.implicitly_wait(5)

# champion_status crawling table
def get_champion_status(url, season, file_name) :
	driver.get(f'{base_url}{season}{url}')

	table_data = driver.find_element_by_class_name('wikitable')
	column_names = table_data.text.split('\n')[3].split(' ')
	row_data = []

	for value in table_data.text.split('\n')[4:] :
		if value != '' :
			row_data.append(value.split(' '))
	df_table = pd.DataFrame(row_data, columns=column_names)
	df_table.to_csv(f'data/{file_name}.csv', index=False)

# team roster crawling table
def get_team_roster(url, season, file_name) :
	driver.get(base_url + season + url)

	table_data = driver.find_elements_by_class_name('wikitable')
	roster_names = driver.find_elements_by_class_name('catlink-teams')
	column_names = ['Team'] + table_data[0].text.split('\n')[0].split(' ')
	row_data = []
	team_list = []

	# team_name_list export
	for value in roster_names :
		team_list.append(value.text.split('\n')[0])

	# team_roster export
	for index in range(0, len(team_list)) :
		for value in table_data[index].text.split('\n')[1:] :
			if value != '' and value != 'KR':
				row_data.append({'Team':team_list[index], 'ID':value.split(' ')[0]})
	df_table = pd.DataFrame(row_data, columns=column_names[0:2])
	# df_table.to_csv(f'data/{file_name}.csv', index=False)
	return df_table

# player_status crawling table
# TODO : team_logo, most_champs 값이 이미지로 들어가 있어서 df로 변환이 불가능
# 가내 수공업으로 된 부분 자동화
def get_player_status(url, season, file_name) :
	driver.get(base_url + season + url)

	table_data = driver.find_element_by_class_name('wikitable')
	column_names = ['Team', 'Player'] + table_data.text.split('\n')[3].split(' ')
	row_data = []

	# 가내 수공업으로 된 이걸 roster 긁어와서 mapping
	team_list = ['Brion', 'Brion', 'Brion', 'Brion',  'Brion',
	     	'DplusKIA', 'DplusKIA', 'DplusKIA', 'DplusKIA', 'DplusKIA', 
			'DRX', 'DRX', 'DRX', 'DRX', 'DRX', 'DRX', 'DRX', 
			'Gen.G', 'Gen.G', 'Gen.G', 'Gen.G', 'Gen.G', 
			'HanWha', 'HanWha', 'HanWha', 'HanWha', 'HanWha', 
			'KTRolster', 'KTRolster', 'KTRolster', 'KTRolster', 'KTRolster', 
			'Kwangdong', 'Kwangdong', 'Kwangdong', 'Kwangdong', 'Kwangdong', 'Kwangdong',
			'Liiv Sandbox', 'Liiv Sandbox', 'Liiv Sandbox', 'Liiv Sandbox', 'Liiv Sandbox', 
			'NongShim', 'NongShim', 'NongShim', 'NongShim', 'NongShim', 
			'T1', 'T1', 'T1', 'T1', 'T1']

	for value in table_data.text.split('\n')[4:] :
		if value != '' :
			row_data.append(value.split(' '))
	df_table = pd.DataFrame(row_data, columns=column_names[0:20])
	df_table.to_csv(f'data/{file_name}.csv', index=False)
	
	# XXX : 이 부분 코드 효율적으로 수정해야됨.
	# 현재 기존 데이터 DF로 변환 -> 저장 후 다시 불러와서 team 값 대입하고 있음
	# TODO : 수정방안
	# Team roster로 team(value) : nick_name(key)로 묶어와서 해당 key값에 맞게 대입
	# 대입한 데이터를 DF로 변환 후 저장 -> 이 때 가능하면 most_three_champion 도
	df_train = pd.read_csv('data/23spring_players.csv')
	
	for index in range(0, len(df_train)) :
		df_train.team[index] = team_list[index]
	df_train.to_csv(f'data/{file_name}.csv', index=False)

# test_bed
if __name__ == '__main__' :
	# get_champion_status(champion_url, season, '23spring_champions')
	# get_player_status(player_url, season, '23spring_players')
	get_team_roster(roster_url, season, '23sping_roster')
	pass