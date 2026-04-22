import click
import questionary
from tabulate import tabulate
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.logging_config import logger

def print_summary(data, title="Order Summary"):
    """Prints a pretty table summary."""
    click.echo(f"\n{'='*20} {title} {'='*20}")
    if isinstance(data, dict):
        table_data = [[k, v] for k, v in data.items() if k != 'full_response']
        click.echo(tabulate(table_data, tablefmt="grid"))
    else:
        click.echo(data)
    click.echo('='*50)

def interactive_mode():
    """Runs the bot in interactive mode using questionary."""
    click.echo("Welcome to the Binance Futures Trading Bot (Testnet)!")
    
    symbol = questionary.text(
        "Enter Trading Symbol (e.g., BTCUSDT):",
        default="BTCUSDT",
        validate=lambda text: len(text) > 0 or "Symbol cannot be empty"
    ).ask()

    side = questionary.select(
        "Select Side:",
        choices=["BUY", "SELL"]
    ).ask()

    order_type = questionary.select(
        "Select Order Type:",
        choices=["MARKET", "LIMIT", "STOP_MARKET"]
    ).ask()

    quantity = questionary.text(
        "Enter Quantity:",
        validate=lambda text: text.replace('.', '', 1).isdigit() or "Must be a number"
    ).ask()

    price = None
    if order_type == 'LIMIT':
        price = questionary.text(
            "Enter Limit Price:",
            validate=lambda text: text.replace('.', '', 1).isdigit() or "Must be a number"
        ).ask()
    
    stop_price = None
    if order_type == 'STOP_MARKET':
        stop_price = questionary.text(
            "Enter Stop Price:",
            validate=lambda text: text.replace('.', '', 1).isdigit() or "Must be a number"
        ).ask()

    confirm = questionary.confirm(f"Place {order_type} {side} order for {quantity} {symbol}?").ask()
    
    if confirm:
        return {
            'symbol': symbol,
            'side': side,
            'order_type': order_type,
            'quantity': float(quantity),
            'price': float(price) if price else None,
            'stop_price': float(stop_price) if stop_price else None
        }
    return None

@click.command()
@click.option('--symbol', help='Trading symbol (e.g., BTCUSDT)')
@click.option('--side', type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Order side')
@click.option('--type', 'order_type', type=click.Choice(['MARKET', 'LIMIT', 'STOP_MARKET'], case_sensitive=False), help='Order type')
@click.option('--quantity', type=float, help='Order quantity')
@click.option('--price', type=float, help='Order price (required for LIMIT)')
@click.option('--stop-price', type=float, help='Stop price (required for STOP_MARKET)')
def main(symbol, side, order_type, quantity, price, stop_price):
    """Binance Futures Trading Bot CLI"""
    
    # If no arguments provided, enter interactive mode
    if not any([symbol, side, order_type, quantity]):
        inputs = interactive_mode()
        if not inputs:
            click.echo("Order cancelled.")
            return
        symbol = inputs['symbol']
        side = inputs['side']
        order_type = inputs['order_type']
        quantity = inputs['quantity']
        price = inputs['price']
        stop_price = inputs['stop_price']

    try:
        # Initialize client and manager
        client = BinanceFuturesClient()
        manager = OrderManager(client)

        # Place order
        result = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )

        if result['success']:
            print_summary(result, "Order Success Details")
        else:
            print_summary(result['error'], "Order Failure Details")

    except Exception as e:
        logger.error(f"CLI Error: {str(e)}")
        click.echo(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
