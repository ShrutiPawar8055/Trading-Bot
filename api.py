from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from bot.client import BinanceFuturesClient
from bot.client_pool import get_client_pool
from bot.orders import OrderManager
from bot.logging_config import logger
from config import get_config

config = get_config()
app = Flask(__name__)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[f"{config.RATE_LIMIT_PER_MINUTE} per minute"] if config.RATE_LIMIT_ENABLED else [],
    storage_uri="memory://"
)

# Initialize client pool
client_pool = get_client_pool(
    pool_size=5,
    api_key=config.BINANCE_API_KEY,
    api_secret=config.BINANCE_API_SECRET,
    testnet=config.TESTNET
)


def require_api_key(f):
    """Decorator for API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not config.API_KEY_REQUIRED:
            return f(*args, **kwargs)
        
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            logger.warning(f"Missing API key from {get_remote_address()}")
            return jsonify({
                'success': False,
                'error': 'API key required. Provide X-API-Key header.'
            }), 401
        
        if api_key != config.API_KEY:
            logger.warning(f"Invalid API key from {get_remote_address()}")
            return jsonify({
                'success': False,
                'error': 'Invalid API key'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function


def handle_errors(f):
    """Decorator for consistent error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error in {f.__name__}: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500
    return decorated_function


def get_client():
    """Get a client from the pool"""
    return client_pool.get_client()


def return_client(client):
    """Return a client to the pool"""
    client_pool.return_client(client)


@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Trading Bot API',
        'version': '1.0',
        'environment': config.__class__.__name__,
        'endpoints': {
            'health': '/health',
            'ping': '/api/client/ping',
            'balance': '/api/client/balance',
            'place_order': '/api/orders/place (POST)',
            'order_status': '/api/orders/<symbol>/<order_id>',
            'order_summary': '/api/orders/summary (POST)'
        },
        'authentication': 'Required' if config.API_KEY_REQUIRED else 'Not required',
        'rate_limiting': 'Enabled' if config.RATE_LIMIT_ENABLED else 'Disabled',
        'documentation': 'See API_DOCUMENTATION.md for details'
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Trading Bot API is running',
        'environment': config.__class__.__name__
    }), 200


@app.route('/api/client/ping', methods=['GET'])
@require_api_key
@handle_errors
def ping_binance():
    """Check connection to Binance"""
    client = get_client()
    try:
        result = client.ping()
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Connected to Binance'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to connect to Binance'
            }), 500
    finally:
        return_client(client)


@app.route('/api/client/balance', methods=['GET'])
@require_api_key
@handle_errors
def get_balance():
    """Get account balance"""
    client = get_client()
    try:
        balance = client.get_account_balance()
        
        if balance:
            return jsonify({
                'success': True,
                'balance': balance
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No USDT balance found'
            }), 404
    finally:
        return_client(client)


@app.route('/api/orders/place', methods=['POST'])
@require_api_key
@limiter.limit("10 per minute")
@handle_errors
def place_order():
    """Place a new order"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body must be JSON'
        }), 400
    
    symbol = data.get('symbol')
    side = data.get('side')
    order_type = data.get('type')
    quantity = data.get('quantity')
    price = data.get('price')
    stop_price = data.get('stop_price')
    
    if not all([symbol, side, order_type, quantity]):
        return jsonify({
            'success': False,
            'error': 'Missing required fields: symbol, side, type, quantity'
        }), 400
    
    client = get_client()
    try:
        manager = OrderManager(client)
        
        result = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=float(quantity),
            price=float(price) if price else None,
            stop_price=float(stop_price) if stop_price else None
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    finally:
        return_client(client)


@app.route('/api/orders/<symbol>/<int:order_id>', methods=['GET'])
@require_api_key
@handle_errors
def get_order_status(symbol, order_id):
    """Get order status"""
    client = get_client()
    try:
        manager = OrderManager(client)
        
        order = manager.get_order_status(symbol, order_id)
        
        if order:
            return jsonify({
                'success': True,
                'order': order
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
    finally:
        return_client(client)


@app.route('/api/orders/summary', methods=['POST'])
@require_api_key
@handle_errors
def order_summary():
    """Get summary report of placed order"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body must be JSON'
        }), 400
    
    order_data = data.get('order')
    
    if not order_data:
        return jsonify({
            'success': False,
            'error': 'Order data required'
        }), 400
    
    summary = {
        'success': True,
        'summary': {
            'order_id': order_data.get('orderId'),
            'symbol': order_data.get('symbol'),
            'side': order_data.get('side'),
            'type': order_data.get('type'),
            'status': order_data.get('status'),
            'quantity': order_data.get('executedQty', order_data.get('quantity')),
            'price': order_data.get('avgPrice', order_data.get('price')),
            'client_order_id': order_data.get('clientOrderId')
        }
    }
    
    return jsonify(summary), 200


if __name__ == '__main__':
    app.run(
        debug=config.API_DEBUG,
        host=config.API_HOST,
        port=config.API_PORT
    )
