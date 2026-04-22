import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.orders import OrderManager
from binance.exceptions import BinanceAPIException, BinanceOrderException


class TestOrderManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_client = Mock()
        self.mock_binance_client = Mock()
        self.mock_binance_client.client = self.mock_client
        self.order_manager = OrderManager(self.mock_binance_client)
    
    def test_place_market_order_success(self):
        """Test successful market order placement"""
        self.mock_client.futures_create_order.return_value = {
            'orderId': 12345,
            'symbol': 'BTCUSDT',
            'status': 'FILLED',
            'executedQty': '0.001',
            'avgPrice': '65000.00',
            'clientOrderId': 'test123'
        }
        
        result = self.order_manager.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='MARKET',
            quantity=0.001
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['orderId'], 12345)
        self.assertEqual(result['status'], 'FILLED')
        self.mock_client.futures_create_order.assert_called_once()
    
    def test_place_limit_order_success(self):
        """Test successful limit order placement"""
        self.mock_client.futures_create_order.return_value = {
            'orderId': 67890,
            'symbol': 'ETHUSDT',
            'status': 'NEW',
            'executedQty': '0.000',
            'avgPrice': '0.00',
            'clientOrderId': 'test456'
        }
        
        result = self.order_manager.place_order(
            symbol='ETHUSDT',
            side='SELL',
            order_type='LIMIT',
            quantity=0.1,
            price=3000
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['orderId'], 67890)
        self.assertEqual(result['status'], 'NEW')
    
    def test_place_stop_market_order_success(self):
        """Test successful stop market order placement"""
        self.mock_client.futures_create_order.return_value = {
            'orderId': 11111,
            'symbol': 'BTCUSDT',
            'status': 'NEW',
            'executedQty': '0.000',
            'avgPrice': '0.00',
            'clientOrderId': 'test789'
        }
        
        result = self.order_manager.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='STOP_MARKET',
            quantity=0.001,
            stop_price=64000
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['orderId'], 11111)
    
    def test_place_order_validation_error(self):
        """Test order placement with validation error"""
        result = self.order_manager.place_order(
            symbol='',
            side='BUY',
            order_type='MARKET',
            quantity=0.001
        )
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_place_order_binance_api_exception(self):
        """Test order placement with Binance API exception"""
        self.mock_client.futures_create_order.side_effect = BinanceAPIException(
            response=Mock(),
            status_code=400,
            text='{"code":-1021,"msg":"Timestamp for this request is outside of the recvWindow."}'
        )
        
        result = self.order_manager.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='MARKET',
            quantity=0.001
        )
        
        self.assertFalse(result['success'])
        self.assertIn('Binance API Error', result['error'])
    
    def test_place_limit_order_without_price(self):
        """Test limit order without price (should fail validation)"""
        result = self.order_manager.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='LIMIT',
            quantity=0.001,
            price=None
        )
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_place_stop_market_order_without_stop_price(self):
        """Test stop market order without stop price (should fail validation)"""
        result = self.order_manager.place_order(
            symbol='BTCUSDT',
            side='BUY',
            order_type='STOP_MARKET',
            quantity=0.001,
            stop_price=None
        )
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_get_order_status_success(self):
        """Test successful order status retrieval"""
        self.mock_client.futures_get_order.return_value = {
            'orderId': 12345,
            'symbol': 'BTCUSDT',
            'status': 'FILLED',
            'executedQty': '0.001',
            'avgPrice': '65000.00'
        }
        
        result = self.order_manager.get_order_status('BTCUSDT', 12345)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['orderId'], 12345)
        self.assertEqual(result['status'], 'FILLED')
    
    def test_get_order_status_error(self):
        """Test order status retrieval with error"""
        self.mock_client.futures_get_order.side_effect = Exception('Order not found')
        
        result = self.order_manager.get_order_status('BTCUSDT', 99999)
        
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
