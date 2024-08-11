from metrics import Metrics
import scipy
import pandas as pd
import numpy as np

class Sharpe(Metrics):
    
    def optimize(self):
        self.num_assets = self.log_returns.shape[1]
        self.weights = np.array(self.num_assets * [1. / self.num_assets])
        
        def sharpe_neg(weights):
            """
            calculates the sharpe ratio of a portfolio. returns the negative value, so we can 
            minimize the function in the optimizer

            Args:
                weights (list[float]): weights of each stock in a portfolio

            Returns:
                float: sharpe ratio
            """
            self.weights = weights
            if self.yearly_volatility == 0:
                return np.inf
            
            self.yearly_volatility = self.calc_yearly_volatility()
            self.yearly_returns = self.calc_yearly_portfolio_returns()
            
            return -self.yearly_returns / self.yearly_volatility
        
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(self.num_assets))
        
        optimizer = scipy.optimize.minimize(sharpe_neg,
                                            self.weights,
                                            method='SLSQP',
                                            bounds=bounds,
                                            constraints=constraints)
        
        return optimizer
    
    def calc_statistics(self):
        optimizer = self.optimize()
        self.weights = optimizer.x
        self.yearly_volatility = self.calc_yearly_volatility() * 100
        self.yearly_returns = self.calc_yearly_portfolio_returns() * 100
        sharpe_ratio = (self.yearly_returns / self.yearly_volatility)
        return self.weights.round(2), self.yearly_returns.round(2), self.yearly_volatility.round(2), sharpe_ratio.round(2)
    

# s = Sharpe(ticker_list=['AAPL', 'MSFT', 'TSLA'])
# print(s.calc_statistics())
            
            