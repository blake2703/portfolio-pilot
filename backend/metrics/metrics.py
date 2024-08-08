from abc import abstractmethod, ABC
import pandas as pd
import numpy as np
import yfinance as yf
from typing import List
from datetime import datetime

class Metrics(ABC):
    
    def __init__(self,
                 ticker_list: List[str]) -> None:
        """
        constructor for the metrics class

        Args:
            ticker_list (List[str]): a list of stock tickers
        """
        self.ticker_list = ticker_list
        self.weights = []
        
        self.price_data = yf.download(tickers=self.ticker_list, start="1980-01-01", end=datetime.today())
        self.log_returns = self.calc_yearly_log_returns()
        self.yearly_volatility = None
        self.yearly_returns = None
        self.num_assets = None
    
    def calc_yearly_log_returns(self) -> pd.DataFrame:
        """
        calculates the yearly log returns of a portfolio

        Returns:
            pd.DataFrame: log returns of a portfolio of stocks
        """
        self.price_data = self.price_data.drop(columns=['High', 'Low', 'Open', 'Volume', 'Close'])
        self.price_data = self.price_data.droplevel(0, axis=1)
        self.price_data = self.price_data.dropna()
        self.log_returns = np.log(self.price_data / self.price_data.shift(1))
        self.log_returns = self.log_returns.dropna()
        return self.log_returns

    def calc_yearly_portfolio_returns(self) -> pd.DataFrame:
        """
        calculates the normal mean returns of a stock portfolio over a year

        Returns:
            pd.DataFrame: normal returns of a portfolio of stocks
        """
        self.yearly_returns = np.sum(self.log_returns.mean() * self.weights) * 252
        return self.yearly_returns
    
    def calc_yearly_volatility(self) -> pd.DataFrame:
        """
        calculates the yearly volatility of a stock portfolio over a year

        Returns:
            pd.DataFrame: yearly volatility of a portfolio of stocks
        """
        self.yearly_volatility =  np.sqrt(np.dot(np.transpose(self.weights), np.dot(self.log_returns.cov() * 252, self.weights)))
        return self.yearly_volatility
        
    @abstractmethod
    def optimize(self):
        """
        optimizes a portfolio of stocks based on  a child class metric
        """
        pass
    
    @abstractmethod
    def calc_statistics(self):
        """
        calculates statistics returned from the optimizer
        """
        pass
    
        