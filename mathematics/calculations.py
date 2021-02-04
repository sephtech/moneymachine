import numpy
import tqdm
import pathlib
import mathematics.preprocess_data as pre
import system_interaction.database_interaction as dbi
import tensorflow as tf
from sklearn import preprocessing as pp

class Calculations():
    '''
    Comes with methods to calculate and transform 
    the needed data for the GUI
    '''

    def predictValue(self, coin, seq_len, future_period):
        '''
        Predicts the next future Value in a given time step

        param coin          -> name of coin to predict a value for
        param seq_len       -> length of the sequences used to train the model
        param future_period -> given time step in 5 seconds

        return -> predicted value
        '''

        #generate path of the model folder
        modelpath = pathlib.Path(__file__).parent.parent.absolute()
        modelpath = f"{modelpath}\\models\\{coin}_{future_period}.model"
        print(modelpath)
        
        #load the model
        model = tf.keras.models.load_model(modelpath, custom_objects=None, compile=True, options=None)
        
        #getting newest sequence and predict th future value
        predictionData, scaler = self.__getSeqPredictData__(coin, seq_len, future_period)
        predictionData = [predictionData]
        predictionData = numpy.array(predictionData)
        predictedValue = model.predict(predictionData)

        #scale the future value inverse
        returnValue = scaler.inverse_transform(predictedValue)

        return returnValue[0][0]

    def __getSeqPredictData__(self, coin, seq_len, future_period):
        '''
        Returns the newest sequence of coin data for the prediction

        param coin          -> name of the coin to predict value for
        param seq_len       -> length of the sequences used to train the model
        param future_period -> given time step in 5 seconds

        return predict_array    -> newest sequence of coin data
        return returnScaler     -> scaler for inverse transformation
        '''

        #getting raw data from database
        processing = pre.Preprocessing(None, None, None, None, None)
        raw = processing.__getRawData__()
        raw.dropna(inplace=True)

        #shift data
        raw['future'] = raw[f"{coin}_open"].shift(-future_period)

        #scales all columns and saves the scaler for inverse transformation
        scaler = pp.MinMaxScaler()
        print("Scale data...")
        for col in tqdm.trange(len(raw.columns)):

            raw[raw.columns[col]] = raw[raw.columns[col]].astype(float)
            raw.dropna(inplace=True)
            raw[raw.columns[col]] = scaler.fit_transform(raw[raw.columns[col]].values.reshape(-1,1))
            
            if raw.columns[col] == "future":
                retrunScaler = scaler

        raw.drop(["future"], 1, inplace=True)
        raw.dropna(inplace=True)

        #sorts the data and uses the newest ones
        times = sorted(raw.index.values)
        last_times = times[-int(seq_len)]

        predict_df = raw[(raw.index >= last_times)]
        predict_df = numpy.array(predict_df)
        predict_array = numpy.array(predict_df)

        return predict_array, retrunScaler
        
    def getGraphAbsoluteData(self, coin):
        '''
        Returns the transformed data for the graph

        param coin -> name of the coin to get data for

        return x_day    -> time axis values for the last day
        return y_day    -> data axis values for the last day
        return x_week   -> time axis values for the last week
        return y_week   -> data axis values for the last week
        return x_month  -> time axis values for the last month
        return y_month  -> data axis values for the last month
        return x_year   -> time axis values for the last year
        return y_year   -> data axis values for the last year
        '''

        interaction = dbi.DatabaseInteraction()
        data = interaction.getCoinDataPackage(coin)

        #splits the data from the database into different x and y arrays
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
        '''
        Transforms the values in the given array to percentages

        param data -> data array for transformation

        return -> array with percentages
        '''

        #saves the start value
        startValue = float(data[0])

        #calculates percentages for every other value
        relativeValues = []
        relativeValues.append(0)
        for value in data[1:]:

            diff = float(value) - startValue
            pct = diff / startValue * 100
            relativeValues.append(pct)

        return relativeValues
