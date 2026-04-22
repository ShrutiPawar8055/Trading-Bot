# Simplified Binance Futures Trading Bot

A Python-based trading bot for placing orders on the Binance Futures Testnet (USDT-M).

## Features
- Place Market and Limit orders.
- Support for BUY and SELL sides.
- Enhanced CLI UX with `questionary`.
- Structured logging for API requests and errors.
- Robust error handling and input validation.

## Prerequisites
- Python 3.8 or higher
- Binance Futures Testnet account and API credentials
  - Get testnet API keys from: https://testnet.binancefuture.com

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/ShrutiPawar8055/Trading-Bot.git
cd trading_bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your Binance Testnet API credentials:
```
BINANCE_API_KEY=your_actual_testnet_api_key
BINANCE_API_SECRET=your_actual_testnet_secret
```

**Important:** Never commit your `.env` file to version control.

## How to Run
The bot can be run via the CLI or as a REST API server.

### CLI Mode

#### Interactive Mode
Simply run the script without arguments:
```bash
python cli.py
```

#### Command Arguments
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

### API Mode

Start the REST API server:
```bash
python api.py
```

The API will be available at `http://localhost:5000`

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API endpoint documentation.

## Logging
All API interactions and errors are logged to `trading_bot.log` in the project root.

## Testing

### Run Unit Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=bot --cov-report=html

# Run specific test file
pytest tests/test_validators.py
```

### Test Coverage
After running tests with coverage, open `htmlcov/index.html` in your browser to view detailed coverage report.

### Manual Testing

1. **Test CLI (Interactive)**:
```bash
python cli.py
```

2. **Test API**:
```bash
# Start the API server
python api.py

# In another terminal, test the health endpoint
curl http://localhost:5000/health
```

## Configuration

### Environment Variables

The bot supports multiple environments (development, production, test). Configure via `.env` file:

```bash
# Environment: development, production, test
ENVIRONMENT=development

# Binance Configuration
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret
TESTNET=true

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60

# API Authentication
API_KEY_REQUIRED=false
API_KEY=your-secure-api-key-here

# Logging
LOG_FILE=trading_bot.log
LOG_LEVEL=INFO
```

### Environment-Specific Settings

**Development** (default):
- Debug mode enabled
- Testnet enabled
- Rate limiting disabled
- API authentication disabled

**Production**:
- Debug mode disabled
- Testnet disabled (uses real Binance)
- Rate limiting enabled
- API authentication required

**Test**:
- Testnet enabled
- Debug disabled
- Rate limiting disabled
- API authentication disabled

## API Authentication

When `API_KEY_REQUIRED=true`, all API requests must include the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secure-api-key-here" \
  http://localhost:5000/api/client/ping
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- Default: 60 requests per minute per IP
- Order placement: 10 requests per minute per IP
- Configure via `RATE_LIMIT_PER_MINUTE` in `.env`

## Project Structure
```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client wrapper
│   ├── client_pool.py     # Connection pooling
│   ├── orders.py          # Order placement and management
│   ├── validators.py      # Input validation logic
│   └── logging_config.py  # Centralized logging setup
├── tests/
│   ├── __init__.py
│   ├── test_validators.py # Validator unit tests
│   └── test_orders.py     # Order manager unit tests
├── api.py                 # REST API server
├── cli.py                 # Command-line interface
├── config.py              # Environment configuration
├── requirements.txt       # Python dependencies
├── pytest.ini             # Pytest configuration
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── API_DOCUMENTATION.md  # API endpoint documentation
```

## Testing

To verify your setup works:

1. **Test CLI (Interactive)**:
```bash
python cli.py
```

2. **Test API**:
```bash
# Start the API server
python api.py

# In another terminal, test the health endpoint
curl http://localhost:5000/health
```

## Owner: Shruti Pawar
