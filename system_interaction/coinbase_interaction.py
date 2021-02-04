import cbpro
import re
import tqdm
import os, time
from datetime import date, timedelta, datetime

#start time of coin value registration set to 2015/01/01
global_coin_start_time = "2015-01-01T00:00:00"
#time steps in data (in seconds)
granularity = 300

class CoinbaseInteraction():
    '''
    Class for the interaction with the coinbase pro API
    '''

    def __init__(self):
        '''
        Constructor for the coinbase interaction class
        Sets the timeszone to UTC and opens a connection
        '''

        #initialize coinbase connection
        os.environ["TZ"] = "Europe/London"
        self.client = cbpro.PublicClient()

    def getCoinVersion(self, coin):
        '''
        Returns the latest timestamp available in the API

        param coin -> coin name to get timestamp from

        return -> timestamp of the last available data set
        '''

        #configures the searching date strings for the API
        #always between 00:00 and 23:55
        todayDate = datetime.today()
        todayDay = datetime.strftime(todayDate, "%Y-%m-%dT%H:%M:%S")
        todayStart = re.sub("\\d\\d:\\d\\d:\\d\\d", "00:00:00", todayDay)
        todayEnd = re.sub("\\d\\d:\\d\\d:\\d\\d", "23:55:00", todayDay)

        #perform API call
        todayCoinInfo =  self.client.get_product_historic_rates("".join((coin, "-USD")), start=todayStart, end=todayEnd, granularity=granularity)
        return todayCoinInfo[0][0]

    def getMissingCoinData(self, coin, lastPresentVersion):
        '''
        Collects all missing data from the API

        param coin               -> name of coin to collect data for
        param lastPresentVersion -> unix timestamp of the last present row in the database

        return -> missing coin data in array
        '''

        #gets present date
        todayDate = datetime.today()
        if int(lastPresentVersion) == 0:
            
            #if no value available in database collect all date from global start time
            secondsLastVersion = 0
            day = global_coin_start_time
            #sets the start date to the global start time
            dayDate = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S")

        else:

            #if values are available in the database set start date to last present date in database
            day = datetime.fromtimestamp(lastPresentVersion)
            day = datetime.strftime(day, "%Y-%m-%dT%H:%M:%S")
            day = re.sub("\\d\\d:\\d\\d:\\d\\d", "00:00:00", day)
            dayDate = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S")

        missingCoinData = []

        #calculates dates to collect values for
        dates = self.__daterange__(dayDate, todayDate)
        print("Downloading missing values of coin {}...".format(coin))
        for index in tqdm.trange(len(dates)):

            #collects data from API in steps of days
            dates[index] = datetime.strftime(dates[index], "%Y-%m-%dT%H:%M:%S")
            missingDayData = self.__getCoinDayData__(coin, dates[index])

            #continues if date is not available in API
            if not missingDayData:
                continue
            
            #reverses the gathered dates to start with the oldes date
            for index in reversed(range(0, len(missingDayData))):
                missingCoinData.append(missingDayData[index])

        #deletes data which is already present
        returnCoinData = []
        if int(lastPresentVersion) != 0:
            for timestamp in missingCoinData:
                if int(timestamp[0]) > int(lastPresentVersion):
                    returnCoinData.append(timestamp)
        else:
            returnCoinData = missingCoinData

        return returnCoinData

    def __getCoinDayData__(self, coin, day):
        '''
        Collects all data of a specific date from the API

        param coin -> name of coin to collect data for
        param day  -> day to collect data from

        return -> data set of the date
        '''

        #waits for a while because the API can only handle three requests per minute
        time.sleep(0.3)
        #generates the end time
        endday = re.sub("T00:00", "T23:55", day)
        return self.client.get_product_historic_rates("".join((coin, "-USD")), start=day, end=endday, granularity=granularity)

    def __daterange__(self, startDate, endDate):
        '''
        Generates all days between start and end date

        param startDate -> date to start the collection from
        param endDate   -> date the end the collection

        return -> list with all days in the range
        '''

        dates = []
        for n in range(int ((endDate - startDate).days)+1):
            dates.append(startDate + timedelta(n))

        return dates