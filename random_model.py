from random import randrange
import pickle

class Model:
    def __init__(self):
        pass

    def predict(self, predict_text):
        self.predict_text = predict_text
        return randrange(4)

random_model = Model()
file_location = 'random_model.sav'

pickle.dump(random_model, open(file_location, 'wb'))