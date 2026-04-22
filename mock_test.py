import unittest
from unittest.mock import MagicMock, patch
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
import os

class TestTradingBot(unittest.TestCase):
    @patch('bot.client.Client')
    @patch('bot.client.load_dotenv')
    def setUp(self, mock_dotenv, mock_client):
        # Mock environment variables
        os.environ['BINANCE_API_KEY'] = 'mock_key'
        os.environ['BINANCE_API_SECRET'] = 'mock_secret'
        
        self.mock_binance_client = BinanceFuturesClient(testnet=True)
        self.manager = OrderManager(self.mock_binance_client)
        
        # Mock the internal binance client's futures_create_order
        self.mock_binance_client.client.futures_create_order = MagicMock()

    def test_market_order_log_generation(self):
        """Simulate a Market order to generate logs."""
        self.mock_binance_client.client.futures_create_order.return_value = {
            'orderId': 12345678,
            'symbol': 'BTCUSDT',
            'status': 'FILLED',
            'executedQty': '0.001',
            'avgPrice': '65000.00',
            'clientOrderId': 'test_market_1'
        }
        
        print("\nTesting Market Order...")
        result = self.manager.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='MARKET',
            quantity=0.001
        )
        self.assertTrue(result['success'])
        self.assertEqual(result['orderId'], 12345678)

    def test_limit_order_log_generation(self):
        """Simulate a Limit order to generate logs."""
        self.mock_binance_client.client.futures_create_order.return_value = {
            'orderId': 87654321,
            'symbol': 'BTCUSDT',
            'status': 'NEW',
            'executedQty': '0.000',
            'avgPrice': '0.00',
            'clientOrderId': 'test_limit_1'
        }
        
        print("\nTesting Limit Order...")
        result = self.manager.place_order(
            symbol='BTCUSDT',
            side='SELL',
            order_type='LIMIT',
            quantity=0.001,
            price=70000.0
        )
        self.assertTrue(result['success'])
        self.assertEqual(result['orderId'], 87654321)

if __name__ == '__main__':
    unittest.main()
