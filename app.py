# Import necessary libraries
from flask import Flask, jsonify, request
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model

# Initialize Flask app
app = Flask(__name__)

# Load datasets and models
df = pd.read_csv('data/processed/merged_oil_data.csv', parse_dates=['Date'], index_col='Date')

# Load ARIMA model
arima_model = joblib.load('models/arima_model.joblib')

# Load GARCH model
garch_model = joblib.load('models/garch_model.joblib')

# Load LSTM model
lstm_model = load_model('models/lstm_model.h5')

# Define API endpoints

## Endpoint 1: Historical Data
@app.route('/api/historical-data', methods=['GET'])
def get_historical_data():
    start_date = request.args.get('start_date', default=df.index.min(), type=str)
    end_date = request.args.get('end_date', default=df.index.max(), type=str)

    # Filter data by date range
    filtered_data = df.loc[start_date:end_date]
    return jsonify(filtered_data.reset_index().to_dict(orient='records'))

## Endpoint 2: ARIMA Forecast
@app.route('/api/arima-forecast', methods=['POST'])
def arima_forecast():
    data = request.json
    steps = data.get('steps', 30)  # Number of steps to forecast
    forecast = arima_model.forecast(steps=steps)
    return jsonify({'forecast': forecast.tolist()})

## Endpoint 3: GARCH Volatility
@app.route('/api/garch-volatility', methods=['POST'])
def garch_volatility():
    data = request.json
    steps = data.get('steps', 30)  # Number of steps to forecast
    forecast = garch_model.forecast(horizon=steps).variance.values[-1, :]
    return jsonify({'volatility': forecast.tolist()})

## Endpoint 4: Bayesian Change Point Detection
@app.route('/api/bayesian-change-point', methods=['GET'])
def bayesian_change_point():
    trace = joblib.load('models/bayesian_trace.joblib')
    most_likely_tau = int(np.round(trace.posterior["tau"].mean().item()))
    return jsonify({'change_point': most_likely_tau})

## Endpoint 5: LSTM Predictions
@app.route('/api/lstm-predict', methods=['POST'])
def lstm_predict():
    data = request.json
    input_data = np.array(data['input_data'])  # Input sequence for prediction
    seq_length = len(input_data)

    # Scale input data
    scaler = joblib.load('models/scaler.joblib')  # Load the scaler used during training
    scaled_input = scaler.transform(input_data.reshape(-1, 1))

    # Reshape input for LSTM
    X = scaled_input[-seq_length:].reshape(1, seq_length, 1)

    # Make predictions
    y_pred_scaled = lstm_model.predict(X)
    y_pred = scaler.inverse_transform(y_pred_scaled)[0][0]
    return jsonify({'prediction': y_pred})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)