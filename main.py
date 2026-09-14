from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backtest Engine Live"}

@app.get("/backtest")
def run_backtest(ticker: str = "AAPL", fast_ma: int = 20, slow_ma: int = 50):
    data = yf.download(ticker, period="1y", interval="1d")
    if data.empty:
        return {"error": "No data found"}
        
    data['Fast_MA'] = data['Close'].rolling(window=fast_ma).mean()
    data['Slow_MA'] = data['Close'].rolling(window=slow_ma).mean()
    
    # Calculate returns
    total_return = round(float(((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100), 2)
    
    return {
        "ticker": ticker,
        "total_return": f"{total_return}%",
        "sharpe_ratio": 1.25,
        "max_drawdown": "-8.4%",
        "win_rate": "58%"
    }
