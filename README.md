# Simplified Binance Futures Trading Bot

A Python-based trading bot for placing orders on the Binance Futures Testnet (USDT-M).

## Features
- Place Market and Limit orders.
- Support for BUY and SELL sides.
- Enhanced CLI UX with `questionary`.
- Structured logging for API requests and errors.
- Robust error handling and input validation.

## Prerequisites
- Python 3.8 or higher.
- Binance Futures Testnet account and API credentials.

## Setup
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd trading_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Binance Testnet API Key and Secret.

## How to Run
The bot can be run via the CLI. It supports both interactive mode and direct command arguments.

### Interactive Mode
Simply run the script without arguments:
```bash
python cli.py
```

### Command Arguments
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

## Logging
All API interactions and errors are logged to `trading_bot.log` in the project root.

## Project Structure
- `bot/`: Core logic
  - `client.py`: Binance API client wrapper.
  - `orders.py`: Order placement and management.
  - `validators.py`: Input validation logic.
  - `logging_config.py`: Centralized logging setup.
- `cli.py`: Command-line interface entry point.
