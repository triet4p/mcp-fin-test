# Real-time Price Module

The Real-time Price module in the Yahoo Finance service provides the endpoint for retrieving real-time stock price data from Yahoo Finance's API.

## Components

### Real-time API Endpoint (`app/api/realtime.py`)

This module defines the endpoint for retrieving real-time stock prices:

#### `get_stock_realtime_price(ticker: str)` Endpoint

The primary endpoint for fetching real-time stock price data:

1. **Purpose**: Retrieve current price information for a specified stock ticker
2. **Method**: GET
3. **Path**: `/market/tickers/{ticker}/price/realtime`
4. **Parameter**: `ticker` - Stock ticker symbol (e.g., AAPL, MSFT, FPT)
5. **Response**: `StockRealtimePrice` object with price data or error information

### Data Fetching (`app/tools/fetch_realtime_stock.py`)

This module contains the implementation for fetching data from Yahoo Finance:

#### `fetch_stock_realtime_price(ticker: str)` Function

The core function that retrieves real-time stock price data:

1. **Purpose**: Fetch current price information from Yahoo Finance using yfinance
2. **Library**: Uses the `yfinance` library for data retrieval
3. **Performance**: Utilizes `fast_info` for efficient data access
4. **Error Handling**: Comprehensive error handling for various failure scenarios

## Usage Flow

```
API Request → get_stock_realtime_price() → fetch_stock_realtime_price() → 
Yahoo Finance API → Process Response → Return StockRealtimePrice
```

## Data Sources

The module uses the `yfinance` library to access Yahoo Finance's API, which provides:

- Real-time price data
- Intraday high/low prices
- Opening price
- Trading volume
- Timestamp information

## Response Structure

The response follows the `StockRealtimePrice` schema which includes:

### Success Case
- `ticker`: The requested stock ticker symbol
- `open`: Today's opening price
- `day_high`: Highest price of the day
- `day_low`: Lowest price of the day
- `last_price`: Current price
- `last_volume`: Current trading volume
- `ts`: Timestamp of the response

### Error Case
- `ticker`: The requested stock ticker symbol
- `ts`: Timestamp of the response
- `error`: Detailed error message

## Error Handling

The module handles several error scenarios:

1. **Invalid Ticker**: When the ticker symbol doesn't exist or has no data
2. **Network Issues**: Connectivity problems with Yahoo Finance
3. **API Changes**: Changes in Yahoo Finance's API that affect data retrieval
4. **Rate Limiting**: Potential rate limiting by Yahoo Finance

In all error cases, the function returns a `StockRealtimePrice` object with an error message rather than raising an exception.