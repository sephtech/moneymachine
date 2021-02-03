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

    def __init__(self, ratio, seq_len, future_period, validation_pct, test_pct):

        self.ratio = ratio
        self.seq_len = seq_len
        self.future_period = future_period
        self.validation_pct = validation_pct
        self.test_pct = test_pct
        pandas.set_option('mode.chained_assignment', None)

    def __getRawData__(self):

        dbi = database.DatabaseInteraction()
        db = dbi.getDatabase()
        coins = activate_coins.__getDefindedCoins__()

        main_df = pandas.DataFrame()
        print("Collect raw data...")
        for coin in tqdm.trange(len(coins)):
            
            df = pandas.read_sql_query(f"SELECT * FROM {coins[coin]};", db)
            df.drop(["id"], 1, inplace=True)
            df.rename(columns={"date": "time", "low": f"{coins[coin]}_low", "high": f"{coins[coin]}_high", "open": f"{coins[coin]}_open", "close": f"{coins[coin]}_close", "volume": f"{coins[coin]}_volume"}, inplace=True)

            df.set_index("time", inplace=True)

            if len(main_df.columns) == 0:
                main_df = df
            else:
                main_df = main_df.join(df)
        
        main_df.fillna(method="ffill", inplace=True)
        main_df.dropna(inplace=True)

        return main_df

    def __shiftData__(self, df):

        df['future'] = df[f"{self.ratio}_open"].shift(-self.future_period)
        return df

    def __splitData__(self, df):

        times = sorted(df.index.values)
        last_times_test = times[-int(self.test_pct * len(times))]

        test_df = df[(df.index >= last_times_test)]
        main_df = df[(df.index < last_times_test)]

        times_2 = sorted(main_df.index.values)
        last_times_val = times_2[-int(self.validation_pct * len(times_2))]

        val_df = main_df[(main_df.index >= last_times_val)]
        train_df = main_df[(main_df.index < last_times_val)]

        return train_df, val_df, test_df

    def __preprocess__(self, df):

        print("Scale data...")
        minmaxscaler = pp.MinMaxScaler()
        for col in tqdm.trange(len(df.columns)):

            df[df.columns[col]] = df[df.columns[col]].astype(float)
            df.dropna(inplace=True)
            df[df.columns[col]] = minmaxscaler.fit_transform(df[df.columns[col]].values.reshape(-1,1))
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

        print("Generate sequences...")
        for row in tqdm.trange(len(df.values)):
            prev_days.append([n for n in df.values[row][:-1]])
            if len(prev_days) == self.seq_len:
                sequential_data.append([numpy.array(prev_days), df.values[row][-1]])
    
        random.shuffle(sequential_data)

        for index in range(0, len(df.columns)):
            if df.columns[index] == f"{self.ratio}_open":
                index_ratio = index

        buys = []
        sells = []
        print("Balance sequences...")
        for i in tqdm.trange(len(sequential_data)):
            seq, future = sequential_data[i]
            if float(future) > float(seq[len(seq) - 1][index_ratio]):
                buys.append([seq, future])
            else:
                sells.append([seq, future])

        random.shuffle(buys)
        random.shuffle(sells)

        lower = min(len(buys), len(sells))

        buys = buys[:lower]
        sells = sells[:lower]
        sequential_data = buys + sells
        random.shuffle(sequential_data)

        x = []
        y = []

        for seq, future in sequential_data:
            x.append(seq)
            y.append(future)

        return numpy.array(x), numpy.array(y)

    def __saveScalerData__(self):

        filepath = pathlib.Path(__file__).parent.parent.absolute()
        filepath = f"{filepath}\\models\\checkpoints\\"
        filename = f"{self.ratio}_scaler_data_{int(time.time())}.txt"

        with open(f"{filepath}{filename}", 'w') as file:
            file.write(json.dumps(self.scalerData))

    def run(self):

        print(f"Prepare data for lstm network - coin:{self.ratio}")

        rawData = self.__getRawData__()
        shiftedData = self.__shiftData__(rawData)
        train_df, val_df, test_df = self.__splitData__(shiftedData)

        self.scalerData = {}

        print("Preprocessing train data...")
        train_x, train_y = self.__preprocess__(train_df)
        print("Preprocessing validation data...")
        validation_x, validation_y = self.__preprocess__(val_df)
        print("Preprocessing test data...")
        test_x, test_y = self.__preprocess__(test_df)

        self.__saveScalerData__()

        return train_x, train_y, validation_x, validation_y, test_x, test_y