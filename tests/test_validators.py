import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price, validate_stop_price
)


class TestValidators(unittest.TestCase):
    
    def test_validate_symbol_valid(self):
        """Test valid symbol validation"""
        self.assertEqual(validate_symbol('BTCUSDT'), 'BTCUSDT')
        self.assertEqual(validate_symbol('btcusdt'), 'BTCUSDT')
        self.assertEqual(validate_symbol('ETHUSDT'), 'ETHUSDT')
    
    def test_validate_symbol_invalid(self):
        """Test invalid symbol validation"""
        with self.assertRaises(ValueError):
            validate_symbol('')
        with self.assertRaises(ValueError):
            validate_symbol('BT')
        with self.assertRaises(ValueError):
            validate_symbol('VERYLONGSYMBOL123')
        with self.assertRaises(ValueError):
            validate_symbol(None)
    
    def test_validate_side_valid(self):
        """Test valid side validation"""
        self.assertEqual(validate_side('BUY'), 'BUY')
        self.assertEqual(validate_side('buy'), 'BUY')
        self.assertEqual(validate_side('SELL'), 'SELL')
        self.assertEqual(validate_side('sell'), 'SELL')
    
    def test_validate_side_invalid(self):
        """Test invalid side validation"""
        with self.assertRaises(ValueError):
            validate_side('HOLD')
        with self.assertRaises(ValueError):
            validate_side('')
    
    def test_validate_order_type_valid(self):
        """Test valid order type validation"""
        self.assertEqual(validate_order_type('MARKET'), 'MARKET')
        self.assertEqual(validate_order_type('market'), 'MARKET')
        self.assertEqual(validate_order_type('LIMIT'), 'LIMIT')
        self.assertEqual(validate_order_type('STOP_MARKET'), 'STOP_MARKET')
    
    def test_validate_order_type_invalid(self):
        """Test invalid order type validation"""
        with self.assertRaises(ValueError):
            validate_order_type('INVALID')
        with self.assertRaises(ValueError):
            validate_order_type('')
    
    def test_validate_quantity_valid(self):
        """Test valid quantity validation"""
        self.assertEqual(validate_quantity(0.001), 0.001)
        self.assertEqual(validate_quantity('0.5'), 0.5)
        self.assertEqual(validate_quantity(10), 10.0)
    
    def test_validate_quantity_invalid(self):
        """Test invalid quantity validation"""
        with self.assertRaises(ValueError):
            validate_quantity(0)
        with self.assertRaises(ValueError):
            validate_quantity(-1)
        with self.assertRaises(ValueError):
            validate_quantity('invalid')
    
    def test_validate_price_limit_order(self):
        """Test price validation for LIMIT orders"""
        self.assertEqual(validate_price(50000, 'LIMIT'), 50000.0)
        self.assertEqual(validate_price('60000', 'LIMIT'), 60000.0)
        
        with self.assertRaises(ValueError):
            validate_price(None, 'LIMIT')
        with self.assertRaises(ValueError):
            validate_price(0, 'LIMIT')
        with self.assertRaises(ValueError):
            validate_price(-100, 'LIMIT')
    
    def test_validate_price_market_order(self):
        """Test price validation for MARKET orders (price not required)"""
        self.assertIsNone(validate_price(None, 'MARKET'))
    
    def test_validate_stop_price_stop_market_order(self):
        """Test stop price validation for STOP_MARKET orders"""
        self.assertEqual(validate_stop_price(50000, 'STOP_MARKET'), 50000.0)
        self.assertEqual(validate_stop_price('60000', 'STOP_MARKET'), 60000.0)
        
        with self.assertRaises(ValueError):
            validate_stop_price(None, 'STOP_MARKET')
        with self.assertRaises(ValueError):
            validate_stop_price(0, 'STOP_MARKET')
        with self.assertRaises(ValueError):
            validate_stop_price(-100, 'STOP_MARKET')
    
    def test_validate_stop_price_market_order(self):
        """Test stop price validation for MARKET orders (not required)"""
        self.assertIsNone(validate_stop_price(None, 'MARKET'))


if __name__ == '__main__':
    unittest.main()
