import sys

import pandas as pd
import uvicorn
import yfinance as yf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.constants import APP_HOST, APP_PORT, NIFTY50_STOCKS, SEQUENCE_WINDOW_SIZE
from src.exception import MyException
from src.logger import logging
from src.pipeline.prediction_pipeline import StockData, StockDataClassifier
from src.pipeline.training_pipeline import TrainPipeline

app = FastAPI(title="NIFTY-50 Stock Forecasting API")


class PredictRequest(BaseModel):
    ticker: str = Field(..., description="NIFTY-50 ticker symbol, e.g. RELIANCE.NS")


class PredictResponse(BaseModel):
    ticker: str
    predicted_30d_return_pct: float


class TrainingResponse(BaseModel):
    status: str


@app.get("/", summary="List available tickers")
def index():
    return {"message": "NIFTY-50 Stock Forecasting API", "tickers": NIFTY50_STOCKS}


@app.get("/training", response_model=TrainingResponse, summary="Retrain the model")
def training():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return TrainingResponse(status="Training successful")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"Error occurred during training: {str(e)}")


@app.post("/predict", response_model=PredictResponse, summary="Predict 30-day forward return")
def predict(request: PredictRequest):
    try:
        if request.ticker not in NIFTY50_STOCKS:
            raise HTTPException(
                status_code=400,
                detail=f"'{request.ticker}' is not a valid NIFTY-50 ticker.",
            )

        lookback_days = SEQUENCE_WINDOW_SIZE + 30
        history = yf.download(
            request.ticker,
            period=f"{lookback_days + 30}d",
            progress=False,
            auto_adjust=True,
        )
        if isinstance(history.columns, pd.MultiIndex):
            history.columns = history.columns.get_level_values(0)
        history = history.tail(lookback_days + 21).reset_index()
        history.rename(columns={"Date": "date"}, inplace=True)

        stock_data = StockData(ticker=request.ticker, recent_ohlcv=history)
        classifier = StockDataClassifier()
        predicted_return = classifier.predict(stock_data)

        return PredictResponse(
            ticker=request.ticker,
            predicted_30d_return_pct=round(predicted_return * 100, 2),
        )

    except HTTPException:
        raise
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)