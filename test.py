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

def tDB():
    
    test = db.DatabaseInteraction()

def tnn():

    activate_coins.activateCoins()

def tord():
    tm = datetime.datetime.strptime("2021-08-22T06:30:00", "%Y-%m-%dT%H:%M:%S")
    print(tm.timestamp())

def test():

    path = sys.path
    root_path = pathlib.Path(__file__).parent.absolute()
    sys.path.append(f"{root_path}\\installation_files\\cudnn-10.1-windows10-x64-v7.6.5.32\\bin")

def tsum():

    model = tf.keras.models.load_model(
        "C:\\Users\\birkle.SEPHTECH\\Documents\\GitHub\\moneymachine\\models\\checkpoints\\RNN_Model_Final-08-nan.model", custom_objects=None, compile=True, options=None
    )   

    model.summary()
    plot_model(model, to_file="C:\\Users\\birkle.SEPHTECH\\Documents\\GitHub\\moneymachine\\models\\checkpoints\\RNN_Model_Final-08-nan.png")

def trun():

    for proc in psutil.process_iter():
        try:
            #check if process name contains the given name string.
            if "mysqld".lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False

def tcalc():

    calc = cl.Calculations()
    print(calc.predictValue("btc", 60, 72))
    #calc.getGraphAbsoluteData("btc")

def tsave():

    activate_coins.__saveModel__("btc", 288)

tnn()