import numpy as np
from flask import Flask, request, render_template, jsonify
import pickle
from data_encoding import  map_brand_to_numeric,map_sim_type_to_numeric
from insert_Data_mysql import insert_Data

from sklearn.linear_model import Lasso
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor


app = Flask(__name__)

model = pickle.load(open('models/xgb_model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        data = request.json
        brand = map_brand_to_numeric(data['brand'])
        screen_size = float(data['screen_size'])
        ram = int(data['ram'])
        rom = int(data['rom'])
        sim_type = map_sim_type_to_numeric(data['sim_type'])
        battery = int(data['battery'])

        int_features = [brand, screen_size, ram, rom, sim_type, battery]
        final_features = [np.array(int_features)]

        predicted_price = model.predict(final_features)
        prediction_result = round(predicted_price[0], 2)

        data_insert = (data['brand'],screen_size,ram,rom,data['sim_type'],battery,float(prediction_result))
        print(data_insert)

        insert_Data(data_insert)



        return jsonify({'predicted_price': float(prediction_result)})

if __name__ == '__main__':
    app.run(debug=True)
