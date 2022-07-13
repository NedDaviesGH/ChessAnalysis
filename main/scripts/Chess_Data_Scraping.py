# from chessdotcom import get_player_profile as profile
# from chessdotcom import is_player_online as online
# from chessdotcom import get_player_stats as stats
from chessdotcom import get_player_games_by_month as month
# from chessdotcom import get_player_game_archives as archives
# from chessdotcom import get_player_games_by_month_pgn as pgn_month
from datetime import datetime
import os
import numpy

def count_all_games_in_year(NAME, first, last):
    for YEAR in range(first, last):
        for MONTH in range(1,13):
            if MONTH > datetime.now().month and YEAR == datetime.now().year:
                break
            if MONTH == 1:
                print(f'\nlet\'s look at {NAME}')
                print(f'creating a new file called {NAME}_{YEAR}.txt')
                raw_details = str(month(NAME, YEAR, MONTH))
                raw_file = open(f'{NAME}_{YEAR}.txt', "w")
                raw_file.write(str(raw_details))
                raw_file.close()
            else:
                raw_details = str(month(NAME, YEAR, MONTH))
                raw_file = open(f'{NAME}_{YEAR}.txt', "a")
                raw_file.write(str(raw_details))
                raw_file.close()

        raw_file = open(f'{NAME}_{YEAR}.txt', "r")
        string_raw_file = raw_file.read()

        game_count = string_raw_file.count(f'username=\'{NAME}\'')
        # if game_count == 0:
        #     print('No games this year, deleting file')
        #     os.remove(f'{NAME}_{YEAR}.txt')

        win_count = string_raw_file.count(f'{NAME} won')
        draw_count = string_raw_file.count(f'draw')
        print(f'{NAME} played', game_count, f'games of chess in {YEAR}')
        print(f'{NAME} won', win_count, 'games')
        print(f'{NAME} drew', draw_count, 'games')
        print(f'{NAME} lost', game_count - win_count - draw_count, 'games')
        raw_file.close()




def json_parser(name, start_year, end_year):
    # path = r'C:\Users\tsadmin\PycharmProjects\Codewars\Chess_scraping'
    path = r'.\.'
    for year in range(start_year,end_year):
        root = f'\\{name}_{year}'
        filename = path + root + '.txt'
        with open(filename, 'r') as chessfile:
            lines = chessfile.readlines()
            line = lines[0].replace('\\n', '\n')
        with open(path + root + '.txt', 'w') as outfile:
            outfile.write(line)


def concat_files(name, start_year, end_year):
    filenames = []
    for year in range(start_year, end_year):
        filenames.append(f'{name}_{year}.txt')
    with open(f'./{name}_{start_year}-{end_year}.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    return outfile

def delete_files(name, start_year, end_year):
    for year in range(start_year, end_year):
        os.remove(f'./{name}_{year}.txt')









