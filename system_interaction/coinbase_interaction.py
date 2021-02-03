import cbpro
import re
import tqdm
import os, time
from datetime import date, timedelta, datetime

#start time of coin value registration set to 2015/01/01
global_coin_start_time = "2015-01-01T00:00:00"
granularity = 300

class CoinbaseInteraction():

    def __init__(self):

        #initialize coinbase connection
        os.environ["TZ"] = "Europe/London"
        self.client = cbpro.PublicClient()

    def getCoinVersion(self, coin):

        todayDate = datetime.today()
        todayDay = datetime.strftime(todayDate, "%Y-%m-%dT%H:%M:%S")
        todayStart = re.sub("\\d\\d:\\d\\d:\\d\\d", "00:00:00", todayDay)
        todayEnd = re.sub("\\d\\d:\\d\\d:\\d\\d", "23:55:00", todayDay)

        todayCoinInfo =  self.client.get_product_historic_rates("".join((coin, "-USD")), start=todayStart, end=todayEnd, granularity=granularity)
        return todayCoinInfo[0][0]

    def getMissingCoinData(self, coin, lastPresentVersion):

        if lastPresentVersion == 0:

            secondsLastVersion = 0
            day = global_coin_start_time
            dayDate = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S")

        else:

            #get the unix seconds of the last present version of the coin for comparison
            secondsLastVersion = self.client.get_product_historic_rates("".join((coin, "-USD")), start=lastPresentVersion, end=lastPresentVersion, granularity=granularity)
            secondsLastVersion = secondsLastVersion[0][0]
            
            day = datetime.strftime(todayDate, "%Y-%m-%dT%H:%M:%S")
            day = re.sub("\\d\\d:\\d\\d:\\d\\d", "00:00:00", day)
            dayDate = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S")

        todayDate = datetime.today()
        missingCoinData = []

        dates = self.__daterange__(dayDate, todayDate)
        print("Downloading missing values of coin {}...".format(coin))
        for index in tqdm.trange(len(dates)):
            dates[index] = datetime.strftime(dates[index], "%Y-%m-%dT%H:%M:%S")
            missingDayData = self.__getCoinDayData__(coin, dates[index])
            if not missingDayData:
                continue
            
            for index in reversed(range(0, len(missingDayData))):
                missingCoinData.append(missingDayData[index])

        returnCoinData = []
        if secondsLastVersion != 0:
            for timestamp in missingCoinData:
                if int(timestamp[0]) > secondsLastVersion:
                    returnCoinData.append(timestamp)
        else:
            returnCoinData = missingCoinData

        return returnCoinData

    def __getCoinDayData__(self, coin, day):

        time.sleep(0.3)
        endday = re.sub("T00:00", "T23:55", day)
        return self.client.get_product_historic_rates("".join((coin, "-USD")), start=day, end=endday, granularity=granularity)

    def __daterange__(self, startDate, endDate):

        dates = []
        for n in range(int ((endDate - startDate).days)+1):
            dates.append(startDate + timedelta(n))

        return dates