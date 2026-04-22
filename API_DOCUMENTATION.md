# Trading Bot API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Trading Bot API is running"
}
```

---

### 2. Ping Binance
**GET** `/api/client/ping`

Check connection to Binance Futures.

**Response:**
```json
{
  "success": true,
  "message": "Connected to Binance"
}
```

---

### 3. Get Account Balance
**GET** `/api/client/balance`

Fetch USDT balance from Binance Futures account.

**Response:**
```json
{
  "success": true,
  "balance": {
    "asset": "USDT",
    "balance": "1000.00",
    "availableBalance": "1000.00"
  }
}
```

---

### 4. Place Order
**POST** `/api/orders/place`

Place a new order on Binance Futures.

**Request Body:**
```json
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "type": "MARKET",
  "quantity": 0.001
}
```

**For LIMIT orders:**
```json
{
  "symbol": "BTCUSDT",
  "side": "SELL",
  "type": "LIMIT",
  "quantity": 0.001,
  "price": 70000
}
```

**For STOP_MARKET orders:**
```json
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "type": "STOP_MARKET",
  "quantity": 0.001,
  "stop_price": 65000
}
```

**Response:**
```json
{
  "success": true,
  "orderId": 12345678,
  "status": "FILLED",
  "executedQty": "0.001",
  "avgPrice": "65000.00",
  "clientOrderId": "abc123"
}
```

---

### 5. Get Order Status
**GET** `/api/orders/<symbol>/<order_id>`

Get the status of a specific order.

**Example:**
```
GET /api/orders/BTCUSDT/12345678
```

**Response:**
```json
{
  "success": true,
  "order": {
    "orderId": 12345678,
    "symbol": "BTCUSDT",
    "status": "FILLED",
    "executedQty": "0.001",
    "avgPrice": "65000.00"
  }
}
```

---

### 6. Order Summary
**POST** `/api/orders/summary`

Get a summary report of a placed order.

**Request Body:**
```json
{
  "order": {
    "orderId": 12345678,
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "status": "FILLED",
    "executedQty": "0.001",
    "avgPrice": "65000.00",
    "clientOrderId": "abc123"
  }
}
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "order_id": 12345678,
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "status": "FILLED",
    "quantity": "0.001",
    "price": "65000.00",
    "client_order_id": "abc123"
  }
}
```

---

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your `.env` file with Binance API credentials.

3. Start the API server:
```bash
python api.py
```

The API will be available at `http://localhost:5000`

---

## Testing with cURL

### Place a Market Order:
```bash
curl -X POST http://localhost:5000/api/orders/place \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.001
  }'
```

### Get Balance:
```bash
curl http://localhost:5000/api/client/balance
```

### Ping Binance:
```bash
curl http://localhost:5000/api/client/ping
```
