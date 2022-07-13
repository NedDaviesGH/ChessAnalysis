import Chess_Data_Scraping as scrap
import Chess_data_prep as prep

# Call this script to create the files for selected username, number of years, and gametype

username = 'ubad00d'
start_year = 2019
end_year = 2022
time_control = 600

scrap.count_all_games_in_year(username, start_year, end_year) #breaks if end year in future
scrap.json_parser(username, start_year, end_year)
scrap.concat_files(username, start_year, end_year)
scrap.delete_files(username, start_year, end_year)


###########################   Chess_data_prep.py

chess_data = prep.dataframe_builder(username, start_year, end_year, time_control)
chess_data = prep.data_frame_refiner1(chess_data)
chess_data = prep.data_frame_refiner2(chess_data, username)


