import os
import pathlib
import re
import psutil, time
import subprocess
import MySQLdb
import system_interaction.coinbase_interaction as coinbase_interaction
import tqdm
import datetime
from dateutil.relativedelta import *

class DatabaseInteraction():
    '''
    Class for the interaction with the mysql database
    '''

    def __init__(self):
        '''
        Constuctor for the database interaction class
        Connects to database
        '''

        #sets the timezone to UTC
        os.environ["TZ"] = "Europe/London"

        #checks if mysqld process is already running
        status = self.checkRunning()
        if not status:
            #starts the database
            self.startDatabase()
            print("Waiting for DB to come online...")
            time.sleep(5)
        
        #initilize database connection
        self.db = MySQLdb.connect(host="localhost", user="root", db="coins")

    def checkRunning(self):
        '''
        Checks if the mysqld process is already running

        return -> boolean (False = not running)
        '''

        for proc in psutil.process_iter():
            try:
                #check if process name contains the given name string.
                if "mysqld".lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False

    def startDatabase(self):
        '''
        Starts up the database
        '''

        #get paths for the database folders
        self.database_root_path_win = pathlib.Path(__file__).parent.parent.absolute()
        self.database_root_path_win = "".join((str(self.database_root_path_win), "\\database"))
        self.database_root_path_win = self.database_root_path_win.replace("c:\\", "C:\\")
        self.database_root_path_unix = self.database_root_path_win.replace("\\", "/")
        self.database_data_path_unix = "".join((self.database_root_path_unix, "/data"))

        #set correct paths in the mysql configuration file
        with open("".join((self.database_root_path_win + "\\my.ini")), 'r') as file :
            filedata = file.read()
            filedata = re.sub("basedir=\\S*", "".join(("basedir=", self.database_root_path_unix)), filedata)
            filedata = re.sub("datadir=\\S*", "".join(("datadir=", self.database_data_path_unix)), filedata)
        
        with open("".join((self.database_root_path_win + "\\my.ini")), 'w') as file :
            file.write(filedata)

        #starts database
        subprocess.Popen("".join((self.database_root_path_win, "\\bin\\mysqld")))
    
    def getDatabase(self):
        '''
        Returns the database object

        return -> database object
        '''

        return self.db
    
    def getCoinData_Date_Open(self, coin):
        '''
        Returns the complete time series of opening prices of specific coin

        param coin -> name of coin to get the data for

        return -> collection of all timestamps with the opening prices
        '''

        #selection every entry from the coin table
        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM {};".format(coin))
        result = db_cursor.fetchall()
        timestamps = []

        #appends opening prices the data to a list
        print("Collecting data for coin {}...".format(coin))
        for index in tqdm.trange(len(result)):
            timestamps.append((result[index][1], result[index][4]))

        return timestamps

    def getCoinDataComplete(self, coin):
        '''
        Returns the complete time series of every information of specific coin

        param coin -> name of coin to get the data for

        return -> collection of all timestamps with every information
        '''

        #selection every entry from the coin table
        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM {};".format(coin))
        result = db_cursor.fetchall()
        timestamps = []

        #appends every information the data to a list
        print("Collecting data for coin {}...".format(coin))
        for index in tqdm.trange(len(result)):
            timestamps.append((result[index][1], result[index][2], result[index][3], result[index][4], result[index][5], result[index][6]))

        return timestamps

    def getCoinDataPackage(self, coin):
        '''
        Generates set of time series data to create different graphs

        param coin -> name of coin to generate set of data for

        return (
            day   -> collection of price information of the past day
            week  -> collection of price information of the past week
            month -> collection of price information of the past month
            year  -> collection of price information of the past yeary
        )
        '''

        #gets the complete table of the database
        coinDataComplete = self.getCoinData_Date_Open(coin)
        #separates data for the past day
        day = self.__getCoinDataDay__(coin, coinDataComplete)
        #separates data for the past week
        week = self.__getCoinDataWeek__(coin, coinDataComplete)
        #separates data for the past month
        month = self.__getCoinDataMonth__(coin, coinDataComplete)
        #separates data for the past year
        year = self.__getCoinDataYear__(coin, coinDataComplete)

        return (day, week, month, year)

    def __getCoinDataDay__(self, coin, coinData):
        '''
        Extracts the relevant data of the last day from a complete data set

        param coin     -> name of coin to extract data for
        param coinData -> complete data set of the coin data

        return -> relevant data of the coin for the last day
        '''

        #gets the current date an calculates the timedelta
        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevDay = timeNow - datetime.timedelta(days=1)
        dayData = []

        #runs through the complete data and collects the data which is in the timedelta range
        print("Generating day overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevDay and timestampDate <= timeNow:
                dayData.append(coinData[index])

        return dayData

    def __getCoinDataWeek__(self, coin, coinData):
        '''
        Extracts the relevant data of the last week from a complete data set

        param coin     -> name of coin to extract data for
        param coinData -> complete data set of the coin data

        return -> relevant data of the coin for the last week
        '''

        #gets the current date an calculates the timedelta
        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevWeek = timeNow - datetime.timedelta(weeks=1)
        weekData = []

        #calculates timesteps to extract relevant data from
        datapoints = []
        for n in range(30, int((timeNow - timePrevWeek).days) * 24 * 60 + 30, 30):
            datapoints.append(timePrevWeek + datetime.timedelta(minutes=n))

        #runs through the complete data and collects the data which is in the timedelta range
        print("Generating week overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevWeek and timestampDate <= timeNow:
                for datapoint in datapoints:
                    if datapoint == timestampDate:
                        weekData.append(coinData[index])

        return weekData

    def __getCoinDataMonth__(self, coin, coinData):
        '''
        Extracts the relevant data of the last month from a complete data set

        param coin     -> name of coin to extract data for
        param coinData -> complete data set of the coin data

        return -> relevant data of the coin for the last month
        '''

        #gets the current date an calculates the timedelta
        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevMonth = timeNow - relativedelta(months=1)
        monthData = []

        #calculates timesteps to extract relevant data from
        datapoints = []
        for n in range(2, int((timeNow - timePrevMonth).days) * 24 + 2, 2):
            datapoints.append(timePrevMonth + datetime.timedelta(hours=n))

        #runs through the complete data and collects the data which is in the timedelta range
        print("Generating month overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevMonth and timestampDate <= timeNow:
                for datapoint in datapoints:
                    if datapoint == timestampDate:
                        monthData.append(coinData[index])

        return monthData

    def __getCoinDataYear__(self, coin, coinData):
        '''
        Extracts the relevant data of the last year from a complete data set

        param coin     -> name of coin to extract data for
        param coinData -> complete data set of the coin data

        return -> relevant data of the coin for the last year
        '''

        #gets the current date an calculates the timedelta
        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevYear = timeNow - relativedelta(years=1)
        yearData = []

        #calculates timesteps to extract relevant data from
        datapoints = []
        for n in range(1, int((timeNow - timePrevYear).days + 1), 1):
            datapoints.append(timePrevYear + datetime.timedelta(days=n))

        #runs through the complete data and collects the data which is in the timedelta range
        print("Generating year overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevYear and timestampDate <= timeNow:
                for datapoint in datapoints:
                    if datapoint == timestampDate:
                        yearData.append(coinData[index])

        return yearData

    def getSavedCoins(self):
        '''
        Retruns all active coins saved in the database

        return -> array with all coins in the database
        '''
        
        #execute database query
        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM versions;")
        result = db_cursor.fetchall()
        coins = []
        
        #put coins in list
        for x in result:
            
            #only append active coins
            if x[3] == "yes": 
                coins.append(x[1])

        return coins

    def updateAllCoins(self):
        '''
        Updates all active coins in the database one after another
        '''

        #gets present coins
        coins = self.getSavedCoins()
        #starts update cyclus for coin
        for coin in coins:
            self.updateCoin(coin)

    def updateCoin(self, coin):
        '''
        Updates specific coin in the database

        param coin -> name of the coin to update
        '''

        #establish coinbase connection
        cb = coinbase_interaction.CoinbaseInteraction()

        #selects the version information in the database
        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM versions WHERE coin='{}';".format(coin))
        result = db_cursor.fetchall()

        for i in result:
            if i[2] == "0":
                #if no data is in database collect everything
                missingValues = cb.getMissingCoinData(coin, 0)
            else:
                #if data is in database collect only newer than newest version of present data
                missingValues = cb.getMissingCoinData(coin, i[2])

        #only write data if there is something to write
        if len(missingValues) > 0:
            print("Writing missing values of coin {} into database...".format(coin))
            for index in tqdm.trange(len(missingValues)):

                #sets a variable for the new coin verision in the database
                if index == len(missingValues) - 1:
                    current_coin_version = missingValues[index][0]
                else:
                    current_coin_version = None
                #inserts the new data row into the database
                db_cursor.execute(f"INSERT INTO {coin}(date, low, high, open, close, volume) VALUES('{missingValues[index][0]}', '{missingValues[index][1]}', '{missingValues[index][2]}', '{missingValues[index][3]}', '{missingValues[index][4]}', '{missingValues[index][5]}');")

            self.db.commit()
            #writes new coin version to database
            self.__writeCoinVersion__(coin, current_coin_version)

    def __writeCoinVersion__(self, coin, version):
        '''
        Writes given coin version to database

        param coin    -> name of coin to write version
        param version -> new version to write into the database
        '''

        # only write version if it is present
        if version:
            db_cursor = self.db.cursor()
            db_cursor.execute("SELECT * FROM versions WHERE coin='{}';".format(coin))
            result = db_cursor.fetchall()

            #if version is not present write new one
            if not result:
                db_cursor.execute("INSERT INTO versions(coin, version, active) VALUES('{}', '{}', '{}');".format(coin, version, "no"))
            else:
                db_cursor.execute("UPDATE versions SET version='{}' WHERE coin='{}';".format(version, coin))

            self.db.commit()