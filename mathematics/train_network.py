import time
import pathlib
import tensorflow as tensorflow
import mathematics.preprocess_data as pre
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

class NetworkTraining():
    '''
    Class for the creating of lstm networks
    '''

    def __init__(self, seq_len=60, future_period=288):
        '''
        Constructor of NetworkTraining class
        Sets important instance variables

        param seq_len -> length of sequneces for the training
        param future_period -> prediction of count of steps into future
        '''

        self.seq_len = seq_len
        self.future_period = future_period
        self.validation_pct = 0.05
        self.test_pct = 0.2
        self.epochs = 5
        self.batch_size = 64

        #sets variable for paths to save the models in
        self.name_prefix = f"{self.seq_len}-seq-{self.future_period}-pred-{int(time.time())}"
        self.root_path = pathlib.Path(__file__).parent.parent.absolute()

    def __trainModel__(self, name, train_x, train_y, validate_x, validate_y, test_x, test_y):
        '''
        Trains a model with the given sequences and labels

        param name -> name of the coin the network is for
        param train_x -> training data sequences
        param train_y -> training data labels
        param validation_x -> validation data sequences
        param validation_y -> validation data labels
        param test_x -> validation data sequences
        param test_y -> validation data labels
        '''

        #creates a sequential model
        model = Sequential()

        #adds a new lstm, dropout and batch_normalization layer
        model.add(LSTM(128, activation="relu", input_shape=(train_x.shape[1:]), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        #adds a new lstm, dropout and batch_normalization layer
        #model.add(LSTM(128, activation="relu", return_sequences=True))
        #model.add(Dropout(0.2))
        #model.add(BatchNormalization())

        #adds a new lstm, dropout and batch_normalization layer
        model.add(LSTM(128, activation="relu"))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        #adds a new dense and dropout layer
        model.add(Dense(32, activation="relu"))
        model.add(Dropout(0.2))

        #adds the output dense layer
        model.add(Dense(1, activation="linear"))

        #creates the optimizer adam with specified learning rate and decay
        opt = tensorflow.keras.optimizers.Adam(lr=0.001, decay=1e-6)

        #compiles the model with specified loss function and adds additional metrics
        model.compile(
            loss='mse',
            optimizer=opt,
            metrics=['mae']
        )

        #creates logs for tensorboard and defines the storage of the model checkpoints
        tensorboard = TensorBoard(log_dir=f"{self.root_path}\\logs\\{self.name_prefix}")
        filename = "RNN_Model_Final-{epoch:02d}-{val_mae:.3f}"
        checkpoint = ModelCheckpoint("{}\\models\\checkpoints\\{}_{}.model".format(self.root_path, name, filename, monitor="val_mae", verbose=1, save_best_one=True, mode="max"))

        #trains the model
        history = model.fit(
            train_x, train_y,
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(validate_x, validate_y),
            callbacks=[tensorboard, checkpoint],
            verbose=1,
        )

        #tests the model and print results to console
        score = model.evaluate(test_x, test_y, verbose=1)
        print('Test loss:', score[0])
        print('Test mse:', score[1])

    def startTraining(self, coin):
        '''
        Starts the training of an lstm model with a given coin to predict

        param coin -> coin name to train the model for
        '''

        #generates data for the training from the database
        preprocessing = pre.Preprocessing(coin, self.seq_len, self.future_period, self.validation_pct, self.test_pct)
        train_x, train_y, val_x, val_y, test_x, test_y = preprocessing.run()

        #trains the model
        self.__trainModel__(coin, train_x, train_y, val_x, val_y, test_x, test_y)