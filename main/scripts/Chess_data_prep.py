import datetime as dt
from datetime import datetime
from datetime import timedelta
import shlex
import pandas as pd
import numpy


def dataframe_builder(name, start_year, end_year, time_control):
    # path = r'C:\Users\tsadmin\PycharmProjects\Codewars\Chess_scraping\\'
    path = r'.\.'
    root = name
    filename = path + root + '.txt'  # This is the path where the final CSV gets created
    person_of_interest = name
    UTC_DATE_KEY = '[UTCDate "'
    UTC_TIME_KEY = '[UTCTime "'
    termination = '[Termination'
    Total_games = 0
    with open(f'./{name}_{start_year}-{end_year}.txt', 'r') as infile:
        lines = infile.readlines()

        utc_date = None
        utc_time = None
        utc_endtime = ''

        empty_data = {'time': [],
                      'end_time': [],
                      'result': [],
                      'colour': [],
                      'reason': [],
                      'white_elo': [],
                      'black_elo': []
                      }

        final_data = {'time': [],
                      'end_time': [],
                      'result': [],
                      'colour': [],
                      'reason': [],
                      'white_elo': [],
                      'black_elo': []
                      }

        temp_data = {'time': [],
                     'end_time': [],
                     'result': [],
                     'colour': [],
                     'reason': [],
                     'white_elo': [],
                     'black_elo': []
                     }
        winsby = {'checkmate': 0, 'resignation': 0, 'time': 0, 'abandoned': 0}
        drawsby = {'repetition': 0, 'stalemate': 0, 'agreement': 0, 'insufficient material': 0,
                   'timeout vs insufficient material': 0, '50-move rule': 0}
        lossby = {'checkmate': 0, 'resignation': 0, 'time': 0, 'abandoned': 0}
        win_total = 0
        loss_total = 0
        draw_total = 0

        # Now we're going through all the games line by line (of the PGN format)

        for line in lines:
            fmt = '%Y.%m.%d %H:%M:%S'
            if f'White "{person_of_interest}"' in line:
                temp_data['colour'].append('White')
            if f'Black "{person_of_interest}"' in line:
                temp_data['colour'].append('Black')
            if line.startswith('[WhiteElo "'):
                WHITE_ELO = line[len('[WhiteElo "'):-3]
                temp_data['white_elo'].append(WHITE_ELO)
            if line.startswith('[BlackElo "'):
                BLACK_ELO = line[len('[BlackElo "'):-3]
                temp_data['black_elo'].append(BLACK_ELO)
            if line.startswith(UTC_DATE_KEY):
                utc_date = line[len(UTC_DATE_KEY):-3]
            if line.startswith(UTC_TIME_KEY):
                utc_time = line[len(UTC_TIME_KEY):-3]
                timestamp = datetime.strptime(utc_date + ' ' + utc_time, fmt)
                temp_data['time'].append(timestamp)
            if line.startswith('[EndTime "'):
                utc_endtime = line[len('[EndTime "'):-3]
                end_timestamp = datetime.strptime(utc_date + ' ' + utc_endtime, fmt)
                temp_data['end_time'].append(end_timestamp)
            if ('time_control' in line) and (f'time_control=\'{time_control}\'' not in line):
                # reinitialise temp_data
                temp_data = {'time': [],
                        'end_time': [],
                        'result': [],
                        'colour': [],
                        'reason': [],
                        'white_elo': [],
                        'black_elo': []
                            }
                continue 
            if (f'time_control=\'{time_control}\'' in line):
                # save data (temp) to final data, then reinitiliase data (temp)
                if temp_data != empty_data:
                
                    for i in temp_data:
                        final_data[i] = final_data[i] + temp_data[i]

                    temp_data = {'time': [],
                    'end_time': [],
                    'result': [],
                    'colour': [],
                    'reason': [],
                    'white_elo': [],
                    'black_elo': []
                        }
                        
        for line in lines:
            if termination in line:
                if 'Game drawn by' in line:
                    reason_parts = shlex.split(line.strip('[]\n'))[1].split()
                    draw_reason = ' '.join(reason_parts[3:])
                    draw_total += 1
                    temp_data['reason'].append(draw_reason)
                    temp_data['result'].append('draw')
                elif person_of_interest in line:
                    if 'won' in line:
                        reason_parts = shlex.split(line.strip('[]\n'))[1].split()
                        reason = reason_parts[len(reason_parts) - 1]
                        temp_data['reason'].append(reason)
                        temp_data['result'].append('win')
                        win_total += 1
                elif person_of_interest not in line and 'won' in line:
                    reason_parts = shlex.split(line.strip('[]\n'))[1].split()
                    loss_reason = reason_parts[len(reason_parts) - 1]
                    temp_data['reason'].append(loss_reason)
                    temp_data['result'].append('loss')
                    loss_total += 1
            if ('time_control' in line) and (f'time_control=\'{time_control}\'' not in line):
            # delete temp data
                temp_data = {'time': [],
                            'end_time': [],
                            'result': [],
                            'colour': [],
                            'reason': [],
                            'white_elo': [],
                            'black_elo': []
                            }
                continue 
            if f'time_control=\'{time_control}\'' in line:
                # save temp_data to final data, then reinitiliase temp_data
                if temp_data != empty_data:
                    for i in temp_data:
                        final_data[i] = [*final_data[i], *temp_data[i]]

                    temp_data = {'time': [],
                    'end_time': [],
                    'result': [],
                    'colour': [],
                    'reason': [],
                    'white_elo': [],
                    'black_elo': []
                                }

        chess_data = pd.DataFrame(final_data)

        return chess_data

def data_frame_refiner1(chess_data):
    #converting elo values from str to int.
    chess_data[["white_elo", "black_elo"]] = chess_data[["white_elo", "black_elo"]].apply(pd.to_numeric)
    chess_data['game_length_s'] = chess_data.end_time - chess_data.time
    chess_data['game_length_s'] = chess_data['game_length_s'].apply(timedelta.total_seconds)
    chess_data['game_length_s'] = chess_data['game_length_s'].apply(int)
    chess_data['game_length_m'] = chess_data['game_length_s'].apply(lambda x: round((x / 60), 2))
    #we made a game_length (seconds) column by taking difference of start and end times
    #We also converted game_length to minutes

    #DATA CLEANING
    #get rid of any weird minus game length times that shouldn't be there
    chess_data2 = (chess_data['game_length_s'] > 0) & (chess_data['game_length_s'] < 1201)
    chess_data = chess_data[chess_data2]

    #We've deleted some rows so let's reset the index count and delete the old index
    chess_data.reset_index(inplace=True)
    chess_data.drop(['index'], axis=1, inplace=True)
    chess_data['game_id'] = (chess_data.index + 1) # let's put a game count column in that starts from 1

    my_elo_list = []
    opponent_elo_list = []

    for index, row in chess_data.iterrows():
        if row['colour'] == 'White':
            my_elo_list.append(row['white_elo'])
            opponent_elo_list.append(row['black_elo'])
        else:
            my_elo_list.append(row['black_elo'])
            opponent_elo_list.append(row['white_elo'])

    my_elo = pd.Series(my_elo_list)
    opponent_elo = pd.Series(opponent_elo_list)
    chess_data['my_elo'] =  my_elo
    chess_data['opponent_elo'] = opponent_elo

    sample_size = len(chess_data.index) # let's save how many rows there are in case it's useful later

    chess_data['elo_difference'] = chess_data['opponent_elo'] - chess_data['my_elo']

    chess_data.groupby('time').time.apply(lambda x: (x.shift(1) - x))

    return chess_data

def data_frame_refiner2(chess_data, person_of_interest):

    def result_numerical_fn(x):
        if x == 'win':
            return 1
        elif x == 'draw':
            return 0
        elif x == 'loss':
            return -1

    def colour_numerical_fn(x):
        if x == 'White':
            return 1
        elif x == 'Black':
            return 0
    chess_data['colour_numerical'] = chess_data.colour.apply(colour_numerical_fn)
    #represent White = 1, Black = 0
    chess_data['result_numerical'] = chess_data.result.apply(result_numerical_fn)
    #represent win = 1, draw = 0, loss = -1

    def day_fn(x):
        return x.isoweekday()

    def month_fn(x):
        return x.month

    def month_day_fn(x):
        return x.day

    def hour_fn(x):
        return x.hour

    def minute_fn(x):
        return x.minute

    def second_fn(x):
        return x.second

    chess_data['Day'] = chess_data.time.apply(day_fn)
    chess_data['Month'] = chess_data.time.apply(month_fn)
    chess_data['Day_in_month'] = chess_data.time.apply(month_day_fn)
    chess_data['Hour'] = chess_data.time.apply(hour_fn)
    chess_data['Minute'] = chess_data.time.apply(minute_fn)
    chess_data['Second'] = chess_data.time.apply(second_fn)
    def time_fn(x):
        return dt.time(hour_fn(x), minute_fn(x), second_fn(x))

    chess_data['Time'] = chess_data.time.apply(time_fn)




    def daily_game_count():
        #return count of games from this day
        #if current_day == day then add 1 to count
        #if current_day != day before then reset count
        daily_game_count_list = []
        daily_game_count = 0
        previous_day = 1
        for index, row in chess_data.iterrows():
            if row['Day'] == previous_day:
                #same day as before
                daily_game_count_list.append(daily_game_count)
                daily_game_count +=1
            elif row['Day'] != previous_day:
                #new day now
                daily_game_count = 0
                daily_game_count_list.append(daily_game_count)
                daily_game_count +=1
                previous_day = row['Day']
        Daily_game_count = pd.Series(daily_game_count_list)
        chess_data['daily_game_count'] =  Daily_game_count


    def daily_result_aggregate():
        #return aggregate of result (1,0,-1) from this day
        daily_result_aggregate_list = []
        daily_result_aggregate = 0
        previous_day = 1

        for index, row in chess_data.iterrows():

            if row['Day'] == previous_day:
                daily_result_aggregate_list.append(daily_result_aggregate)
                daily_result_aggregate += row['result_numerical']
                #same day as before

            elif row['Day'] != previous_day:
                #new day now
                daily_result_aggregate = 0
                daily_result_aggregate_list.append(daily_result_aggregate)
                daily_result_aggregate +=1
                previous_day = row['Day']

        Daily_result_aggregate = pd.Series(daily_result_aggregate_list)

        chess_data['daily_result_aggregate'] =  Daily_result_aggregate

    def time_since_last_game():
        #return time(n) - time(n-1)
        time_since_last_game_list = []
        time_since_last_game = 0
        previous_time = 0
        for index, row in chess_data.iterrows():
            if previous_time == 0:
                time_since_last_game = row['time']
                time_since_last_game_list.append(time_since_last_game)
                previous_time = row['time']
            else:
                time_since_last_game = row['time'] - previous_time
                time_since_last_game_list.append(time_since_last_game)
                previous_time = row['time']
        Time_since_last_game = pd.Series(time_since_last_game_list)
        chess_data['time_since_last_game'] = Time_since_last_game


    daily_game_count()
    daily_result_aggregate()
    time_since_last_game()





    def last_game_result():
        #return result of last game
        #chess_data['last_game_result']
        previous_result_list = []
        previous_result_numerical = 0

        for index, row in chess_data.iterrows():
            previous_result_list.append(previous_result_numerical)
            previous_result_numerical = row['result_numerical']

        Previous_result = pd.Series(previous_result_list)
        chess_data['Previous_result'] =  Previous_result

    last_game_result()





    def length_of_last_game():
        #return length of last
        length_of_last_game_list = []
        length_of_last_game = 10

        for index, row in chess_data.iterrows():
            length_of_last_game_list.append(length_of_last_game)
            length_of_last_game = row['game_length_m']
        Length_of_last_game = pd.Series(length_of_last_game_list)
        chess_data['length_of_last_game'] = Length_of_last_game


    length_of_last_game()

    chess_data_first_row_temp = chess_data[0:1]
    chess_data = chess_data.iloc[1: , :]
    chess_data['time_since_last_game_m'] = chess_data['time_since_last_game'].apply(timedelta.total_seconds)
    chess_data['time_since_last_game_m'] = chess_data['time_since_last_game_m'].apply(int)
    chess_data['time_since_last_game_m'] = chess_data['time_since_last_game_m'].apply(lambda x: round((x / (60)), 2))

    chess_data = pd.concat([chess_data_first_row_temp, chess_data])

    #impute first row of time_since_last_game_m with mean to avoid null. DON'T REPEAT THIS STEP AS MEAN WILL CHANGE EACH TIME
    chess_data.time_since_last_game_m[0] = chess_data.time_since_last_game_m.mean()
    chess_data['time_since_last_game_m'] = chess_data['time_since_last_game_m'].apply(lambda x: round(x, 2))
    chess_data = chess_data.drop(columns='time_since_last_game')
    #Trigger factor is the result of last game * 1/time_since_last_game, so it takes into account how fresh the win/loss is.
    chess_data['trigger_factor'] = (1 / chess_data.time_since_last_game_m) * chess_data.Previous_result
    chess_data['my_elo_av'] = chess_data['my_elo'][::-1].rolling(window=30).mean()

    chess_data.to_csv(f'chess_data_{person_of_interest}.csv')

    return chess_data

