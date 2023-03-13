from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 찾는 요소가 존재 여부 파악하는 라이브러리
from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup
# import requests

# html to table
# import html_table_parser

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
	# df_table = pd.DataFrame(row_data, columns=column_names[0:2])
	# df_table.to_csv(f'data/{file_name}.csv', index=False)
	return row_data.keys(), row_data.values()

# 몇 개만 뽑아서 합쳐보죠 선수 데이터를 할껀데 팀을 자동으로 들어가는 식


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

# TODO : time, side 연결해서 넣어줘야됨.
# export_data : timeline, build(button_click를 이용해서 추출), allstatus(전체화면)
timeLine_url = 'https://gol.gg/game/stats/44907/page-timeline/'
# timeLine_url = f'https://gol.gg/game/stats/{game_num}/page-{export_data}/'

# driver.get(timeLine_url)

# timeLine_data = driver.find_elements_by_class_name('table_list')

# test_url = 'https://gol.gg/game/stats/44907/page-game/'
# driver.get(test_url)

# test = driver.find_elements_by_class_name('playersInfosLine')
# side = [['Side', 'Player', 'KDA', 'CS']]

# for idx in range(0, len(test)):
# 	for index in range(3, len(test[idx].text.split()) + 1) :
# 		if index % 3 == 0 and index > 4:
# 			if idx == 0 :
# 				side.append(['blue'] + test[idx].text.split()[index - 3:index])
# 			else : 
# 				side.append(['red'] + test[idx].text.split()[index - 3:index])
# df_side = pd.DataFrame(side[1:], columns=side[0])

# print([test[0].text.split()[index - 3:index] for index in range(3, len(test[0].text.split()) + 1) if index % 3 == 0])

# league match별 진영데이터
# TODO : game_numbering 생각해봐야됨 game_number or match_time
def get_match_side() :
	side = [['Side', 'Player', 'KDA', 'CS', 'Game_number']]

	for game_number in set_game_list() :
		url = f'https://gol.gg/game/stats/{game_number}/page-game/'
		driver.get(url)

		table_data = driver.find_elements_by_class_name('playersInfosLine')

		for idx in range(0, len(table_data)) :
			for index in range(3, len(table_data[idx].text.split()) + 1) :
				if index % 3 == 0 and index > 4 :
					if idx == 0 :
						side.append(['blue'] + table_data[idx].text.split()[index - 3:index] + [game_number])
					else :
						side.append(['red'] + table_data[idx].text.split()[index - 3:index] + [game_number])

	df_side = pd.DataFrame(side[1:], columns=side[0])
	# df_side.to_csv('data/test/side.csv', index=False)

	return df_side

# 해당 시즌 game_number모음
def set_game_list() :
	game_list = []

	with open('data/test/lck_list.txt', 'r', encoding='utf-8') as fr :
		rows = fr.readlines()

		for value in rows :
			game_list.extend(value.strip().split('\n'))

		return game_list

# TODO : game_number로 side값 연결해서 뽑아으면 됨. + 날짜값도 같이 뽑아오면 좋음.
def get_game_list () :
	game_list = []

	for index in range(44546, 47228):
		test = f'https://gol.gg/game/stats/{index}/page-game/'
		driver.get(test)

		try :
			game_number = driver.find_element_by_class_name('col-sm-7')
		except NoSuchElementException:
			continue
		else :
			if 'LCK S' in game_number.text:
				game_list.append(index)
			# if game_number.text in 'LCK Spring 2023 (KR)' :
			# 	game_list.append(index)
	
	with open('data/test/lck_list.txt', 'w+', encoding='utf-8') as fw:
		fw.write('\n'.join(map(str, game_list)))

# TODO : game_list 및 date infomation 
# test = f'https://gol.gg/game/stats/44546/page-game/'
# driver.get(test)

# tmp = driver.find_elements_by_class_name('row')

# match_all status
test = 'https://gol.gg/game/stats/44546/page-fullstats/'
driver.set_window_size(1920, 1080)
driver.get(test)

tmp = driver.find_element_by_class_name('tablesaw-swipe')
column_names = []

# df_test = pd.DataFrame(tmp.text.split('\n'))
# df_test = df_test.T

# for index in range(len(tmp.text.split())) :
# 	if index % 11 == 0 :
# 		column_names.append(tmp.text.split('\n')[index].split())

# 0 ~ 5 개의 문자들이 있는데 이걸 합쳐야 column_name이 된다.
for index in range(len(tmp.text.split('\n'))) :
	column_names.append(tmp.text.split('\n')[index].split()[0])

# test_bed
if __name__ == '__main__' :
	# get_champion_status(champion_url, season, '23spring_champions')
	# get_player_status(player_url, season, '23spring_players')
	# get_team_roster(roster_url, season, '23sping_roster')
	# print(timeLine_data[1].text.split('\n')[1:])
	# get_game_list()
	# print(set_game_list())
	# get_match_side()
	print(column_names)
	# print(tmp.text.split('\n'))
	# print(tmp.text.split('\n')[0].split())
	pass

