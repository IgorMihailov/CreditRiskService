# os to handle saving/deleting images
import os
import pickle
import pandas as pd
import numpy as np

def predict(data_dict):

    data = pd.DataFrame([data_dict])#, index = [0])
    data = pd.get_dummies(data, columns=['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'])

    model = pickle.load(open('project/scoring/model.bin', 'rb'))
    predictions = model.predict(data).tolist()

    return predictions[0]
