from fastapi import FastAPI, HTTPException
import yfinance as yf
from cachetools import TTLCache
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any
from openai import OpenAI
from config import NEMO_API_KEY, NEMO_MODEL, NEMO_API_URL, API_TIMEOUT, MAX_TOKENS, TEMPERATURE, CACHE_TTL, CACHE_MAX_SIZE,LOG_LEVEL, DEBUG, validate_config

app = FastAPI()

# Validate configuration on startup
validate_config()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, will restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = TTLCache(maxsize=100, ttl=10)

@app.get("/api/price/{symbol}")
def get_price(symbol: str):
    if symbol in cache:
        return cache[symbol]

    ticker = yf.Ticker(symbol.upper())
    data = ticker.history(period="2d", interval="1d")

    if data.empty or len(data) < 2:
        raise HTTPException(status_code=404, detail="Ticker not found")

    # Get previous close and latest close
    previous_close = data["Close"].iloc[-2]
    last_price = data["Close"].iloc[-1]

    change_percent = ((last_price - previous_close) / previous_close) * 100

    result = {
        "symbol": symbol.upper(),
        "price": float(last_price),  # don’t round here if frontend will format
        "previous_close": float(previous_close),
        "change_percent": change_percent
    }

    cache[symbol] = result
    return result

@app.get("/api/history/{symbol}")
def get_history(symbol: str, period: str = "1mo", interval: str = "1d"):
    ticker = yf.Ticker(symbol.upper())
    data = ticker.history(period=period, interval=interval)
    return {
        "symbol": symbol.upper(),
        "history": [{"date": str(i), "close": round(v, 2)} for i, v in data["Close"].items()]
    }

@app.get("/api/ticker")
def get_ticker_data():
    symbols = ["^GSPC", "^DJI", "^IXIC", "VTI", "NVDA", "AMD", "AAPL", "GOOGL"]
    data = []
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist['Close'][-2]
            latest_close = hist['Close'][-1]
            change_percent = ((latest_close - prev_close) / prev_close) * 100
            data.append({
                "symbol": symbol,
                "change_percent": round(change_percent, 2)
            })
    return data  

@app.get("/api/validate/{ticker}")
def validate_ticker(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
       
        if not info or 'symbol' not in info:
            raise HTTPException(status_code=404, detail="Ticker not found")
           
        return {"valid": True, "symbol": ticker.upper()}
    except:
        raise HTTPException(status_code=404, detail="Ticker not found")

# NeMo Integration Functions
def send_to_nemo(data: Dict[str, Any], prompt_template: str) -> Dict[str, Any]:
    """Send data to NVIDIA Nemotron model using OpenAI-compatible API"""
    if not NEMO_API_KEY:
        raise HTTPException(status_code=500, detail="NeMo API key not configured")
    
    try:
        # Initialize OpenAI client with NVIDIA endpoint
        client = OpenAI(
            base_url=NEMO_API_URL,
            api_key=NEMO_API_KEY
        )
        
        # Format the prompt
        formatted_prompt = prompt_template.format(data=data)
        
        # Create completion using OpenAI-compatible API
        completion = client.chat.completions.create(
            model=NEMO_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert financial analyst. Provide clear, data-driven investment recommendations."},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=TEMPERATURE,
            top_p=0.95,
            max_tokens=MAX_TOKENS,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        # Extract the response
        response_text = completion.choices[0].message.content
        
        return {
            "generated_text": response_text,
            "model": NEMO_MODEL,
            "usage": completion.usage.__dict__ if completion.usage else {}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NeMo API error: {str(e)}")

def prepare_stock_data(symbol: str, period: str = "1mo") -> Dict[str, Any]:
    """Prepare stock data for NeMo analysis"""
    ticker = yf.Ticker(symbol.upper())
    data = ticker.history(period=period, interval="1d")
    
    if data.empty:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    # Calculate additional metrics
    current_price = float(data["Close"].iloc[-1])
    previous_close = float(data["Close"].iloc[-2]) if len(data) > 1 else current_price
    price_change = ((current_price - previous_close) / previous_close) * 100
    
    # Calculate volatility (standard deviation of returns)
    returns = data["Close"].pct_change().dropna()
    volatility = float(returns.std() * 100)  # Convert to percentage
    
    # Calculate moving averages
    ma_20 = float(data["Close"].rolling(window=20).mean().iloc[-1]) if len(data) >= 20 else current_price
    ma_50 = float(data["Close"].rolling(window=50).mean().iloc[-1]) if len(data) >= 50 else current_price
    
    # Volume analysis
    avg_volume = float(data["Volume"].mean())
    current_volume = float(data["Volume"].iloc[-1])
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
    
    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "previous_close": previous_close,
        "price_change_percent": round(price_change, 2),
        "volatility_percent": round(volatility, 2),
        "moving_averages": {
            "ma_20": round(ma_20, 2),
            "ma_50": round(ma_50, 2)
        },
        "volume": {
            "current": int(current_volume),
            "average": int(avg_volume),
            "ratio": round(volume_ratio, 2)
        },
        "price_range": {
            "high_52w": float(data["High"].max()),
            "low_52w": float(data["Low"].min()),
            "current_vs_high": round(((current_price - data["High"].max()) / data["High"].max()) * 100, 2)
        },
        "data_points": len(data)
    }      
       
@app.get("/api/quick-decision/{symbol}")
def get_quick_decision(symbol: str):
    """Get quick buy/hold/sell decision from NeMo"""
    try:
        stock_data = prepare_stock_data(symbol, "5d")
        
        quick_prompt = """
        Analyze this stock and provide ONLY a buy/hold/sell recommendation:

        {data}

        Respond in this exact format:
        DECISION: [BUY/HOLD/SELL]
        REASON: [One sentence explaining why]
        """
        
        nemo_response = send_to_nemo(stock_data, quick_prompt)
        analysis_text = nemo_response.get('generated_text', '')
        
        # Extract decision
        lines = analysis_text.split('\n')
        decision = "HOLD"
        reason = "Analysis unavailable"
        
        for line in lines:
            if line.startswith("DECISION:"):
                decision = line.split(":", 1)[1].strip()
            elif line.startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()
        
        return {
            "symbol": symbol.upper(),
            "decision": decision,
            "reason": reason,
            "data": stock_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quick decision failed: {str(e)}")