# 🤖 NVIDIA NeMo 9B Integration

This document explains how to use the NVIDIA NeMo 9B model integration in your AI Investment Research Analyst.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the backend directory:
```bash
# .env
NEMO_API_KEY=your_nvidia_nemo_api_key_here
NEMO_API_URL=https://api.nvidia.com/v1/nemo
```

### 3. Start the Server
```bash
python -m uvicorn main:app --reload
```

### 4. Test the Integration
```bash
python test_nemo.py
```

## 📊 New API Endpoints

### 1. Comprehensive Analysis
**POST** `/api/analyze/{symbol}`

Get detailed AI-powered stock analysis using NeMo 9B.

**Parameters:**
- `symbol` (path): Stock ticker symbol (e.g., AAPL, GOOGL)
- `period` (query, optional): Data period (default: "1mo")

**Example:**
```bash
curl -X POST "http://localhost:8000/api/analyze/AAPL?period=3mo"
```

**Response:**
```json
{
  "symbol": "AAPL",
  "analysis": {
    "generated_text": "Comprehensive analysis from NeMo 9B..."
  },
  "raw_data": {
    "symbol": "AAPL",
    "current_price": 150.25,
    "price_change_percent": 2.5,
    "volatility_percent": 1.8,
    "moving_averages": {
      "ma_20": 148.50,
      "ma_50": 145.75
    },
    "volume": {
      "current": 50000000,
      "average": 45000000,
      "ratio": 1.11
    },
    "price_range": {
      "high_52w": 180.00,
      "low_52w": 120.00,
      "current_vs_high": -16.5
    }
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Quick Analysis
**GET** `/api/quick-analysis/{symbol}`

Get a brief AI analysis for quick insights.

**Example:**
```bash
curl "http://localhost:8000/api/quick-analysis/AAPL"
```

**Response:**
```json
{
  "symbol": "AAPL",
  "quick_analysis": {
    "generated_text": "Brief analysis from NeMo 9B..."
  },
  "data": {
    "symbol": "AAPL",
    "current_price": 150.25,
    "price_change_percent": 2.5,
    "volatility_percent": 1.8
  }
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEMO_API_KEY` | Your NVIDIA NeMo API key | Required |
| `NEMO_API_URL` | NeMo API endpoint | `https://api.nvidia.com/v1/nemo` |
| `API_TIMEOUT` | Request timeout in seconds | `30` |
| `MAX_TOKENS` | Maximum tokens for NeMo response | `1000` |
| `TEMPERATURE` | NeMo temperature setting | `0.7` |

### Configuration File
Edit `config.py` to customize settings:

```python
# NeMo API Configuration
NEMO_API_URL = "https://api.nvidia.com/v1/nemo"
NEMO_API_KEY = "your_api_key_here"

# API Settings
API_TIMEOUT = 30
MAX_TOKENS = 1000
TEMPERATURE = 0.7
```

## 📈 Data Analysis Features

The NeMo integration provides comprehensive stock analysis including:

### Technical Analysis
- Price trend analysis
- Moving average signals (20-day, 50-day)
- Volatility assessment
- Volume analysis

### Risk Assessment
- Volatility risk level
- Price position relative to 52-week range
- Volume patterns and liquidity

### Investment Recommendations
- Buy/Hold/Sell recommendations
- Price targets
- Time horizon suggestions

### Key Factors to Watch
- Important technical levels
- Volume patterns to monitor
- Market conditions affecting the stock

## 🧪 Testing

### Run Tests
```bash
# Test all endpoints
python test_nemo.py

# Test specific functionality
python -c "from config import validate_config; validate_config()"
```

### Manual Testing
```bash
# Test comprehensive analysis
curl -X POST "http://localhost:8000/api/analyze/AAPL" | jq

# Test quick analysis
curl "http://localhost:8000/api/quick-analysis/GOOGL" | jq
```

## 🚨 Error Handling

The integration includes comprehensive error handling:

- **API Key Missing**: Clear warning message
- **Network Errors**: Timeout and connection error handling
- **Invalid Tickers**: Proper error responses
- **Rate Limiting**: Graceful handling of API limits

## 💡 Usage Tips

1. **API Key**: Get your NeMo API key from [NVIDIA Developer](https://developer.nvidia.com/nemo)

2. **Rate Limiting**: The integration includes caching to minimize API calls

3. **Error Handling**: Check the response status and error messages

4. **Performance**: Use quick analysis for faster responses

5. **Data Quality**: More historical data provides better analysis

## 🔗 Integration with Frontend

The NeMo analysis can be easily integrated into your frontend:

```javascript
// Get comprehensive analysis
async function getNeMoAnalysis(symbol) {
  const response = await fetch(`/api/analyze/${symbol}`, {
    method: 'POST'
  });
  return await response.json();
}

// Get quick analysis
async function getQuickAnalysis(symbol) {
  const response = await fetch(`/api/quick-analysis/${symbol}`);
  return await response.json();
}
```

## 📚 Additional Resources

- [NVIDIA NeMo Documentation](https://docs.nvidia.com/nemo/)
- [NVIDIA Developer Portal](https://developer.nvidia.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🐛 Troubleshooting

### Common Issues

1. **"NeMo API key not configured"**
   - Set `NEMO_API_KEY` in your `.env` file

2. **"NeMo API error: 401"**
   - Check your API key is valid and active

3. **"NeMo API error: 429"**
   - You've hit rate limits, wait before retrying

4. **"Analysis failed: Ticker not found"**
   - Check the ticker symbol is valid

5. **Connection errors**
   - Ensure the FastAPI server is running
   - Check your internet connection
