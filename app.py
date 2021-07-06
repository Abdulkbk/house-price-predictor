from flask import Flask, render_template, request
from sklearn.base import BaseEstimator, TransformerMixin
import json
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)


class AddAtrributes(BaseEstimator, TransformerMixin):
    def __init__(self, do=True):
        self.do = do

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        bathrooms_per_bedrooms = X[:, 1] / X[:, 0]
        bedrooms_per_bathrooms = X[:, 0] / X[:, 1]
        bedrooms_bathrooms = X[:, 0] * X[:, 1]
        bathrooms_toilets = X[:, 1] * X[:, 2]
        if self.do:
            return np.c_[X, bathrooms_per_bedrooms, bedrooms_per_bathrooms, bedrooms_bathrooms, bathrooms_toilets]
        else:
            return X


model = joblib.load('./model/regressor.joblib')
cols = ['bedrooms', 'bathrooms', 'toilets',
        'parking_space', 'title', 'town', 'state']


@app.route('/')
def home_page():
    return render_template('index.html ')


@app.route('/predict', methods=['GET', 'POST'])
def predict_price():
    req = json.loads(request.data)

    bedrooms = int(req['bedrooms'])
    bathrooms = int(req['bathrooms'])
    toilets = int(req['toilets'])
    parking = int(req['parking_space'])
    title = req['title']
    town = req['town']
    state = req['state']

    dt = [bedrooms, bathrooms, toilets, parking, title, town, state]

    dataframe = pd.DataFrame([dt], columns=cols)
    result = model.predict(dataframe)[0]
    return {'price': result}


if __name__ == "__main__":
    app.run(debug=True)
