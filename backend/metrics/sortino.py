import pandas as pd
from .portfolio_optimizer import PortfolioOptimizer
from scipy import optimize
from typing import Tuple
import numpy as np

class Sortino(PortfolioOptimizer):
    """
    Optimizes a portfolio using the Sortino ratio.
    
    Args:
        PortfolioOptimizer (PortfolioOptimizer): Inherited base class for portfolio optimization.
    """
    
    def optimize_portfolio(self, risk_free_rate: float = 0) -> Tuple[np.ndarray, float, float, float]:
        log_returns = np.log(self.price_data / self.price_data.shift(1)).dropna()
        mean_returns = log_returns.mean()
        cov_matrix = log_returns.cov()
        n_stocks = len(self.ticker_list)
        
        return self.maximize_ratio(mean_returns=mean_returns,
                                   cov_matrix=cov_matrix,
                                   risk_free_rate=risk_free_rate,
                                   n_holdings=n_stocks)
    
    def calculate_downside_deviation(self, log_returns: pd.DataFrame, weights: np.ndarray, threshold: float = 0) -> float:
        portfolio_log_returns = np.dot(log_returns, weights)
        # Convert log returns to simple returns for downside deviation calculation
        portfolio_simple_returns = np.exp(portfolio_log_returns) - 1
        downside_returns = np.minimum(portfolio_simple_returns - threshold, 0)
        return np.sqrt(np.mean(downside_returns**2)) * np.sqrt(252)
    
    def maximize_ratio(self,
                       mean_returns: pd.Series,
                       cov_matrix: pd.DataFrame,
                       risk_free_rate: float,
                       n_holdings: int) -> Tuple[np.ndarray, float, float, float]:
        
        def neg_sortino(weights: np.ndarray,
                        mean_returns: pd.Series,
                        cov_matrix: pd.DataFrame,
                        risk_free_rate: float) -> float:
            log_returns = np.log(self.price_data / self.price_data.shift(1)).dropna()
            portfolio_log_return = np.sum(mean_returns * weights) * 252
            # Convert annualized log return to simple return
            portfolio_simple_return = np.exp(portfolio_log_return) - 1
            downside_deviation = self.calculate_downside_deviation(log_returns, weights)
            sortino_ratio = (portfolio_simple_return - risk_free_rate) / downside_deviation
            return -sortino_ratio
        
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(n_holdings))
        initial_weights = np.array([1/n_holdings] * n_holdings)
        
        result = optimize.minimize(fun=neg_sortino,
                                   x0=initial_weights,
                                   args=(mean_returns, cov_matrix, risk_free_rate),
                                   method='SLSQP',
                                   bounds=bounds,
                                   constraints=constraints)
        
        optimized_weights = result.x.round(4)
        sortino_ratio = -result.fun.round(4)
        
        # Convert annualized log return to simple return
        portfolio_log_return = np.sum(mean_returns * optimized_weights) * 252
        portfolio_return = (np.exp(portfolio_log_return) - 1).round(4)
        
        log_returns = np.log(self.price_data / self.price_data.shift(1)).dropna()
        downside_deviation = self.calculate_downside_deviation(log_returns, optimized_weights).round(4)

        return optimized_weights, portfolio_return, downside_deviation, sortino_ratio