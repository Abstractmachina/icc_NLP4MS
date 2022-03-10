import random
import pickle
from random_model import Model

MS_type_labels = {
        0: 'PPMS',
        1: 'SPMS',
        2: 'RRMS',
        3: 'Benign',
        4: 'Unknown'
    }

# model_name = 'regression_model_bow.sav'
model_name = 'random_model.sav'

class TextPredictor:
    def __init__(self, model_name):
        """
        Initialization for the TextPredictor class
        """
        self.model = pickle.load(open(model_name, 'rb'))

    def predict(self, predict_text):
        return self.model.predict(predict_text)

    
textPredictor = TextPredictor(model_name=model_name)

def predict(predict_text):
    print(predict_text)

    # here we should import the model, and call the actual predict funtions
    ans = textPredictor.predict(predict_text=predict_text)

    return MS_type_labels[ans]