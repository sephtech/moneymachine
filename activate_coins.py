import pathlib
import sys
import re
import distutils.dir_util as dirutil
import shutil
import glob, os
import system_interaction.database_interaction as database
import mathematics.train_network as train

def activateCoins():

    __waitForConfirmation__()

    databaseInteraction = database.DatabaseInteraction()
    db = databaseInteraction.getDatabase()

    print("Download and save new coins...")
    newCoins = __updateNewCoins__(True, db, databaseInteraction)
    print("Update all coins...")
    __updateNewCoins__(False, db, databaseInteraction)
    databaseInteraction.updateAllCoins()

    print("Train models for every coin with new data...")
    __trainNewModels__()

    for coin in newCoins:
        __setCoinActive__(coin)

    print("Done... Restart app!")

def __waitForConfirmation__():

    print("This process will need a lot of time!")
    print("ca. 4h per coin in coins.conf")
    print("Cancel if you dont have the time!")
    print("Dont shutdown PC if you proceed!")
    input()

def __getDefindedCoins__():

    with open("coins.conf") as file:
        lines = file.readlines()
        coins = []
        for line in lines:
            if not re.search("#", line):
                line = re.sub("\n", "", line)
                coins.append(line)

    return coins

def __createNewCoins__(db, databaseInteraction):

        existingCoins= databaseInteraction.getSavedCoins()
        definedCoins = __getDefindedCoins__()
        newCoins = []

        for definedCoin in definedCoins:
            if not definedCoin in existingCoins:
                
                newCoins.append(definedCoin)
                databaseInteraction.__writeCoinVersion__(definedCoin, "0")
                db_curser = db.cursor()
                db_curser.execute("CREATE TABLE IF NOT EXISTS {}(id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(20), low VARCHAR(20), high VARCHAR(20), open VARCHAR(20), close VARCHAR(20), volume VARCHAR(20));".format(definedCoin))
                db_curser.execute("TRUNCATE TABLE {};".format(definedCoin))
            
        db.commit()
        return newCoins

def __updateNewCoins__(create, db, databaseInteraction):

    if create == True:
        newCoins = __createNewCoins__(db, databaseInteraction)
    for coin in __getDefindedCoins__():
        databaseInteraction.updateCoin(coin)

def __setCoinActive__(db, coin):

    db_cursor = db.cursor()
    db_cursor.execute("UPDATE versions SET active='yes' WHERE coin='{}';".format(coin))
    dv.commit()

def __trainNewModels__():

    #coins = __getDefindedCoins__()
    coins = ["btc"]
    seq_lens = [120]
    future_periods = [288]
    
    for i in range(0, len(seq_lens)):

        for coin in coins:

            trainer = train.NetworkTraining(seq_len=seq_lens[i], future_period=future_periods[i])
            trainer.startTraining(coin)
            __saveModel__(coin, future_periods[i])

def __saveModel__(coin, future_period):

    root_dir = pathlib.Path(__file__).parent.absolute()
    list_of_files = glob.glob(f"{root_dir}\\models\\checkpoints\\{coin}*.model")
    latest_model = max(list_of_files, key=os.path.getctime)
    list_of_files = glob.glob(f"{root_dir}\\models\\checkpoints\\{coin}_scaler_data_*.txt")
    latest_scaler = max(list_of_files, key=os.path.getctime)

    model_file = re.sub("checkpoints.*", "PLACEHOLDER.model", latest_model)
    model_file = re.sub("PLACEHOLDER", f"{coin}_{future_period}", model_file)
    scaler_file = re.sub("checkpoints.*", "PLACEHOLDER.scaler", latest_scaler)
    scaler_file = re.sub("PLACEHOLDER", f"{coin}_{future_period}", scaler_file)
    
    shutil.copy(latest_scaler, scaler_file)
    dirutil.copy_tree(latest_model, model_file)