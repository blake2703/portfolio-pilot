from .strategy import Strategy
import pandas as pd
import pandas_ta
from datetime import datetime, timedelta, time
from bs4 import BeautifulSoup
import requests
import os
import yfinance as yf
import json



COLUMN_HEADINGS = ['Check_box', 'Name', 'Symbol', 'RSf', 'Rtn-1d', 'Rtn-5d', 'Rtn-1mo', 'Rtn-3mo', 'Rtn-6mo', 'Rtn-1yr', '$vol-21']

# this class will need to be on an automated schedule to run, i.e. everyday at 12:50PST
class Rsi2(Strategy):
    
    def __init__(self) -> None:
        """
        Constructor for the Rsi2 class
        
        @scraped_efts: etfs scraped from etf screen
        @stock_data: holds the High, Low, Open, Close, Adj close prices per each for for all stocks in scraped_etfs
        @current_etf_file_storage_path: file path of the last time the scrape function ran
        @new_etf_file_storage_path: current time and data for the current scrape
        @etf_buys_storage_path: file path for the buys for the current day
        """
        
        self.stock_data = None
        self.scraped_etfs = None

        current_timestamp = datetime.now().replace(hour=12, minute=50, second=0, microsecond=0)
        yesterday_timestamp = current_timestamp - timedelta(days=1)
        
        current_timestamp_str = current_timestamp.strftime("%Y%m%d-%H%M")
        yesterday_timestamp_str = yesterday_timestamp.strftime("%Y%m%d-%H%M")
        
        self.current_etf_file_storage_path = f"{os.getcwd()}/{yesterday_timestamp_str}-rsi2_data.csv"
        self.new_etf_file_storage_path = f"{os.getcwd()}/{current_timestamp_str}-rsi2_data.csv"
        self.etf_buys_storage_path = f"{os.getcwd()}/buys.json"
    
    def should_scrape(self) -> bool:
        """
        Determines if it is time to run the scrape function

        Returns:
            bool: True if it is 12:50pm pst and the scrape has not ran, False otherwise
        """
        # extract the date
        day_year = self.current_etf_file_storage_path.split('/')[-1].split('-')[0]
        file_date = datetime.strptime(day_year, '%Y%m%d').date()

        # Get the current date and time
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        # Define the target time for comparison (12:50 PM)
        target_time = time(12, 50)

        # Check if the current day is greater than the file date and the current time is after 12:50 PM
        if current_date > file_date and current_time >= target_time:
            return True
        return False
    
    def remove_previous_day_file(self) -> None:
        """
        Removes the previous day's scraped etf data
        """
        try:
            if os.path.exists(self.current_etf_file_storage_path):
                os.remove(self.current_etf_file_storage_path)
                print(f"Removed file: {self.current_etf_file_storage_path}")
            else:
                print(f"File not found: {self.current_etf_file_storage_path}")
        except Exception as e:
            print(f"Error removing file: {e}")
        

    def scrape(self) -> None: 
        if self.should_scrape():
            self.remove_previous_day_file()
            data_list = []
    
            url = "https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1mo%7Cdesc&t=6&d=i&ftS=yes&ftL=yes&vFf=dolVol21&vFl=gt&vFv=1000000&udc=default&d=i"
            response = requests.get(url=url)
    
            if response.status_code != 200:
                print(f"Error in getting response: {response.status_code}")
                return None
    
            soup = BeautifulSoup(response.content, "html.parser")
            table_div = soup.find('div', class_="ptbl")
    
            if table_div:
                table = table_div.find('table', class_="ptbl")
        
                if table:
                    table_rows = table.find_all('tr')
            
                    for table_row in range(len(table_rows)):
                        curr_row = table_rows[table_row]
                        table_row_data = curr_row.find_all('td')
                        data_dict = {}
                
                        for index, val in enumerate(COLUMN_HEADINGS):
                            if index < len(table_row_data):
                                data_dict[val] = table_row_data[index].text.strip()
                        data_list.append(data_dict)
            
            if len(data_list) == 0:
                print("Error: no data found")
                return None
            
            df = pd.DataFrame.from_dict(data=data_list)
            df = df.drop(index=[0,1])
            
            df.to_csv(self.new_etf_file_storage_path)
    
    def validate_scrape(self) -> None:
        """
        Ensures that all columns are present in the data
        """
        for column in COLUMN_HEADINGS:
            if column == 'Check_box':
                continue
            if column not in self.scraped_etfs.columns:
                raise ValueError(f"Missing required column: {column}")
                
    
    def process_scrape(self) -> None:
        """
        Preprocesses the data that was scraped
        """
        self.scraped_etfs = pd.read_csv(self.new_etf_file_storage_path)
        self.scraped_etfs = self.scraped_etfs.drop(columns=['Check_box'])
        self.validate_scrape()
        
        self.scraped_etfs = self.scraped_etfs[~self.scraped_etfs['Name'].str.contains('vix', case=False)]
        self.scraped_etfs = self.scraped_etfs[~self.scraped_etfs['Name'].str.contains('etn', case=False)]
        
        self.scraped_etfs['RSf'] = self.scraped_etfs['RSf'].astype('float')
        self.scraped_etfs['Rtn-1d'] = self.scraped_etfs['Rtn-1d'].astype('float')
        self.scraped_etfs['Rtn-5d'] = self.scraped_etfs['Rtn-5d'].astype('float')
        self.scraped_etfs['Rtn-1mo'] = self.scraped_etfs['Rtn-1mo'].astype('float')
        self.scraped_etfs['Rtn-3mo'] = self.scraped_etfs['Rtn-3mo'].astype('float')
        self.scraped_etfs['Rtn-6mo'] = self.scraped_etfs['Rtn-6mo'].astype('float')
        self.scraped_etfs['Rtn-1yr'] = self.scraped_etfs['Rtn-1yr'].astype('float')
        
        self.scraped_etfs = self.scraped_etfs[self.scraped_etfs['RSf'] >= 80]
        self.scraped_etfs = self.scraped_etfs.sort_values('Rtn-1mo', ascending=True)
        self.scraped_etfs = self.scraped_etfs[:25] # might need to update this after we test further
        
    
    def set_stock_data(self) -> None:
        """
        Setter that grabs all price data for each etf stock scraped
        """
        ticker_list = self.scraped_etfs['Symbol'].tolist()
        self.stock_data = yf.download(tickers=ticker_list, start=datetime.today() - timedelta(days=365), end=datetime.today())
        self.stock_data = self.stock_data.stack().reset_index().rename(index=str, columns={"level_1": "Ticker"}).sort_values(['Ticker', 'Date'])
        self.stock_data['Date'] = pd.to_datetime(self.stock_data['Date'])
        self.stock_data.set_index('Date', inplace=True)
    
    def add_ta(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        stock_data[['donchian_lower', 'donchian_middle', 'donchian_upper']] = pandas_ta.donchian(
            high=stock_data['High'], # update to high for the real time day
            low=stock_data['Low'], # update to low for the  real time day
            upper_length=55,
            lower_length=55
        )
        
        stock_data['rsi2'] = pandas_ta.rsi(
            close=stock_data['Close'], # need to update to real time price
            length=2
        )
        
        return stock_data
    
    def filter_by_ta(self) -> None:
        self.stock_data = self.stock_data.groupby('Ticker').apply(self.add_ta)
        self.stock_data = self.stock_data.dropna()
        
        self.stock_data['at_donchian_upper'] = self.stock_data['High'] >= self.stock_data['donchian_upper']
        self.stock_data['below_30_rsi2'] = self.stock_data['rsi2'] <= 30
        
        self.stock_data['above_70_rsi2'] = self.stock_data['rsi2'] >= 70
        self.stock_data['buy_signal'] = False
        self.stock_data['sell_signal'] = False
        
    
    def generate_buy_signal(self) -> None:
        for ticker in self.stock_data['Ticker'].unique():
            ticker_data = self.stock_data[self.stock_data['Ticker'] == ticker]
            donchian_upper_days = ticker_data[ticker_data['at_donchian_upper']].index
            
            for upper_day in donchian_upper_days:
                subsequent_days = ticker_data.loc[upper_day:].index
                
                for day in subsequent_days:
                    if ticker_data.loc[day, 'below_30_rsi2']:
                        self.stock_data.loc[day, 'buy_signal'] = True
                        break
    
    def sell_signal(self) -> None:
        pass
    
    def postprocess(self) -> None:
        buys = self.stock_data[self.stock_data['buy_signal'] == True]
        
        buys = buys.drop(columns=['Ticker'])
        buys = buys.reset_index(drop=False)
        buys = buys[['Date', 'Ticker']]
        
        today = pd.Timestamp(datetime.now().date())
        buys = buys[buys['Date'] == today]
        
        with open(self.etf_buys_storage_path, 'w') as file:
            json.dump(buys.to_dict(orient='records'), file)

# rsi2 = Rsi2()
# rsi2.scrape()
# rsi2.process_scrape()
# rsi2.set_stock_data()
# rsi2.filter_by_ta()
# rsi2.generate_buy_signal()
# data = rsi2.postprocess()