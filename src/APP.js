import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function App() {
  const [historicalData, setHistoricalData] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [changePoint, setChangePoint] = useState(null);

  // Fetch historical data
  useEffect(() => {
    const fetchHistoricalData = async () => {
      const response = await axios.get('/api/historical-data', {
        params: { start_date: '2020-01-01', end_date: '2022-12-31' }
      });
      setHistoricalData(response.data);
    };
    fetchHistoricalData();
  }, []);

  // Fetch ARIMA forecast
  const fetchForecast = async () => {
    const response = await axios.post('/api/arima-forecast', { steps: 30 });
    setForecastData(response.data.forecast.map((price, i) => ({
      Date: new Date(Date.now() + i * 86400000).toISOString().split('T')[0],
      Price: price
    })));
  };

  // Fetch Bayesian change point
  const fetchChangePoint = async () => {
    const response = await axios.get('/api/bayesian-change-point');
    setChangePoint(response.data.change_point);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Brent Oil Price Analysis</h1>

      {/* Historical Data Chart */}
      <LineChart width={800} height={400} data={historicalData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="Date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="Price" stroke="#8884d8" activeDot={{ r: 8 }} />
      </LineChart>

      {/* Forecast Button */}
      <button onClick={fetchForecast}>Fetch ARIMA Forecast</button>
      {forecastData.length > 0 && (
        <LineChart width={800} height={400} data={forecastData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Price" stroke="#82ca9d" />
        </LineChart>
      )}

      {/* Change Point Detection */}
      <button onClick={fetchChangePoint}>Detect Change Point</button>
      {changePoint !== null && <p>Most Likely Change Point: Day {changePoint}</p>}
    </div>
  );
}

export default App;