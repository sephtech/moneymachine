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

    def __init__(self):

        #initilize database ineraction
        os.environ["TZ"] = "Europe/London"

        if self.checkRunning == False:
            self.startDatabase()
            print("Waiting for DB to come online...")
            time.sleep(5)
        
        self.db = MySQLdb.connect(host="localhost", user="root", db="coins")

    def checkRunning(self):

        for proc in psutil.process_iter():
            try:
                #check if process name contains the given name string.
                if "mysqld".lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False

    def startDatabase(self):

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

        #start database
        subprocess.Popen("".join((self.database_root_path_win, "\\bin\\mysqld")))
    
    def getDatabase(self):

        return self.db
    
    def getCoinData_Date_Open(self, coin):

        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM {};".format(coin))
        result = db_cursor.fetchall()
        timestamps = []

        print("Collecting data for coin {}...".format(coin))
        for index in tqdm.trange(len(result)):
            timestamps.append((result[index][1], result[index][4]))

        return timestamps

    def getCoinDataComplete(self, coin):

        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM {};".format(coin))
        result = db_cursor.fetchall()
        timestamps = []

        print("Collecting data for coin {}...".format(coin))
        for index in tqdm.trange(len(result)):
            timestamps.append((result[index][1], result[index][2], result[index][3], result[index][4], result[index][5], result[index][6]))

        return timestamps

    def getCoinDataPackage(self, coin):

        coinDataComplete = self.getCoinData_Date_Open(coin)
        day = self.__getCoinDataDay__(coin, coinDataComplete)
        week = self.__getCoinDataWeek__(coin, coinDataComplete)
        month = self.__getCoinDataMonth__(coin, coinDataComplete)
        year = self.__getCoinDataYear__(coin, coinDataComplete)

        return (day, week, month, year)

    def __getCoinDataDay__(self, coin, coinData):

        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevDay = timeNow - datetime.timedelta(days=1)
        dayData = []

        print("Generating day overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevDay and timestampDate <= timeNow:
                dayData.append(coinData[index])

        return dayData

    def __getCoinDataWeek__(self, coin, coinData):

        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevWeek = timeNow - datetime.timedelta(weeks=1)
        weekData = []

        datapoints = []
        for n in range(30, int((timeNow - timePrevWeek).days) * 24 * 60 + 30, 30):
            datapoints.append(timePrevWeek + datetime.timedelta(minutes=n))

        print("Generating week overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevWeek and timestampDate <= timeNow:
                for datapoint in datapoints:
                    if datapoint == timestampDate:
                        weekData.append(coinData[index])

        return weekData

    def __getCoinDataMonth__(self, coin, coinData):

        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevMonth = timeNow - relativedelta(months=1)
        monthData = []

        datapoints = []
        for n in range(2, int((timeNow - timePrevMonth).days) * 24 + 2, 2):
            datapoints.append(timePrevMonth + datetime.timedelta(hours=n))

        print("Generating month overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevMonth and timestampDate <= timeNow:
                for datapoint in datapoints:
                    if datapoint == timestampDate:
                        monthData.append(coinData[index])

        return monthData

    def __getCoinDataYear__(self, coin, coinData):

        timeNow = datetime.datetime.fromtimestamp(int(coinData[len(coinData)-1][0]))
        timePrevYear = timeNow - relativedelta(years=1)
        yearData = []

        datapoints = []
        for n in range(1, int((timeNow - timePrevYear).days + 1), 1):
            datapoints.append(timePrevYear + datetime.timedelta(days=n))

        print("Generating year overview for coin {}...".format(coin))
        for index in tqdm.trange(len(coinData)):
            timestampDate = datetime.datetime.fromtimestamp(int(coinData[index][0]))
            if timestampDate > timePrevYear and timestampDate <= timeNow:
                for datapoint in datapoints:
                    if datapoint == timestampDate:
                        yearData.append(coinData[index])

        return yearData

    def getSavedCoins(self):
        
        #execute database query
        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM versions;")
        result = db_cursor.fetchall()
        coins = []
        
        #put tables in list
        for x in result:
            if x[3] == "yes": 
                coins.append(x[1])

        return coins

    def updateAllCoins(self):

        coins = self.getSavedCoins()
        for coin in coins:
            self.updateCoin(coin)

    def updateCoin(self, coin):

        cb = coinbase_interaction.CoinbaseInteraction()

        db_cursor = self.db.cursor()
        db_cursor.execute("SELECT * FROM versions WHERE coin='{}';".format(coin))
        result = db_cursor.fetchall()

        for i in result:
            if i[2] == "0":
                missingValues = cb.getMissingCoinData(coin, 0)
            else: 
                missingValues = cb.getMissingCoinData(coin, i[2])

        print("Writing missing values of coin {} into database...".format(coin))
        for index in tqdm.trange(len(missingValues)):

            if index == len(missingValues) - 1:
                current_coin_version = missingValues[index][0]
            else:
                current_coin_version = None
            db_cursor.execute(f"INSERT INTO {coin}(date, low, high, open, close, volume) VALUES('{missingValues[index][0]}', '{missingValues[index][1]}', '{missingValues[index][2]}', '{missingValues[index][3]}', '{missingValues[index][4]}', '{missingValues[index][5]}');")

        self.db.commit()
        self.__writeCoinVersion__(coin, current_coin_version)

    def __writeCoinVersion__(self, coin, version):

        if version:
            db_cursor = self.db.cursor()
            db_cursor.execute("SELECT * FROM versions WHERE coin='{}';".format(coin))
            result = db_cursor.fetchall()

            if not result:
                db_cursor.execute("INSERT INTO versions(coin, version, active) VALUES('{}', '{}', '{}');".format(coin, version, "no"))
            else:
                db_cursor.execute("UPDATE versions SET version='{}' WHERE coin='{}';".format(version, coin))

            self.db.commit()