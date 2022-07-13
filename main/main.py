import Chess_Data_Scraping as scrap
import Chess_data_prep as prep
import Chess_data_analysis as anal
# import Chess_data_modelling as mod
import PySimpleGUI as sg
# import sys

###########################   Chess_Data_Scraping.py

# Call this script to create the files for selected username, number of years, and gametype
# username = input('Please input a username: ')
# start_year = int(input('Please input the year to start: '))
# end_year = int(input('Please input the year to end: ')) + 1
# time_control = int(input('Please input time control to include in seconds: '))

sg.theme('DarkAmber')
layout = [[sg.T('Enter your chess.com username'), sg.In(key='-ID1-')],
          [sg.T('Enter the year to start analysis'), sg.In(key='-ID2-')],
          [sg.T('Enter the year to end analysis'), sg.In(key='-ID3-')],
          [sg.T('Enter time control'), sg.In(key='-ID4-')],
          [sg.Button('Read'), sg.Exit()]]
window = sg.Window('Chess.com Analysis Program', layout)

while True:  # The Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit' or (type(values['-ID1-']) == str and type(int(values['-ID2-'])) == int
                                                     and type(int(values['-ID3-'])) == int):
        break

username = str(values['-ID1-'])
start_year = int(values['-ID2-'])
end_year = int(values['-ID3-']) + 1
time_control = int(values['-ID4-'])
window.close()

sg.theme('DarkAmber')  # Keep things interesting for your users
layout = [[sg.T(f'Initiate data scraping for {username}\'s {time_control}s games between {start_year} and {end_year}')],
          [sg.Exit('Next')]]
window = sg.Window('Chess.com Analysis Program', layout)
window.read()

scrap.count_all_games_in_year(username, start_year, end_year) #breaks if end year in future
scrap.json_parser(username, start_year, end_year)
scrap.concat_files(username, start_year, end_year)
scrap.delete_files(username, start_year, end_year)
window.close()

###########################   Chess_data_prep.py

sg.theme('DarkAmber')
layout = [[sg.T(f'Initiate data prep for {username}')],
          [sg.Exit('Next')]]
window = sg.Window('Chess.com Analysis Program', layout)
window.read()

chess_data = prep.dataframe_builder(username, start_year, end_year, time_control)
chess_data = prep.data_frame_refiner1(chess_data)
chess_data = prep.data_frame_refiner2(chess_data, username)
window.close()

###########################   Chess_data_analysis.py

sg.theme('DarkAmber')  # Keep things interesting for your users
layout =   [[sg.T(f'Made chess_data_{username}_{start_year}_{end_year}.csv')],
            [sg.T(f'containing {chess_data.columns}')],
            [sg.T(f'Initiate data analysis for {username}')],
            [sg.Exit('Next')]]
window = sg.Window('Chess.com Analysis Program', layout)
window.read()

av_g_l, av_t, av_gpd, av_tpd, game_count = anal.analysis(chess_data, username, start_year, end_year)
window.close()


###########################   Chess_data_modelling.py
# sg.theme('DarkAmber')  # Keep things interesting for your users
# layout =   [[sg.T(f'Analysis of chess games complete')],
#             [sg.T(f'You played {game_count} {time_control}s games between {start_year} and {end_year}')],
#             [sg.T(f'On average you played {round(av_tpd)}m per day')],
#             [sg.T(f'This works out as averaging {av_gpd} games per day')],
#             [sg.Exit('Next')]]
# window = sg.Window('Chess.com Analysis Program', layout)
# window.read()
# mod.first_model(chess_data, username)
# mid.second_model(chess_data, username)