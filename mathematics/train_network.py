import time
import pathlib
import tensorflow as tensorflow
import mathematics.preprocess_data as pre
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

class NetworkTraining():

    def __init__(self, seq_len=60, future_period=288):

        self.seq_len = seq_len
        self.future_period = future_period
        self.validation_pct = 0.05
        self.test_pct = 0.2
        self.epochs = 5
        self.batch_size = 64
        self.name_prefix = f"{self.seq_len}-seq-{self.future_period}-pred-{int(time.time())}"
        self.root_path = pathlib.Path(__file__).parent.parent.absolute()

    def __trainModel__(self, name, train_x, train_y, validate_x, validate_y, test_x, test_y):

        model = Sequential()
        model.add(LSTM(128, activation="relu", input_shape=(train_x.shape[1:]), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        #model.add(LSTM(128, activation="relu", return_sequences=True))
        #model.add(Dropout(0.2))
        #model.add(BatchNormalization())

        model.add(LSTM(128, activation="relu"))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        model.add(Dense(32, activation="relu"))
        model.add(Dropout(0.2))

        model.add(Dense(1, activation="linear"))

        opt = tensorflow.keras.optimizers.Adam(lr=0.001, decay=1e-6)

        model.compile(
            loss='mse',
            optimizer=opt,
            metrics=['mae']
        )

        tensorboard = TensorBoard(log_dir=f"{self.root_path}\\logs\\{self.name_prefix}")
        filename = "RNN_Model_Final-{epoch:02d}-{val_mae:.3f}"
        checkpoint = ModelCheckpoint("{}\\models\\checkpoints\\{}_{}.model".format(self.root_path, name, filename, monitor="val_mae", verbose=1, save_best_one=True, mode="max"))

        history = model.fit(
            train_x, train_y,
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(validate_x, validate_y),
            callbacks=[tensorboard, checkpoint],
            verbose=1,
        )

        score = model.evaluate(test_x, test_y, verbose=1)
        print('Test loss:', score[0])
        print('Test mse:', score[1])

    def startTraining(self, coin):

        preprocessing = pre.Preprocessing(coin, self.seq_len, self.future_period, self.validation_pct, self.test_pct)
        train_x, train_y, val_x, val_y, test_x, test_y = preprocessing.run()

        self.__trainModel__(coin, train_x, train_y, val_x, val_y, test_x, test_y)