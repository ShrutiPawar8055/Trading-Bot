import re

def validate_symbol(symbol):
    """Validates the trading symbol (e.g., BTCUSDT)."""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string.")
    
    if not re.match(r'^[A-Z0-9]{3,12}$', symbol.upper()):
        raise ValueError(f"Invalid symbol format: {symbol}")
    
    return symbol.upper()

def validate_side(side):
    """Validates order side (BUY/SELL)."""
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type):
    """Validates order type (MARKET/LIMIT/STOP_MARKET)."""
    order_type = order_type.upper()
    allowed_types = ['MARKET', 'LIMIT', 'STOP_MARKET']
    if order_type not in allowed_types:
        raise ValueError(f"Order type must be one of: {', '.join(allowed_types)}")
    return order_type

def validate_quantity(quantity):
    """Validates order quantity."""
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return qty
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity: {quantity}. Must be a positive number.")

def validate_price(price, order_type):
    """Validates price, required for LIMIT orders."""
    if order_type.upper() == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be greater than zero.")
            return p
        except (ValueError, TypeError):
            raise ValueError(f"Invalid price: {price}. Must be a positive number.")
    return price

def validate_stop_price(stop_price, order_type):
    """Validates stop price, required for STOP_MARKET orders."""
    if order_type.upper() == 'STOP_MARKET':
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        try:
            sp = float(stop_price)
            if sp <= 0:
                raise ValueError("Stop price must be greater than zero.")
            return sp
        except (ValueError, TypeError):
            raise ValueError(f"Invalid stop price: {stop_price}. Must be a positive number.")
    return stop_price
