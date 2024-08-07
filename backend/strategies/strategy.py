from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """
    Abstract class to define methods used from all other stock strategies implemented
    """
    
    @abstractmethod
    def add_ta(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """
        Adds technical analysis to a stock for the strategy

        Args:
            stock_data (pd.DataFrame): a dataframe consisting of stock prices

        Returns:
            pd.DataFrame: a dataframe with the technical analysis as a column
        """
        pass
    
    @abstractmethod
    def filter_by_ta(self) -> None:
        """
        Filters stocks based on the technical analysis for a given strategy
        """
        pass
    
    @abstractmethod
    def generate_buy_signal(self) -> None:
        """
        Adds a column to the dataframe if the current day is a buy signal
        """
        pass
    
    @abstractmethod
    def sell_signal(self) -> None:
        """
        Adds a column to the dataframe if the current day is a sell signal
        """
        pass
    
    @abstractmethod
    def postprocess(self) -> None:
        """
        Formats the data from a buy signal
        """
        pass