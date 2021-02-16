import activate_coins
import time, datetime
import sys, pathlib
import psutil
import re
import tqdm, numpy
import system_interaction.database_interaction as db
import system_interaction.coinbase_interaction as cb
import mathematics.train_network as nn
import tensorflow as tf
import mathematics.calculations as cl
import mathematics.preprocess_data as pre
from tensorflow.keras.utils import plot_model
from sklearn import preprocessing as pp

def t_database():
    '''
    Start up the database
    '''
    
    test = db.DatabaseInteraction()

def t_activate():
    '''
    Start the coin activation 
    '''

    activate_coins.activateCoins()

def t_summary():
    '''
    Creates summary of model
    '''

    model = tf.keras.models.load_model(
        "C:\\Users\\birkle.SEPHTECH\\Documents\\GitHub\\moneymachine\\models\\btc_72.model", custom_objects=None, compile=True, options=None
    )   

    print(model.summary())
    #plot_model(model, to_file="C:\\Users\\birkle.SEPHTECH\\Documents\\GitHub\\moneymachine\\models\\checkpoints\\btc_72.png")

def t_calculation():
    '''
    Test calculation class
    '''
    activate_coins.__updateNewCoins__(False, )
    calc = cl.Calculations()
    print(calc.predictValue("btc", 60, 72))
    #calc.getGraphAbsoluteData("btc")

def t_preprocess():
    '''
    Test preprocessing
    '''

    pp = pre.Preprocessing("btc",60,72,0.05,0.2)
    df = pp.__getRawData__()
    df = pp.__shiftData__(df)
    train, val, test = pp.__splitData__(df)
    pp.__preprocess__(train)

def t_days_pred():

    dbi = db.DatabaseInteraction()
    dbi.updateAllCoins()

    coins = ("btc", "eth", "ltc")
    future_period = 72
    seq_len = 60

    #cbi = cb.CoinbaseInteraction()

    start_DSTR = "20210205000000"
    #end_DSTR = "20210214000000"
    start_Date = datetime.datetime.strptime(start_DSTR, "%Y%m%d%H%M%S")
    #end_Date = datetime.datetime.strptime(end_DSTR, "%Y%m%d%H%M%S")
    dates = []
    for n in range(10):
            dates.append(start_Date + datetime.timedelta(days=n))

    print(dates)

    
    for coin in coins:

        #getting raw data from database
        processing = pre.Preprocessing(None, None, None, None, None)
        raw = processing.__getRawData__()
        raw.dropna(inplace=True)

        '''
        results = []
        for dt in dates:

            test = raw[(raw.index == str(int(dt.timestamp())))][f"{coin}_open"].values[0]
            results.append(test)

        '''
        #shift data
        raw['future'] = raw[f"{coin}_open"].shift(-future_period)

        #scales all columns and saves the scaler for inverse transformation
        scaler = pp.MinMaxScaler()
        print("Scale data...")
        for col in tqdm.trange(len(raw.columns)):

            raw[raw.columns[col]] = raw[raw.columns[col]].astype(float)
            raw.dropna(inplace=True)
            raw[raw.columns[col]] = scaler.fit_transform(raw[raw.columns[col]].values.reshape(-1,1))
            
            if raw.columns[col] == "future":
                retrunScaler = scaler

        raw.drop(["future"], 1, inplace=True)
        raw.dropna(inplace=True)

        #sorts the data and uses the newest ones
        times = sorted(raw.index.values)
        sequences = []
        for dte in dates:
            seconds = dte.timestamp()
            for timestamp in times:
                if float(timestamp) == seconds:
                    sequences.append(str(int(timestamp) - (seq_len*300)))
                    break
            
        print(sequences)
        results = []

        for last_times in sequences:
            predict_df = raw[(raw.index >= last_times)]
            predict_df = predict_df[(predict_df.index < str(int(last_times) + (seq_len*300)))]
            predict_df = numpy.array(predict_df)
            predict_array = numpy.array(predict_df)

            #generate path of the model folder
            modelpath = pathlib.Path(__file__).parent.absolute()
            modelpath = f"{modelpath}\\models\\{coin}_{future_period}.model"
            print(modelpath)
            
            #load the model
            model = tf.keras.models.load_model(modelpath, custom_objects=None, compile=True, options=None)
            
            #getting newest sequence and predict th future value
            predictionData = predict_array
            scaler = retrunScaler
            predictionData = [predictionData]
            predictionData = numpy.array(predictionData)
            predictedValue = model.predict(predictionData)

            #scale the future value inverse
            returnValue = scaler.inverse_transform(predictedValue)
            results.append(returnValue[0][0])

        print(coin)
        print(len(results))
        for i in results:
            print(i)

t_days_pred()