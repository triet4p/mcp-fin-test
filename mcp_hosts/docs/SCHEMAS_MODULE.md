# Schemas Module

The Schemas module contains auto-generated Pydantic models for data validation when interacting with external services. These models ensure type safety and proper data serialization/deserialization.

## Structure

The schemas are organized by provider:

- **ITAPIA** (`itapia.py`): Complex financial analysis schemas
- **YF** (`yf.py`): Yahoo Finance real-time price schemas

## Auto-generation

These schemas are auto-generated using `datamodel-codegen` from API specifications. This ensures they stay in sync with the external services they represent.

## Key Schema Types

### ITAPIA Schemas

ITAPIA provides comprehensive financial analysis capabilities:

- **AdvisorResponse**: Final investment recommendations with risk assessment
- **TechnicalReport**: Detailed technical analysis reports
- **ForecastingReport**: Price movement predictions with confidence levels
- **NewsAnalysisReport**: Sentiment analysis of relevant financial news
- **ProfileResponse**: User investment profile information

### YF Schemas

YF (Yahoo Finance) schemas handle real-time price data:

- **StockRealtimePrice**: Current price information for stock tickers

## Usage

These schemas are used throughout the application for:

1. **Data Validation**: Ensuring API responses match expected formats
2. **Type Safety**: Providing IDE support and preventing type-related errors
3. **Serialization**: Converting between Python objects and JSON
4. **Documentation**: Serving as a contract for data structures

## Maintenance

When external service APIs change, the schemas should be regenerated to maintain compatibility.