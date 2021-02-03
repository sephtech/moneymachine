import numpy
import tqdm
import pathlib
import mathematics.preprocess_data as pre
import system_interaction.database_interaction as dbi
import tensorflow as tf
from sklearn import preprocessing as pp


class Calculations():

    def predictValue(self, coin, seq_len, future_period):

        modelpath = pathlib.Path(__file__).parent.parent.absolute()
        modelpath = f"{modelpath}\\models\\{coin}_{future_period}.model"
        
        model = tf.keras.models.load_model(modelpath, custom_objects=None, compile=True, options=None)
        
        predictionData, scaler = self.__getSeqPredictData__(coin, seq_len)
        predictionData = [predictionData]
        predictionData = numpy.array(predictionData)
        predictedValue = model.predict(predictionData)

        returnValue = scaler.inverse_transform(predictedValue)

        return returnValue[0][0]

    def __getSeqPredictData__(self, coin, seq_len):

        processing = pre.Preprocessing(None, None, None, None, None)
        raw = processing.__getRawData__()
        raw.dropna(inplace=True)

        times = sorted(raw.index.values)
        last_times = times[-int(seq_len)]

        scaler = pp.MinMaxScaler()
        print("Scale data...")
        for col in tqdm.trange(len(raw.columns)):

            raw[raw.columns[col]] = raw[raw.columns[col]].astype(float)
            raw.dropna(inplace=True)
            raw[raw.columns[col]] = scaler.fit_transform(raw[raw.columns[col]].values.reshape(-1,1))
            
            if raw.columns[col] == f"{coin}_open":
                retrunScaler = scaler

        raw.dropna(inplace=True)

        predict_df = raw[(raw.index >= last_times)]
        predict_df = numpy.array(predict_df)
        predict_array = numpy.array(predict_df)

        return predict_array, retrunScaler 
        
    def getGraphAbsoluteData(self, coin):

        interaction = dbi.DatabaseInteraction()
        data = interaction.getCoinDataPackage(coin)

        transformedTimelines = []
        for timeline in data:

            x = []
            y = []
            for timestamp in timeline:
                x.append(int(timestamp[0]))
                y.append(float(timestamp[1]))
            
            transformedTimelines.append(x)
            transformedTimelines.append(y)

        self.calculateRelativeChanges(transformedTimelines[1])
        return transformedTimelines

    def calculateRelativeChanges(self, data):

        startValue = float(data[0])

        relativeValues = []
        relativeValues.append(0)
        for value in data[1:]:

            diff = float(value) - startValue
            pct = diff / startValue * 100
            relativeValues.append(pct)

        return relativeValues
