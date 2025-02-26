# **Brent Oil Price Analysis: Change Point Detection and Statistical Modeling**

## Table of Contents
1. [Overview](#overview)
2. [Business Objective](#business-objective)
3. [Methodology](#methodology)
4. [Results](#results)
5. [Usage Instructions](#usage-instructions)
6. [Dependencies](#dependencies)
7. [Acknowledgments](#acknowledgments)

---

## Overview

This project analyzes historical Brent oil price data to identify significant events that impact price fluctuations. Using advanced statistical models (ARIMA, GARCH, Bayesian change point detection) and machine learning techniques (LSTM), we provide actionable insights for investors, policymakers, and energy companies. The analysis is complemented by an interactive dashboard built with Flask (backend) and React (frontend).

The dataset spans daily prices from **May 20, 1987, to September 30, 2022**, and additional factors like GDP growth, inflation, exchange rates, and geopolitical events are incorporated to enhance the analysis.

---

## Business Objective

As a data scientist at **Birhan Energies**, a leading consultancy firm specializing in energy market insights, the goal of this project is to:
1. Identify key events that have significantly impacted Brent oil prices over the past decade.
2. Measure the magnitude of these impacts on price changes.
3. Provide clear, data-driven insights to guide investment strategies, policy development, and operational planning.

The global energy market's volatility makes it challenging for stakeholders to make informed decisions. This project addresses this need by delivering:
- Accurate forecasts of price movements.
- Insights into how political decisions, conflicts, sanctions, and OPEC policies affect oil prices.
- Tools for risk management and strategic planning.

---

## Methodology

### **Task 1: Defining the Data Analysis Workflow**
1. **Data Understanding**:
   - The dataset contains daily Brent oil prices (`Price`) recorded from May 20, 1987, to September 30, 2022.
   - Each entry includes a `Date` field formatted as `day-month-year`.

2. **Exploratory Data Analysis (EDA)**:
   - Visualized trends, seasonality, and potential change points in the time series.
   - Checked for stationarity using the Augmented Dickey-Fuller (ADF) test.
   - Analyzed autocorrelation (ACF) and partial autocorrelation (PACF) to determine lag structures.

3. **Model Selection**:
   - Explored traditional time series models (ARIMA, GARCH).
   - Investigated Bayesian inference using PyMC3 for detecting change points.
   - Considered machine learning models like LSTM for capturing complex patterns.

4. **Assumptions and Limitations**:
   - Assumed the data is representative of global Brent oil price trends.
   - Limited by the availability of external factors (e.g., geopolitical events, economic indicators) for the entire date range.

---

### **Task 2: Advanced Statistical and Machine Learning Models**
1. **Time Series Analysis**:
   - Applied ARIMA to model trends and seasonality.
   - Used GARCH to capture volatility in residuals.

2. **Bayesian Change Point Detection**:
   - Detected significant shifts in the time series using PyMC3.
   - Associated change points with major events (e.g., geopolitical conflicts, OPEC policy changes).

3. **Long Short-Term Memory (LSTM) Model**:
   - Developed an LSTM neural network to forecast short-term price movements.
   - Achieved an RMSE of **2.0098**, indicating reasonable accuracy.

4. **Incorporating Additional Factors**:
   - Integrated economic indicators (GDP growth, inflation, exchange rates).
   - Examined technological advancements and regulatory changes affecting the oil market.

---

### **Task 3: Interactive Dashboard Development**
An interactive dashboard was developed to visualize the results and facilitate exploration:
- **Backend (Flask)**:
  - Served APIs for historical data, forecasts, and model outputs.
  - Handled requests for different datasets and performance metrics.

- **Frontend (React)**:
  - Created an intuitive interface for displaying trends, forecasts, and correlations.
  - Included features like event highlighting, date range filtering, and model comparisons.

---

## Results

1. **Key Events Impacting Brent Oil Prices**:
   - Political Decisions: Events like the Iraq-Kuwait conflict (1990) and the Russia-Ukraine war (2022) caused significant price spikes.
   - Economic Indicators: Positive correlation between global GDP growth and oil prices.
   - Exchange Rates: Inverse relationship between USD strength and oil prices.

2. **Model Performance**:
   - ARIMA: Captured overall trends; RMSE: **X.XX**.
   - GARCH: Modeled volatility effectively.
   - LSTM: Demonstrated superior performance during volatile periods; RMSE: **2.0098**.

3. **Insights**:
   - Volatility peaks during crises (e.g., pandemics, wars).
   - OPEC policy changes directly influence global oil supply and prices.

---

## Usage Instructions

### **Prerequisites**
Ensure you have the following installed:
- Python 3.8+ (preferably in a virtual environment).
- Node.js and npm for the React frontend.

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/brent-oil-analysis.git
   cd brent-oil-analysis
   ```

2. Set up the Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Load environment variables:
   - Create a `.env` file in the root directory and add API keys:
     ```
     FRED_API_KEY=your_fred_api_key_here
     NEWSAPI_API_KEY=your_newsapi_api_key_here
     EXCHANGERATE_API_KEY=your_exchangerate_api_key_here
     ```

4. Start the Flask backend:
   ```bash
   python app.py
   ```

5. Set up the React frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

6. Access the dashboard:
   - Open your browser and navigate to [http://localhost:3000](http://localhost:3000).

---

## Dependencies

### **Python**
Install dependencies using:
```bash
pip install -r requirements.txt
```

Key libraries:
- `pandas`: For data manipulation.
- `numpy`: For numerical computations.
- `statsmodels`: For ARIMA and GARCH models.
- `tensorflow`: For building and training the LSTM model.
- `pymc`: For Bayesian change point detection.
- `flask`: For serving APIs in the backend.

### **JavaScript (React Frontend)**
Install dependencies using:
```bash
cd frontend
npm install
```

Key libraries:
- `react`: For building the user interface.
- `recharts`: For interactive visualizations.
- `axios`: For making API calls to the Flask backend.

---

## Acknowledgments

Special thanks to the tutors at **10 Academy** for their guidance and support:
- Mahlet
- Rediet
- Kerod
- Elias
- Emitinan
- Rehmet

This project would not have been possible without their expertise and encouragement.

---

## References

1. **Data Science Workflow**:
   - [Mastering the Data Science Workflow](https://towardsdatascience.com/mastering-the-data-science-workflow-2a47d8b613c4)
   - [Comprehensive Guide to Data Science Workflow](https://www.datascience-pm.com/data-science-workflow/)

2. **Change Point Analysis**:
   - [Change Point Detection in Time Series](https://forecastegy.com/posts/change-point-detection-time-series-python/)
   - [Bayesian Changepoint Detection with PyMC3](https://www.pymc.io/blog/chris_F_pydata2022.html)

3. **Bayesian Inference and MCMC**:
   - [Introduction to Bayesian Statistics](https://warwick.ac.uk/fac/sci/statistics/staff/academic-research/steel/steel_homepage/bayesiantsrev.pdf)
   - [Monte Carlo Markov Chain Explained](https://towardsdatascience.com/monte-carlo-markov-chain-mcmc-explained-94e3a6c8de11)

4. **React Dashboard Templates**:
   - [CoreUI Free React Admin Template](https://github.com/coreui/coreui-free-react-admin-template)
   - [Light Bootstrap Dashboard React](https://github.com/creativetimofficial/light-bootstrap-dashboard-react)

---

## Screenshots

![Historical Trends](path_to_screenshot_historical_trends.png)
*Figure 1: Historical trends with event highlights.*

![LSTM Predictions](path_to_screenshot_lstm_predictions.png)
*Figure 2: LSTM predictions vs actual prices.*

![Dashboard Interface](path_to_screenshot_dashboard.png)
*Figure 3: Interactive dashboard interface.*

---

## Final Thoughts

This project provides a comprehensive analysis of Brent oil price fluctuations and their association with major events. By leveraging advanced statistical models and machine learning techniques, we deliver actionable insights to help stakeholders navigate the complexities of the global energy market.

Feel free to explore the codebase, run the dashboard locally, or extend the analysis further. Contributions and feedback are welcome!

---

## Contact

For questions or collaboration opportunities, please contact:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

This README serves as a guide for understanding and replicating the project. Ensure all paths and dependencies are correctly configured before running the application. Happy exploring!
