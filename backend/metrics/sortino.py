import pandas as pd
import numpy as np
import scipy
from bs4 import BeautifulSoup
import requests
import re
from metrics import Metrics

class Sortino(Metrics):
    
    def get_risk_free_rate(self):
        """
        Grabs the current 10 year treasury rate

        Returns:
            str: curretn risk free rate
        """
        url = "https://www.cnbc.com/quotes/US10Y"
        response = requests.get(url=url)
        
        if response.status_code != 200:
            print(f"Error in getting response: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        bond_price = soup.find('div', class_="QuoteStrip-lastPriceStripContainer").text
        pattern = r'(\d+\.\d+)%'
        match = re.search(pattern=pattern, string=bond_price)
        
        if match:
            return match.group(1)

        print(f"Bond price could not be found: {match}")
        return None
    
    def calc_deviations(self, threshold=0):
        """
        Calculates the standard deviation of a portfolio

        Args:
            threshold (int, optional): Only consider negative returns as a drawdown. Defaults to 0.

        Returns:
            float: standard deviation of a portfolio
        """
        deviations = np.where(self.log_returns < threshold, self.log_returns - threshold, 0)
        squared_deviations = deviations ** 2
        mean_squared_deviation = np.mean(squared_deviations)
        
        return np.sqrt(mean_squared_deviation)
    
    def optimize(self):

        self.num_assets = self.log_returns.shape[1]
        self.weights = np.array(self.num_assets * [1. / self.num_assets])
        
        def sortino(weights):
            """
            Calculates the sortino ratio of a portfolio 

            Args:
                weights (list[float]): weights of each stock in a portfolio

            Returns:
                float: sortino ratio
            """
            self.weights = weights
            risk_free_rate = float(self.get_risk_free_rate()) / 100
            
            portfolio_return = np.sum(self.log_returns.mean() * self.weights) * 252 - risk_free_rate
            downside_deviation = self.calc_deviations()
            portfolio_downside_deviation = np.sqrt(np.dot(np.transpose(self.weights), np.dot(downside_deviation, self.weights)))
            
            return -portfolio_return / portfolio_downside_deviation

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(self.num_assets))
        
        optimizer = scipy.optimize.minimize(sortino,
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
        sortino_ratio = self.yearly_returns / self.yearly_volatility
        
        return self.weights.round(2), self.yearly_returns.round(2), self.yearly_volatility.round(2), sortino_ratio.round(2)

# s = Sortino(ticker_list=['AAPL', 'MSFT', 'TSLA'])
# print(s.calc_statistics())