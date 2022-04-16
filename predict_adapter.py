import random
import pickle
from model.random_model import Model
from sklearn.feature_extraction.text import CountVectorizer

MS_type_labels = {
        0: 'PPMS',
        1: 'SPMS',
        2: 'RRMS',
        3: 'Benign',
        4: 'Unknown'
    }

model_name = 'model/regression_model_bow.sav'
# model_name = 'model/random_model.sav'

class MSDataset(object):
    def __init__(self, data, labels, idxs_train, idxs_test):
        self.train_set = [data[i] for i in idxs_train]
        self.train_labels = [labels[i] for i in idxs_train]
        self.test_set = [data[i] for i in idxs_test]
        self.test_labels = [labels[i] for i in idxs_test]
        
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
    print("Predicting using model for: \n'",predict_text, "'\n ...")
    bow = pickle.load(open('model/vectorizer_full.sav', 'rb'))
    predict_vector = bow.transform([predict_text]) # transform to a bag of words vector

    # here we should import the model, and call the actual predict funtions
    ans = textPredictor.predict(predict_text=predict_vector)

    return MS_type_labels[ans[0]] 
    # MS_type_labels[ans]

# print(textPredictor.model)
# print(predict('hello my name is johnston'))