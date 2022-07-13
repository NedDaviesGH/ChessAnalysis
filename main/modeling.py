import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


#MODELLING#

def first_model(chess_data, username):

    pdf = matplotlib.backends.backend_pdf.PdfPages(f"Chess_first_model_{username}.pdf")

    X = chess_data[['black_elo']]
    y = chess_data.white_elo


    # In[58]:


    lr = LinearRegression()
    lr.fit(X,y)


    # In[59]:


    ic.ic(lr.intercept_)
    ic.ic(lr.coef_)


    # In[839]:


    # new_values = [[800], [1600], [1700], [200], [2000]]
    # lr.predict(new_values)


    # In[60]:


    lr.score(X,y) # returns R^2. Best possible score is 1.0


    # In[61]:


    plt.scatter(X, y, linewidths=1, alpha=0.5)
    plt.xlabel('Black ELO')
    plt.ylabel('White ELO')
    plt.plot(X, lr.predict(X), color='k')


    # In[ ]:

def second_model(chess_data, username):

    pdf = matplotlib.backends.backend_pdf.PdfPages(f"Chess_second_model_{username}.pdf")

    y_ = chess_data.result_numerical
    features = ['elo_difference', 'game_length_m', 'colour_numerical', 'Hour', 'Day', 'Day_in_month', 'game_id',
                'daily_game_count', 'daily_result_aggregate', 'time_since_last_game_m', 'Previous_result',
                'trigger_factor','time_since_last_game_m']
    X_ = chess_data[features]


    train_X, val_X, train_y, val_y = train_test_split(X_, y_)


    chess_model = DecisionTreeRegressor()
    chess_model.fit(train_X,train_y)

    val_predictions = chess_model.predict(val_X)

    validation_table = pd.DataFrame(val_y)
    validation_table['result_predictions'] = val_predictions
    validation_table.result_predictions = validation_table.result_predictions.apply(int)
    validation_table.reset_index()
    validation_table['Prediction_correct'] = validation_table.result_numerical == validation_table.result_predictions
    print(validation_table.Prediction_correct.value_counts())
    print(validation_table['result_numerical'].value_counts())
    print(validation_table['result_predictions'].value_counts())

    vtwl = validation_table[validation_table['result_numerical'] == 1].count()[1] # validation table win length
    mask_w = ((validation_table['result_numerical'] == 1) & (validation_table['Prediction_correct'] == True))
    cwc = validation_table[mask_w].sum()[0] #correct win count

    print('rate of correct win prediction:', cwc/vtwl)

    vtll = validation_table[validation_table['result_numerical'] == -1].count()[1] # validation table win length
    mask_l = ((validation_table['result_numerical'] == -1) & (validation_table['Prediction_correct'] == True))
    clc = validation_table[mask_l].sum()[1] #correct win count

    print('rate of correct loss prediction:', -clc/vtll)

    vtdl = validation_table[validation_table['result_numerical'] == 0].count()[1] # validation table draw length
    mask_d = ((validation_table['result_numerical'] == 0) & (validation_table['Prediction_correct'] == True))
    cdc = validation_table[mask_d].sum()[2] #correct draw count

    print('rate of correct draw prediction:', cdc/vtdl)

    mean_absolute_error(val_y, val_predictions)



    importance = chess_model.feature_importances_


    #correlation heatmap
    plt.figure(figsize=(20,10))
    c= chess_data.corr()
    sns.heatmap(c,cmap="BrBG",annot=True)
