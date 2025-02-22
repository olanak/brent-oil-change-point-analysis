import pymc as pm  # Use `pymc` (not `pymc3`)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def detect_change_points(data_path='data/Processed/processed_data.csv'):
    """Bayesian change point detection with improved sampling."""
    df = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date')
    prices = df['Price'].values
    n = len(prices)
    
    with pm.Model() as model:
        # Priors for changepoint location (single changepoint)
        tau = pm.DiscreteUniform('tau', lower=0, upper=n)
        
        # Priors for mean and variance (adjusted for stability)
        mu = pm.Normal('mu', mu=np.mean(prices), sigma=np.std(prices), shape=2)
        sigma = pm.HalfNormal('sigma', sigma=np.std(prices), shape=2)
        
        # Segment the data into pre/post changepoint
        mu_segment = pm.math.switch(tau > np.arange(n), mu[0], mu[1])
        sigma_segment = pm.math.switch(tau > np.arange(n), sigma[0], sigma[1])
        
        # Likelihood
        likelihood = pm.Normal('likelihood', mu=mu_segment, sigma=sigma_segment, observed=prices)
        
        # Sampling with better initialization and more chains
        trace = pm.sample(
            draws=1000,
            tune=1000,
            chains=4,  # Increased to 4 chains for better diagnostics
            cores=1,
            init='adapt_diag',
            step=[pm.Metropolis([tau]), pm.NUTS([mu, sigma])]
        )
    
    return trace

if __name__ == "__main__":
    trace = detect_change_points()
    pm.plot_trace(trace)  # Use `plot_trace` instead of `traceplot`
    plt.show()