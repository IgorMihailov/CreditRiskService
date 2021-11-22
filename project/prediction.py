# os to handle saving/deleting images
import os
import pickle
import pandas as pd
import numpy as np

def predict(data_dict):

    data = pd.DataFrame([data_dict])#, index = [0])
    data = pd.get_dummies(data, columns=['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'])

    model = pickle.load(open('ml_models/model.bin', 'rb'))
    predictions = model.predict(data).tolist()

    return predictions[0]

    # @app.route('/')
    # def hello():
    #     return render_template('index.html', name='Jerry')

    #loaded_model = pickle.load(open('models/model.bin', 'rb'))
    #####
    # MODEL TEST SECTION

    # #loaded_model.predict();
    # data = pd.read_csv("credit_risk_dataset.csv")
    #
    # #target = data["loan_status"]
    # data = data.drop("loan_status", axis=1)
    # data = pd.get_dummies(data, columns=['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'])
    #
    # str = data.tail(1)
    #
    # result = loaded_model.predict(str)
    # return str.to_json(orient='records')[1:-1].replace('},{', '} {')
    #np.array_str(result)
    #return 'Home'
    #####
