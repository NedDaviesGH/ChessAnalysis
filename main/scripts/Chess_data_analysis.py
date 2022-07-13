import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.ticker import PercentFormatter
import seaborn as sns
##########
#ANALYSIS#
##########

# chess_data = pd.read_csv('./chess_data_ubad00d.csv')

def analysis(chess_data, username, start_year, end_year):
    # last = datetime.strptime(chess_data.time.iloc[-2:-1])
    # first = datetime.strptime(chess_data.time.iloc[0])
    game_count = chess_data.time.size
    last = chess_data.time.iloc[-2:-1]
    first = chess_data.time.iloc[0]
    difference = last - first
    difference = int(difference.values) / (10 ** 9)
    total_month_difference = round((((difference / 60) / 60) / 24) / 365 * 12)
    total_day_difference = round((((difference / 60) / 60) / 24))
    average_game_length = chess_data.game_length_m.mean()
    average_time_since_last_game = chess_data.time_since_last_game_m.mean()
    average_games_per_day = chess_data.game_id.count() / total_day_difference
    average_total_time_playing_per_day =  average_games_per_day * chess_data.game_length_m.mean()
    av_g_l, av_t, av_gpd, av_tpd = average_game_length, average_time_since_last_game, average_games_per_day, average_total_time_playing_per_day


    pdf = matplotlib.backends.backend_pdf.PdfPages(f"Chess_analysis_{username}_{start_year}_{end_year}.pdf")
    #save average_total_time_playing_per_day, average_games_per_day,
    # average_game_length, average_time_since_last_game to pdf

    firstPage = plt.figure(figsize=(11.69,8.27))
    firstPage.clf()
    txt = f'Here\'s some cool stats about {username}:'
    if game_count < 100:
        stats = 'Average game length (mins): ' + str(
            round(av_g_l)) + '\n' + 'Average time between games (mins): ' + str(round(av_t)) \
                + '\n' + 'Average games per day: ' + str(av_gpd) + '\n' + 'Average time playing per day (mins): ' \
                + str(round(av_tpd)) + '\n' + f'You played {game_count} games between {start_year} and {end_year}... do you even know how to move the pieces?'
    elif game_count > 100 and game_count < 1000:
        stats = 'Average game length (mins): ' + str(
            round(av_g_l)) + '\n' + 'Average time between games (mins): ' + str(round(av_t)) \
                + '\n' + 'Average games per day: ' + str(av_gpd) + '\n' + 'Average time playing per day (mins): ' \
                + str(round(av_tpd)) + '\n' + f'You played {game_count} games between {start_year} and {end_year}... need to do better than that'
    elif game_count > 1000:
        stats = 'Average game length (mins): ' + str(
            round(av_g_l)) + '\n' + 'Average time between games (mins): ' + str(round(av_t)) \
                + '\n' + 'Average games per day: ' + str(av_gpd) + '\n' + 'Average time playing per day (mins): ' \
                + str(round(av_tpd)) + '\n' + f'You played {game_count} games between {start_year} and {end_year}.. you need to get a life'

    firstPage.text(0.5, 0.5, stats, transform=firstPage.transFigure, size=24, ha="center", va='bottom')
    firstPage.text(0.3,0.5,txt, transform=firstPage.transFigure, size=24, ha="center", va='top')

    pdf.savefig()
    plt.close()



    # chess_data = chess_data.head(10)


    #Win rate per month

    chess_data_win = chess_data[chess_data['result'] == 'win']
    sample_size_win = len(chess_data_win.index)
    fig1 = plt.figure()
    plt.hist(chess_data_win['time'], color = 'blue', edgecolor = 'black',
             figure=fig1, bins = total_month_difference)
    plt.title(f'{username}: Number of wins per month (out of {sample_size_win} wins)')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.gcf().autofmt_xdate() #make X axis look better with dates

    pdf.savefig(fig1)
    plt.close()

    #plot distribution of losses across time as histogram
    chess_data_loss = chess_data[chess_data['result'] == 'loss']
    sample_size_loss = len(chess_data_loss.index)
    fig2 = plt.figure()
    plt.hist(chess_data_loss['time'], color = 'blue', edgecolor = 'black',
             figure=fig2, bins = total_month_difference)
    plt.title(f'{username}: Number of losses per month (out of {sample_size_loss} losses)')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.gcf().autofmt_xdate() #make X axis look better with dates
    pdf.savefig(fig2)
    plt.close()

    #plot distribution of draws across time as histogram
    chess_data_draw = chess_data[chess_data['result'] == 'draw']
    sample_size_draw = len(chess_data_draw.index)
    fig3 = plt.figure()
    plt.hist(chess_data_draw['time'], color = 'blue', edgecolor = 'black',
             figure=fig3, bins = total_month_difference)
    plt.title(f'{username}: Number of draws per month (out of {sample_size_draw} draws)')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.gcf().autofmt_xdate() #make X axis look better with dates
    pdf.savefig(fig3)
    plt.close()

    #plot bar chart of number of reasons for win/loss

    # plt.hist(chess_data['reason'], color = 'blue', edgecolor = 'black')
    #
    # plt.xlabel('Reason')
    # plt.ylabel('Frequency')
    # plt.gcf().autofmt_xdate()

    fig4 = plt.figure()
    plt.hist(chess_data_win['reason'], color = 'blue', edgecolor = 'black', figure=fig4)
    plt.xlabel('Reason for win')
    plt.ylabel('Frequency')
    plt.gcf().autofmt_xdate()
    pdf.savefig(fig4)
    plt.close()

    fig5 = plt.figure()
    plt.hist(chess_data_loss['reason'], color = 'blue', edgecolor = 'black', figure=fig5)
    plt.xlabel('Reason for loss')
    plt.ylabel('Frequency')
    plt.gcf().autofmt_xdate()
    pdf.savefig(fig5)
    plt.close()

    fig6 = plt.figure()
    plt.hist(chess_data_draw['reason'], color = 'blue', edgecolor = 'black', figure=fig6)
    plt.xlabel('Reason for draw')
    plt.ylabel('Frequency')
    plt.gcf().autofmt_xdate()
    pdf.savefig(fig6)
    plt.close()

    #plot distribution of games across time as histogram

    sample_size = len(chess_data.index)
    fig7 = plt.figure()
    plt.hist(chess_data['time'], color = 'blue', edgecolor = 'black',
             figure=fig7, bins = total_month_difference)
    plt.title(f'{username}: Number of games per month (out of {sample_size} games)')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.gcf().autofmt_xdate() #make X axis look better with dates
    pdf.savefig(fig7)

    # Wins/loss/draws on one histograms
    fig8 = plt.figure()
    plt.hist(chess_data_win['time'], figure=fig8,alpha=0.5, label='wins', bins = total_month_difference)
    plt.hist(chess_data_loss['time'], figure=fig8,alpha=0.5, label='losses', bins = total_month_difference )
    plt.hist(chess_data_draw['time'], figure=fig8,alpha=0.5, label = 'draws', bins = total_month_difference)
    plt.title(f'{username}: Number of games per month (out of {sample_size} games)')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.gcf().autofmt_xdate()
    pdf.savefig(fig8)

    # # Wins/loss/draws using subplots

    fig9, axs = plt.subplots(4, sharex=True)
    axs[0].hist(chess_data['time'], figure=fig9,alpha=0.5, label='Games', bins = total_month_difference)
    axs[1].hist(chess_data_win['time'], figure=fig9,alpha=0.5, label='wins', bins = total_month_difference)
    axs[2].hist(chess_data_loss['time'], figure=fig9,alpha=0.5, label='losses', bins = total_month_difference)
    axs[3].hist(chess_data_draw['time'], figure=fig9, alpha=0.5, label = 'draws', bins = total_month_difference)
    plt.suptitle(f'{username}: Number of games per month (out of {sample_size} games)')
    axs[0].set_title('Total')
    axs[1].set_title('Wins')
    axs[2].set_title('Losses')
    axs[3].set_title('Draws')
    plt.gcf().autofmt_xdate()
    fig9.tight_layout()
    fig9.text(0.53, -0.1, 'Date', ha='center')
    fig9.text(0.00, 0.5, 'Frequency', va='center', rotation='vertical')
    pdf.savefig(fig9)

    #plot distribution of game lengths
    fig10 = plt.figure()
    histogram = plt.hist(chess_data['game_length_m'],
                         weights=np.ones(chess_data.game_length_m.count()) / chess_data.game_length_m.count(),
                         color = 'blue', edgecolor = 'black', bins = 20, figure=fig10)
    plt.title(f'{username}: Game Length distribution (out of {sample_size} games)')
    plt.xlabel('Time / mins')
    plt.ylabel('Percentage')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    pdf.savefig(fig10)

    #plot histogram of game length distribution for WINS only

    chess_data_win = chess_data[chess_data['result'] == 'win'] # dataframe only with win rows included
    sample_size_wins = len(chess_data_win.index)
    fig11 = plt.figure()
    histogram = plt.hist(chess_data_win['game_length_m'], color = 'blue',
                         figure=fig11,edgecolor = 'black', bins = 20)
    plt.title(f'{username}: Game Length distribution (out of {sample_size_wins} wins)')
    plt.xlabel('Time / mins')
    plt.ylabel('Frequency')
    pdf.savefig(fig11)

    #plot histogram of game length distribution for LOSSES only
    chess_data_loss = chess_data[chess_data['result'] == 'loss'] # dataframe only with win rows included
    sample_size_loss = len(chess_data_loss.index)
    fig12 = plt.figure()
    histogram = plt.hist(chess_data_loss['game_length_m'], color = 'blue',
                         figure=fig12, edgecolor = 'black', bins = 20)
    plt.title(f'{username}: Game Length distribution (out of {sample_size_loss} losses)')
    plt.xlabel('Time / mins')
    plt.ylabel('Frequency')
    pdf.savefig(fig12)

    #plot histogram of game length distribution for DRAWS only

    chess_data_draw = chess_data[chess_data['result'] == 'draw'] # dataframe only with win rows included
    sample_size_draw = len(chess_data_draw.index)
    fig13 = plt.figure()
    histogram = plt.hist(chess_data_draw['game_length_m'], color = 'blue',
                         figure=fig13,edgecolor = 'black', bins = 20)
    plt.title(f'{username}: Game Length distribution (out of {sample_size_draw} draws)')
    plt.xlabel('Time / mins')
    plt.ylabel('Frequency')
    pdf.savefig(fig13)

    # Wins/loss/draws on one histograms
    fig14 = plt.figure()
    plt.hist(chess_data_win['game_length_m'], alpha=0.5, label='wins',
             figure=fig14,bins = 30)
    plt.hist(chess_data_loss['game_length_m'], alpha=0.5, label='losses',
             figure=fig14,bins = 30 )
    plt.hist(chess_data_draw['game_length_m'], alpha=0.5, label = 'draws',
             figure=fig14,bins = 30)
    plt.title(f'{username}: Game Length distribution (out of {sample_size} games)')
    plt.xlabel('Time / mins')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    pdf.savefig(fig14)

    #plot distribution of white_elo
    fig15 = plt.figure()
    graph = plt.hist(chess_data['white_elo'], color = 'blue',
                     figure=fig15,edgecolor = 'black', bins = 10)
    plt.title(f'{username}: White ELO distribution (out of {sample_size} games)')
    plt.xlabel('White ELO')
    plt.ylabel('Frequency')
    plt.gcf()
    pdf.savefig(fig15)

    #plot distribution of black_elo
    fig16 = plt.figure()
    graph = plt.hist(chess_data['black_elo'], color = 'blue',
                     figure=fig16,edgecolor = 'black', bins = 10)
    plt.title(f'{username}: Black ELO distribution (out of {sample_size} games)')
    plt.xlabel('Black ELO')
    plt.ylabel('Frequency')
    plt.gcf()
    pdf.savefig(fig16)

    #plot distribution of my ELO
    fig17 = plt.figure()
    graph = plt.hist(chess_data['my_elo'], color = 'blue',
                     figure=fig17,edgecolor = 'black', bins = 20)
    plt.title(f'{username}: ELO distribution (out of {sample_size} games)')
    plt.xlabel('ELO')
    plt.ylabel('Frequency')
    pdf.savefig(fig17)

    #plot distribution of opponent's elo
    fig18 = plt.figure()
    graph = plt.hist(chess_data['opponent_elo'], color = 'blue',
                     figure=fig18,edgecolor = 'black', bins = 20)
    plt.title(f'{username}: ELO distribution (out of {sample_size} games)')
    plt.xlabel('ELO')
    plt.ylabel('Frequency')
    pdf.savefig(fig18)

    #plot game length barchart/boxplot vs day of week

    #my_elo/opponent elo vs game_id
    fig19 = plt.figure()
    plt.plot(chess_data['game_id'], chess_data['my_elo'], label='My ELO',
             figure=fig19,color = 'blue')
    plt.plot(chess_data['game_id'], chess_data['opponent_elo'],linewidth=0.5,alpha=0.5,
             figure=fig19,label='Opponent\'s ELO',color = 'red')
    plt.xlabel('Game ID')
    plt.ylabel('ELO')
    plt.title(f'{username}: ELO vs game ID')
    plt.legend(loc='lower right')
    pdf.savefig(fig19)

    #my elo/opponent elo vs time
    fig20 = plt.figure()
    plt.plot(chess_data['time'], chess_data['my_elo'], label='My ELO', color = 'blue',
             figure=fig20)
    plt.plot(chess_data['time'], chess_data['opponent_elo'],linewidth=0.5,alpha=0.5,
             figure=fig20,label='Opponent\'s ELO',color = 'red')
    plt.xlabel('time')
    plt.ylabel('ELO')
    plt.gcf().autofmt_xdate()

    plt.title(f'{username}: ELO vs time')
    plt.legend(loc='lower right')
    pdf.savefig(fig20)

    #plot number of games vs hour in the day
    fig21 = plt.figure()
    graph = plt.hist(chess_data['Hour'], color = 'blue', edgecolor = 'black',
                     figure=fig21,bins = 20, alpha=0.2)
    plt.title(f'{username}: Hour distribution (out of {sample_size} games)')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    pdf.savefig(fig21)

    #plot number of wins vs hour in the day
    fig22 = plt.figure()
    graph2 = plt.hist(chess_data_win['Hour'], color = 'red',
                      figure=fig22,edgecolor = 'black', bins = 20, alpha=0.2)
    plt.title(f'{username}: Hour distribution (out of {sample_size_win} games)')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    pdf.savefig(fig22)

    #plot number of losses vs hour in the day
    fig23 = plt.figure()
    graph3 = plt.hist(chess_data_loss['Hour'], color = 'green',
                      figure=fig23,edgecolor = 'black', bins = 20, alpha=0.2)
    plt.title(f'{username}: Hour distribution (out of {sample_size_loss} games)')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    pdf.savefig(fig23)

    #Win rate vs hour of day

    # #Games over time

    # graph = plt.plot_date(chess_data['Time'], chess_data['result'], color = 'blue')
    # plt.title(f'Hour distribution (out of {sample_size} games)')
    # plt.xlabel('Hour')
    # plt.ylabel('Frequency')
    # plt.show;

    #plot win rate over time
    #win rate = % of games which were my win
    #plot win rate over time for white
    #plot win rate over time for black
    #plot win rate for each hour of day (histogram?)
    #plot win rate for black vs white
    #plot black elo vs white elo
    fig24 = plt.figure()
    graph = plt.plot(chess_data['black_elo'], chess_data['white_elo'], '.',
                     figure=fig24,markersize=2, color = 'blue')
    plt.xlabel('Black elo')
    plt.ylabel('White elo')
    pdf.savefig(fig24)

    #plot win rate for each day of the week (bar chart?)
    # #plot my elo vs opponent elo
    # fig25 = plt.figure()
    # graph = plt.plot(chess_data['my_elo'], chess_data['opponent_elo'],
    #                  figure=fig25,'.', markersize=2, color = 'blue')
    # plt.xlabel('My elo')
    # plt.ylabel('Opponent elo')
    # pdf.savefig(fig25)

    pdf.close()
    return av_g_l, av_t, av_gpd, av_tpd, game_count


# analysis(chess_data, 'ubad00d')