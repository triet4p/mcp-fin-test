# Yahoo Finance (YF) Module

The Yahoo Finance module is a service that provides real-time stock price data by fetching information from Yahoo Finance's API. It exposes a simple REST API endpoint that can be used by other services in the MCP ecosystem.

## Overview

The YF service is a FastAPI application that provides a single endpoint for retrieving real-time stock price information. It uses the `yfinance` library to fetch data from Yahoo Finance and returns structured responses with proper error handling.

## Components

### Core Configuration (`app/core`)

The core configuration module handles application settings through environment variables:

- `API_V1_BASE_ROUTE`: Base route for API endpoints (default: `/api/v1`)

### API Endpoints (`app/api`)

The API module provides FastAPI endpoints for external interaction:

1. **Health Check** (`/health`): Application status monitoring
2. **Real-time Price** (`/market/tickers/{ticker}/price/realtime`): Fetch real-time stock price data

### Data Schemas (`app/schemas.py`)

The schemas module defines the Pydantic models used for data validation and serialization:

- `StockRealtimePrice`: Schema for real-time stock price data including error handling

### Data Fetching (`app/tools`)

The tools module contains the business logic for fetching data from Yahoo Finance:

- `fetch_realtime_stock.py`: Implementation for retrieving real-time stock price data

## Usage

To fetch real-time stock price data, make a GET request to the endpoint:

```
GET /api/v1/market/tickers/{ticker}/price/realtime
```

Replace `{ticker}` with the desired stock ticker symbol (e.g., AAPL, MSFT, FPT).

## Response Format

The response follows the `StockRealtimePrice` schema:

### Success Response

```json
{
  "ticker": "AAPL",
  "open": 150.25,
  "day_high": 152.30,
  "day_low": 149.80,
  "last_price": 151.75,
  "last_volume": 1250000,
  "ts": 1640995200
}
```

### Error Response

```json
{
  "ticker": "INVALID",
  "ts": 1640995200,
  "error": "No real-time trading data found for ticker 'INVALID'."
}
```

## Error Handling

The service handles various error conditions:

1. **Invalid Ticker**: Returns an error message when the ticker symbol is not found
2. **Network Issues**: Returns an error message when there are connectivity problems
3. **API Issues**: Returns an error message when Yahoo Finance API returns unexpected data

## Limitations

1. **Real-time Only**: The service only provides real-time data, not historical data
2. **No News/Reports**: The service does not fetch news or financial reports
3. **Rate Limiting**: Yahoo Finance may impose rate limits on API requests

## Documentation
- [REALTIME_MODULE](docs/REALTIME_MODULE.md)