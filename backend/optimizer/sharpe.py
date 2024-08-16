import pandas as pd
from .portfolio_optimizer import PortfolioOptimizer
from scipy import optimize
from typing import Tuple
import numpy as np

class Sharpe(PortfolioOptimizer):
    """
    Optimizes a portfolio's weights based on the maximum Sharpe ratio the portfolio can receive
    
    S = E[r_p - rf] / std_p
    r_p = return of portfolio
    rf = risk free rate
    std_p = std of portfolio's excess return
    
    x < 1 = bad, 1 <= x <= 2 = good, x > 2 = great
    """
    
    def optimize_portfolio(self,
                           risk_free_rate: float = 0.0) -> Tuple[np.ndarray, float, float, float]:
        """
        Optimizes the portfolio based on Sharpe ratio
        
        1. Find log returns
        2. Find mean of log returns
        3. Compute covariance matrix
        """
        log_returns = np.log(self.price_data / self.price_data.shift(1)).dropna()
        mean_returns = log_returns.mean()
        covariance = log_returns.cov()
        n_stocks = len(self.ticker_list)
        
        if n_stocks != len(mean_returns) or n_stocks != covariance.shape[0]:
            raise ValueError("Mismatch in number of stocks and data dimensions")
        
        return self.maximize_ratio(mean_returns=mean_returns,
                                   covar_returns=covariance,
                                   risk_free_rate=risk_free_rate,
                                   n_holdings=n_stocks)
    
    def maximize_ratio(self,
                       mean_returns: pd.Series,
                       covar_returns: pd.DataFrame,
                       risk_free_rate: float,
                       n_holdings: int) -> Tuple[np.ndarray, float, float, float]:
        """
        Helper function to maximize the Sharpe ratio
        """
        
        def neg_sharpe(weights: np.ndarray,
                       mean_returns: np.ndarray,
                       covar_returns: np.ndarray,
                       risk_free_rate: float) -> float:
            """
            Calculate the Sharpe Ratio
            
            1. Find portfolio return over the course of a trading year (252 days)
            2. Find the std of excess returns of a single year
            """
            portfolio_return = np.sum(mean_returns * weights) * 252
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covar_returns, weights))) * np.sqrt(252)
            
            # Convert log return to simple return for Sharpe ratio calculation
            portfolio_simple_return = np.exp(portfolio_return) - 1
            sharpe_ratio = (portfolio_simple_return - risk_free_rate) / portfolio_volatility
            return -sharpe_ratio
        
        mean_returns = mean_returns.values
        covar_returns = covar_returns.values
        
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(n_holdings))
        initial_weights = np.array([1/n_holdings] * n_holdings)
        
        result = optimize.minimize(fun=neg_sharpe,
                                   x0=initial_weights,
                                   args=(mean_returns, covar_returns, risk_free_rate),
                                   method='SLSQP',
                                   bounds=bounds,
                                   constraints=constraints)
        
        optimized_weights = result.x.round(4)
        sharpe_ratio = -result.fun.round(4)
        
        # Convert annualized log return to simple return
        yearly_log_return = np.sum(mean_returns * optimized_weights) * 252
        yearly_return = (np.exp(yearly_log_return) - 1).round(4)
        
        yearly_volatility = (np.sqrt(np.dot(optimized_weights.T, np.dot(covar_returns, optimized_weights))) * np.sqrt(252)).round(4)

        return optimized_weights, yearly_return, yearly_volatility, sharpe_ratio        