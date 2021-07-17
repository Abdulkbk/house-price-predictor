from flask import Flask, render_template, request
import json
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)


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
    dataframe['lagOrAbj'] = np.where(
        (dataframe['state'] == "Abuja") | (dataframe['state'] == "Lagos"), 1, 0)
    result = model.predict(dataframe)[0]
    return {'price': result}


if __name__ == "__main__":
    app.run(debug=True)
