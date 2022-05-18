# import random
import pickle
#from model.random_model import Model
from sklearn.feature_extraction.text import CountVectorizer

'''
In the future, when there is a different NLP model that is created,
it should be relatively straightforward to add it here. To do so, just
import the relevant packages, load the pre-trained model as model_name,
and ensure it has a 'predict' function associated with it.
Additionally, if the MS type labels change, etc., please ensure that this 
is changed in the MS_type_labels dictionary below.

This original release version includes a Bag-of-Words linear regression model.
To understand how this model was created, please inspect the .ipynb file
titled "BoW_model.ipynb". 
'''

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

    # here we use the imported model, and call the predict funtions
    ans = textPredictor.predict(predict_text=predict_vector)

    return MS_type_labels[ans[0]] 