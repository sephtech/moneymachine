import pathlib
import sys
import re
import distutils.dir_util as dirutil
import shutil
import glob, os
import system_interaction.database_interaction as database
import mathematics.train_network as train

def activateCoins():
    '''
    Method to activate new coins in the coins.conf file
    Will download all necessary data into the database
    Will create new lstm networks for every coin to predict future prices

    Can also be used to update all persistent coins
    '''

    #wait for user confirmation to start
    __waitForConfirmation__()

    #creates new database session
    databaseInteraction = database.DatabaseInteraction()
    db = databaseInteraction.getDatabase()

    #downloads and creates new coins
    print("Download and save new coins...")
    newCoins = __updateNewCoins__(True, db, databaseInteraction)
    #updates all coins
    print("Update all coins...")
    __updateNewCoins__(False, db, databaseInteraction)
    databaseInteraction.updateAllCoins()

    #only execute if there are new coins
    #if newCoins:
    print("Train models for every coin with new data...")
    __trainNewModels__()

        #activates the coins in the database
    #    for coin in newCoins:
    #        __setCoinActive__(coin)

    print("Done... Restart app!")

def __waitForConfirmation__():
    '''
    Method to wait for the user confirmation before continueing
    '''

    print()
    print("This process will need a lot of time!")
    print("ca. 4h per coin in coins.conf")
    print("Cancel if you dont have the time!")
    print("Dont shutdown PC if you proceed!")
    input()

def __getDefindedCoins__():
    '''
    Reads all coins defined in the coins.conf

    retrun -> collection of defined coins
    '''

    with open("coins.conf") as file:
        lines = file.readlines()
        coins = []
        for line in lines:
            #do not parse comment lines
            if not re.search("#", line):
                line = re.sub("\n", "", line)
                coins.append(line)

    return coins

def __createNewCoins__(db, databaseInteraction):
    '''
    Creates new Tables in the database for the new coins
    If version of coin in version table is set to 0 - truncate the coin table

    param db                  -> database instance
    param databaseInteraction -> database interaction instance

    return -> list of new coins
    '''

        #gets the coins that alread exist
        existingCoins= databaseInteraction.getSavedCoins()
        #gets the defined coins
        definedCoins = __getDefindedCoins__()
        newCoins = []

        for definedCoin in definedCoins:
            if not definedCoin in existingCoins:
                
                #only create or truncate table if coin is not in use
                newCoins.append(definedCoin)
                #writes new version of the coin to 0
                databaseInteraction.__writeCoinVersion__(definedCoin, "0")
                db_curser = db.cursor()
                db_curser.execute("CREATE TABLE IF NOT EXISTS {}(id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(20), low VARCHAR(20), high VARCHAR(20), open VARCHAR(20), close VARCHAR(20), volume VARCHAR(20));".format(definedCoin))
                db_curser.execute("TRUNCATE TABLE {};".format(definedCoin))
            
        db.commit()
        return newCoins

def __updateNewCoins__(create, db, databaseInteraction):
    '''
    Updates new created or all coins

    param create              -> boolean(True: update only new coins)
    param db                  -> database instance
    param databaseInteraction -> database interaction instance
    '''

    if create == True:
        #only create and update new coins
        newCoins = __createNewCoins__(db, databaseInteraction)
    for coin in __getDefindedCoins__():
        #updates all coins
        databaseInteraction.updateCoin(coin)

def __setCoinActive__(db, coin):
    '''
    Sets coin in database to active so it can be used
    
    param coin -> name of coin to be set active
    '''

    #performs the quary
    db_cursor = db.cursor()
    db_cursor.execute("UPDATE versions SET active='yes' WHERE coin='{}';".format(coin))
    dv.commit()

def __trainNewModels__():
    '''
    Trains the new models for all coins in the database
    '''

    #get defined coins from coins.conf
    coins = __getDefindedCoins__()
    #sets all different future periods
    future_periods = [72]
    #sets all seqence lengths for the future periods
    seq_lens = [60]
    
    #walk through all future periods and create the models for them
    for i in range(0, len(future_periods)):

        #create a own model for every coin
        for coin in coins:
            trainer = train.NetworkTraining(seq_len=seq_lens[i], future_period=future_periods[i])
            trainer.startTraining(coin)
            #save the newest model in the models folder
            __saveModel__(coin, future_periods[i])

def __saveModel__(coin, future_period):
    '''
    Saves the latest model and the latest scaler data file to the models folder
    Deletes models which are already there

    param future_period -> steps into future for the predictions
    '''

    #creates the root dir variable
    root_dir = pathlib.Path(__file__).parent.absolute()
    #searches for the newest model and scaler date in the right category
    list_of_files = glob.glob(f"{root_dir}\\models\\checkpoints\\{coin}*.model")
    latest_model = max(list_of_files, key=os.path.getctime)
    list_of_files = glob.glob(f"{root_dir}\\models\\checkpoints\\{coin}_scaler_data_*.txt")
    latest_scaler = max(list_of_files, key=os.path.getctime)

    #create new filenames for the model and the scaler data
    model_file = re.sub("checkpoints.*", "PLACEHOLDER.model", latest_model)
    model_file = re.sub("PLACEHOLDER", f"{coin}_{future_period}", model_file)
    scaler_file = re.sub("checkpoints.*", "PLACEHOLDER.scaler", latest_scaler)
    scaler_file = re.sub("PLACEHOLDER", f"{coin}_{future_period}", scaler_file)
    
    #copy the files
    shutil.copy(latest_scaler, scaler_file)
    dirutil.copy_tree(latest_model, model_file)