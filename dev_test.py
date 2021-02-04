import activate_coins
import time, datetime
import sys, pathlib
import psutil
import re
import system_interaction.database_interaction as db
import mathematics.train_network as nn
import tensorflow as tf
import mathematics.calculations as cl
import mathematics.preprocess_data as pre
from tensorflow.keras.utils import plot_model

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


t_summary()