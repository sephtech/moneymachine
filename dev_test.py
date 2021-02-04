import activate_coins
import time, datetime
import sys, pathlib
import psutil
import re
import system_interaction.database_interaction as db
import mathematics.train_network as nn
import tensorflow as tf
import mathematics.calculations as cl
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
        "C:\\Users\\birkle.SEPHTECH\\Documents\\GitHub\\moneymachine\\models\\checkpoints\\RNN_Model_Final-08-nan.model", custom_objects=None, compile=True, options=None
    )   

    model.summary()
    plot_model(model, to_file="C:\\Users\\birkle.SEPHTECH\\Documents\\GitHub\\moneymachine\\models\\checkpoints\\RNN_Model_Final-08-nan.png")

def t_calculation():
    '''
    Test calculation class
    '''
    activate_coins.__updateNewCoins__(False, )
    calc = cl.Calculations()
    print(calc.predictValue("btc", 60, 72))
    #calc.getGraphAbsoluteData("btc")

t_calculation()