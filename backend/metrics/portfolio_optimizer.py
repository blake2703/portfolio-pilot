from abc import ABC, abstractmethod
from typing import List
import yfinance as yf
import pandas as pd

class PortfolioOptimizer(ABC):
    
    def __init__(self,
                 ticker_list: List[str]) -> None:
        
        self.ticker_list = ticker_list
    
        self.price_data = yf.download(tickers=self.ticker_list, period="max")['Close'].dropna()
    
    @abstractmethod
    def optimize_portfolio(self,
                           risk_free_rate: float):
        pass
    
    @abstractmethod
    def maximize_ratio(self,
                       mean_returns: pd.DataFrame,
                       covar_returns: pd.DataFrame,
                       risk_free_rate: float,
                       n_holdings: int):
        pass
                       
        
        