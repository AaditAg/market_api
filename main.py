import yfinance as yf
from fastapi import FastAPI
import pandas as pd
import numpy as np
import json

app = FastAPI()


def clean_obj(obj):
    """Clean objects to make them JSON serializable"""
    # Handle None values
    if obj is None:
        return None

    # Handle DataFrames
    if isinstance(obj, pd.DataFrame):
        # Replace NaN values with None (which becomes null in JSON)
        df_cleaned = obj.replace({np.nan: None})
        return df_cleaned.reset_index().to_dict(orient="records")

    # Handle Series
    if isinstance(obj, pd.Series):
        # Replace NaN values with None
        series_cleaned = obj.replace({np.nan: None})
        return series_cleaned.to_dict()

    # Handle numpy types and NaN values
    if isinstance(obj, (np.int64, np.int32, np.float64, np.float32)):
        if np.isnan(obj):
            return None
        return obj.item()

    # Handle regular Python float NaN
    if isinstance(obj, float) and np.isnan(obj):
        return None

    # Handle dicts recursively to clean any nested NaN values
    if isinstance(obj, dict):
        cleaned_dict = {}
        for key, value in obj.items():
            if isinstance(value, (float, np.floating)) and np.isnan(value):
                cleaned_dict[key] = None
            elif isinstance(value, (np.int64, np.int32, np.float64, np.float32)):
                cleaned_dict[key] = value.item()
            else:
                cleaned_dict[key] = value
        return cleaned_dict

    # Handle lists
    if isinstance(obj, list):
        return [clean_obj(item) for item in obj]

    # Everything else (convert to string for safety)
    return str(obj)


@app.get("/stock")
async def stock_method(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        response = {
            'cmp': clean_obj(stock.info.get('currentPrice')),
            'info': clean_obj(stock.info),
            'calendar': clean_obj(stock.calendar),
            'balance_sheet': clean_obj(stock.balance_sheet),
            'income_stmt': clean_obj(stock.income_stmt),
            'ttm_income_stmt': clean_obj(stock.ttm_income_stmt),
            'quarterly_income_stmt': clean_obj(stock.quarterly_income_stmt),
            'cash_flow': clean_obj(stock.cash_flow),
            'ttm_cash_flow': clean_obj(stock.ttm_cash_flow),
            'quarterly_cash_flow': clean_obj(stock.quarterly_cash_flow),
            'dividends': clean_obj(stock.dividends),
            'splits': clean_obj(stock.splits),
            'actions': clean_obj(stock.actions),
            'recommendations': clean_obj(stock.recommendations),
            'history': clean_obj(stock.history(period='1d')),
            'sustainability': clean_obj(stock.sustainability),
            'institutional_holders': clean_obj(stock.institutional_holders),
            'mutualfund_holders': clean_obj(stock.mutualfund_holders),
        }
        return response
    except Exception as e:
        return {"error": f"Failed to fetch stock data: {str(e)}"}


@app.get("/stock/history")
async def stock_history(ticker: str, period: str = "1d"):
    try:
        stock = yf.Ticker(ticker)
        history_data = stock.history(period=period)
        return clean_obj(history_data)
    except Exception as e:
        return {"error": f"Failed to fetch stock history: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)