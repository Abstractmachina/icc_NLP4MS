import random

MS_type_labels = {
        0: 'PPMS',
        1: 'SPMS',
        2: 'RRMS',
        3: 'Benign',
        4: 'Unknown'
    }

def predict(predict_text):
    print(predict_text)
    # here we should import the model, and call the actual predict funtions
    return (random.choice(list(MS_type_labels.values())))