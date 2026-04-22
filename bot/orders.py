from binance.exceptions import BinanceAPIException, BinanceOrderException
from .logging_config import logger
from .validators import (
    validate_symbol, validate_side, validate_order_type, 
    validate_quantity, validate_price
)

class OrderManager:
    def __init__(self, binance_client):
        self.client = binance_client.client

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """
        Places an order on Binance Futures.
        """
        try:
            # Validate inputs
            symbol = validate_symbol(symbol)
            side = validate_side(side)
            order_type = validate_order_type(order_type)
            quantity = validate_quantity(quantity)
            price = validate_price(price, order_type)

            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }

            if order_type == 'LIMIT':
                params['price'] = price
                params['timeInForce'] = 'GTC'  # Good Till Cancelled
            
            if order_type == 'STOP_MARKET':
                if stop_price is None:
                    raise ValueError("Stop price is required for STOP_MARKET orders.")
                params['stopPrice'] = stop_price

            logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}...")
            logger.debug(f"Order Params: {params}")

            # Execute order
            response = self.client.futures_create_order(**params)
            
            logger.info(f"Order placed successfully! Order ID: {response.get('orderId')}")
            logger.debug(f"API Response: {response}")
            
            return {
                'success': True,
                'orderId': response.get('orderId'),
                'status': response.get('status'),
                'executedQty': response.get('executedQty'),
                'avgPrice': response.get('avgPrice'),
                'clientOrderId': response.get('clientOrderId'),
                'full_response': response
            }

        except BinanceAPIException as e:
            error_msg = f"Binance API Error: {e.status_code} - {e.message}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except BinanceOrderException as e:
            error_msg = f"Binance Order Error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"Unexpected Error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}

    def get_order_status(self, symbol, order_id):
        """Fetches status of a specific order."""
        try:
            response = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            return response
        except Exception as e:
            logger.error(f"Error fetching order status: {str(e)}")
            return None
