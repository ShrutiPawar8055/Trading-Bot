import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv
from .logging_config import logger

load_dotenv()

class BinanceFuturesClient:
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        self.testnet = testnet
        
        if not self.api_key or not self.api_secret:
            logger.error("API Key or Secret missing. Please check your .env file.")
            raise ValueError("API Key and Secret are required.")
            
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            if self.testnet:
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
            
            logger.info(f"Binance Futures Client initialized (Testnet={self.testnet})")
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {str(e)}")
            raise

    def ping(self):
        """Check connection to Binance."""
        try:
            self.client.futures_ping()
            return True
        except Exception as e:
            logger.error(f"Ping failed: {str(e)}")
            return False

    def get_account_balance(self):
        """Fetch account balance for USDT."""
        try:
            balances = self.client.futures_account_balance()
            for balance in balances:
                if balance['asset'] == 'USDT':
                    return balance
            return None
        except BinanceAPIException as e:
            logger.error(f"API Error fetching balance: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching balance: {str(e)}")
            raise
