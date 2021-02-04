import system_interaction.database_interaction as database
import activate_coins
import pandas
import os
import json, time, pathlib
import datetime
import numpy
import tqdm
import random
from sklearn import preprocessing as pp
from collections import deque

class Preprocessing():
    '''
    Class for the preprocessing of data to feed an lstm network
    Data will be extracted from database
    '''

    def __init__(self, ratio, seq_len, future_period, validation_pct, test_pct):
        '''
        Constructor for preprocessing class
        Sets instance variables

        param ratio             -> name of coin to predict
        param seq_len           -> length of secquences of data
        param future_period     -> distance of prediction value in 5 minutes steps
        param validation_pct    -> percentage of validation data (from train data)
        param test_pct          -> percentage of test data (from whole data)
        '''

        self.ratio = ratio
        self.seq_len = seq_len
        self.future_period = future_period
        self.validation_pct = validation_pct
        self.test_pct = test_pct

        #sets warnigs for chain assingnment to false
        pandas.set_option('mode.chained_assignment', None)

    def __getRawData__(self):
        '''
        Method for getting raw data from database
        Data will be combined to one data frame

        return -> created data frame
        '''

        #establish connection to database
        dbi = database.DatabaseInteraction()
        db = dbi.getDatabase()
        #get coins defined in conf file
        coins = activate_coins.__getDefindedCoins__()

        main_df = pandas.DataFrame()
        print("Collect raw data...")
        for coin in tqdm.trange(len(coins)):
            
            #get data from database and store it in data frame
            df = pandas.read_sql_query(f"SELECT * FROM {coins[coin]};", db)
            df.drop(["id"], 1, inplace=True)
            df.rename(columns={"date": "time", "low": f"{coins[coin]}_low", "high": f"{coins[coin]}_high", "open": f"{coins[coin]}_open", "close": f"{coins[coin]}_close", "volume": f"{coins[coin]}_volume"}, inplace=True)

            #set index of data frame to time
            df.set_index("time", inplace=True)

            #joins all data of every coin together
            if len(main_df.columns) == 0:
                main_df = df
            else:
                main_df = main_df.join(df)
        
        #fills nan values and drops persistent nan
        main_df.fillna(method="ffill", inplace=True)
        main_df.dropna(inplace=True)

        return main_df

    def __shiftData__(self, df):
        '''
        Shifts label data in a given period of time

        param df -> data frame with raw data

        return -> data frame with shifted label data
        '''

        df['future'] = df[f"{self.ratio}_open"].shift(-self.future_period)
        return df

    def __splitData__(self, df):
        '''
        Splits data of given data fram into:
        Training data, Validation data, Test data

    	param df -> data fram with shifted data

        return train_df  -> data frame with training data
        return val_df    -> data frame with validation data
        return test_data -> data frame with test data
        '''

        #sort values
        times = sorted(df.index.values)
        last_times_test = times[-int(self.test_pct * len(times))]

        #splits train and test data into different data frames
        test_df = df[(df.index >= last_times_test)]
        main_df = df[(df.index < last_times_test)]

        #sort values again
        times_2 = sorted(main_df.index.values)
        last_times_val = times_2[-int(self.validation_pct * len(times_2))]

        #splits train and validation data into different data frames
        val_df = main_df[(main_df.index >= last_times_val)]
        train_df = main_df[(main_df.index < last_times_val)]

        return train_df, val_df, test_df

    def __preprocess__(self, df):
        '''
        Preprocesses the data. Contains:
        Scaling, Sequencing, Balancing

        param df -> data fram with one of the splitted data

        return x -> sequence collection
        return y -> label collection
        '''

        #scales the data per column with minmaxscaler
        print("Scale data...")
        minmaxscaler = pp.MinMaxScaler()
        for col in tqdm.trange(len(df.columns)):

            df[df.columns[col]] = df[df.columns[col]].astype(float)
            df.dropna(inplace=True)
            df[df.columns[col]] = minmaxscaler.fit_transform(df[df.columns[col]].values.reshape(-1,1))
            #stors scaler params into dictionary
            scalerParams = {}
            scalerParams["min"] = minmaxscaler.min_[0]
            scalerParams["scale"] = minmaxscaler.scale_[0]
            scalerParams["data_min"] = minmaxscaler.data_min_[0]
            scalerParams["data_max"] = minmaxscaler.data_max_[0]
            scalerParams["data_range"] = minmaxscaler.data_range_[0]
            self.scalerData[df.columns[col]] = scalerParams

        df.dropna(inplace=True)

        sequential_data = []
        prev_days = deque(maxlen=self.seq_len)

        #generates sequences with given sequence length
        print("Generate sequences...")
        for row in tqdm.trange(len(df.values)):
            prev_days.append([n for n in df.values[row][:-1]])
            if len(prev_days) == self.seq_len:
                sequential_data.append([numpy.array(prev_days), df.values[row][-1]])

        #shuffles the sequences
        random.shuffle(sequential_data)

        #stores the index of the prediction values
        for index in range(0, len(df.columns)):
            if df.columns[index] == f"{self.ratio}_open":
                index_ratio = index

        #balances the values
        buys = []
        sells = []
        print("Balance sequences...")
        for i in tqdm.trange(len(sequential_data)):
            seq, future = sequential_data[i]
            if float(future) > float(seq[len(seq) - 1][index_ratio]):
                buys.append([seq, future])
            else:
                sells.append([seq, future])

        #shuffles the data again
        random.shuffle(buys)
        random.shuffle(sells)

        lower = min(len(buys), len(sells))

        #cuts off the overlapping data
        buys = buys[:lower]
        sells = sells[:lower]
        sequential_data = buys + sells
        random.shuffle(sequential_data)

        x = []
        y = []

        #stores the sequences and labels in different arrays
        for seq, future in sequential_data:
            x.append(seq)
            y.append(future)

        return numpy.array(x), numpy.array(y)

    def __saveScalerData__(self):
        '''
        Saves used scalter data for later usage in file
        '''

        #creates the file path to store the scaler dictionary
        filepath = pathlib.Path(__file__).parent.parent.absolute()
        filepath = f"{filepath}\\models\\checkpoints\\"
        filename = f"{self.ratio}_scaler_data_{int(time.time())}.txt"

        #saves the dictionary in txt file
        with open(f"{filepath}{filename}", 'w') as file:
            file.write(json.dumps(self.scalerData))

    def run(self):
        '''
        Starts the preprocessing to generate data to train a lstm network

        return train_x      -> Training sequences
        return train_x      -> Training labels
        return validation_x -> Validation sequences
        return validation_y -> Validation labels
        return test_x       -> Test sequences
        return test_y       -> Test labels
        '''

        #climb the process
        print(f"Prepare data for lstm network - coin:{self.ratio}")
        rawData = self.__getRawData__()
        shiftedData = self.__shiftData__(rawData)
        train_df, val_df, test_df = self.__splitData__(shiftedData)

        #init of scaler params dictionary
        self.scalerData = {}

        #preprocess the data frames
        print("Preprocessing train data...")
        train_x, train_y = self.__preprocess__(train_df)
        print("Preprocessing validation data...")
        validation_x, validation_y = self.__preprocess__(val_df)
        print("Preprocessing test data...")
        test_x, test_y = self.__preprocess__(test_df)

        self.__saveScalerData__()

        return train_x, train_y, validation_x, validation_y, test_x, test_y