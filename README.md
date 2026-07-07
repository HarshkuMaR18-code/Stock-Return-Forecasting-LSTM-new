# 📈 Stock Return Forecasting using Deep Learning (CNN + LSTM)

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=for-the-badge&logo=tensorflow)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas)

</p>

---

## 📌 Project Overview

This project predicts the **30-day forward stock return (%)** for **NIFTY-50 companies** using a hybrid **CNN + LSTM Deep Learning architecture**.

Instead of training on a single stock, the model learns from the historical data of **all NIFTY-50 stocks**, allowing it to capture common market patterns and improve generalization.

The trained model is deployed using **FastAPI**, enabling real-time predictions through REST APIs.

---

# 🚀 Features

- 📊 Uses historical data of all NIFTY-50 stocks
- 📈 Predicts 30-Day Future Return
- 🧠 Hybrid CNN + LSTM Deep Learning Model
- 🔢 Stock Embedding Layer
- 📉 Technical Indicator Engineering
- ⚡ FastAPI Deployment
- 🔄 Automated Training Pipeline
- 📦 Modular Project Structure
- 📖 Interactive Swagger API Documentation

---

# 🏗️ Project Architecture

```
Market Data (Yahoo Finance)
            │
            ▼
Data Ingestion
            │
            ▼
Data Validation
            │
            ▼
Feature Engineering
            │
            ▼
Data Transformation
            │
            ▼
CNN + LSTM Model
            │
            ▼
Model Evaluation
            │
            ▼
Saved Model (.keras)
            │
            ▼
FastAPI Prediction API
```

---

# 🧠 Model Architecture

The model combines both convolutional and recurrent neural networks.

```
Historical OHLCV Data
            │
            ▼
Feature Engineering
            │
            ▼
Conv1D
            │
            ▼
Conv1D
            │
            ▼
LSTM
            │
            ▼
Dropout
            │
            ▼
Ticker Embedding
            │
            ▼
Concatenation
            │
            ▼
Dense Layer
            │
            ▼
Output
(30-Day Return)
```

---

# 📊 Features Used

The model is trained using:

- Close Price
- Volume
- Daily Return
- 7-Day Moving Average
- 21-Day Moving Average
- 7-Day Volatility
- Stock Embedding

---

# 🎯 Prediction Target

The model predicts

```
Future Return (%) after 30 Trading Days
```

Target formula:

```python
target = (Future_Close / Current_Close) - 1
```

---

# ⚙️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Deep Learning | TensorFlow / Keras |
| API | FastAPI |
| Data | Pandas, NumPy |
| ML Utilities | Scikit-Learn |
| Data Source | Yahoo Finance |
| Server | Uvicorn |

---

# 📂 Project Structure

```
Stock-Return-Forecasting/

│
├── artifact/
│
├── config/
│
├── notebook/
│
├── src/
│   ├── components/
│   ├── pipeline/
│   ├── utils/
│   ├── constants.py
│   ├── logger.py
│   └── exception.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Stock-Return-Forecasting.git

cd Stock-Return-Forecasting
```

Create virtual environment

```bash
python -m venv stock
```

Activate

### Windows

```bash
stock\Scripts\activate
```

### Linux / Mac

```bash
source stock/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Train Model

```bash
python src/pipeline/training_pipeline.py
```

This will

- Download stock data
- Perform preprocessing
- Engineer features
- Train CNN + LSTM model
- Save model
- Save scaler

---

# 🌐 Run API

```bash
python app.py
```

or

```bash
uvicorn app:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 📌 API Endpoints

## Home

```
GET /
```

Returns available NIFTY-50 tickers.

---

## Train Model

```
GET /training
```

Retrains the model.

---

## Predict

```
POST /predict
```

Example Request

```json
{
    "ticker":"RELIANCE.NS"
}
```

Example Response

```json
{
    "ticker":"RELIANCE.NS",
    "predicted_30d_return_pct":0.54
}
```

---

# 📈 Example Predictions

| Stock | Predicted 30-Day Return |
|--------|------------------------|
| RELIANCE.NS | 0.54 % |
| TCS.NS | 1.34 % |
| INFY.NS | 0.82 % |

---

# 📌 Future Improvements

- Transformer-based forecasting
- Attention Mechanism
- Sentiment Analysis Integration
- Hyperparameter Optimization
- Docker Deployment
- CI/CD Pipeline
- Cloud Deployment (AWS/GCP)

---

# 👨‍💻 Author

**Harsh Kumar**

AI & Data Science Undergraduate

NIT Kurukshetra

---

# ⭐ If you found this project useful

Please consider giving this repository a ⭐ on GitHub.
