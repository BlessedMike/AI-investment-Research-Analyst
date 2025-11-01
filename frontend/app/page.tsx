'use client';

import { useState, useEffect } from 'react';
import PriceChart from '../components/PriceChart';

interface StockPrice {
  symbol: string;
  price: number;
  previous_close: number;
  change_percent: number;
}

interface MarketData {
  symbol: string;
  change_percent: number;
}

interface QuickDecision {
  decision: string;
  reason: string;
}

export default function Home() {
  const [stockPrice, setStockPrice] = useState<StockPrice | null>(null);
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [symbol, setSymbol] = useState('AAPL');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [quickDecision, setQuickDecision] = useState<QuickDecision | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  const fetchStockPrice = async (ticker: string) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`http://localhost:8000/api/price/${ticker}`);
      if (response.ok) {
        const data = await response.json();
        setStockPrice(data);
      } else {
        setError('Stock not found');
      }
    } catch (err) {
      setError('Error fetching data');
    } finally {
      setLoading(false);
    }
  };

  const fetchMarketData = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/ticker`);
      if (response.ok) {
        const data = await response.json();
        setMarketData(data);
      }
    } catch (err) {
      console.error('Error fetching market data:', err);
    }
  };

  const fetchQuickDecision = async (ticker: string) => {
    setAnalyzing(true);
    try {
      const response = await fetch(`http://localhost:8000/api/quick-decision/${ticker}`);
      if (response.ok) {
        const data = await response.json();
        setQuickDecision(data);
      }
    } catch (err) {
      console.error('Error fetching quick decision:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  useEffect(() => {
    fetchStockPrice(symbol);
    fetchMarketData();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchStockPrice(symbol);
    fetchQuickDecision(symbol);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          📈 AI Investment Research Analyst
        </h1>

        {/* Stock Price Lookup */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">💰 Stock Price Lookup</h2>
          <form onSubmit={handleSubmit} className="flex gap-4 mb-6">
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="Enter ticker symbol (e.g., AAPL)"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Get Price'}
            </button>
          </form>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {stockPrice && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-700">{stockPrice.symbol}</h3>
                <p className="text-3xl font-bold text-gray-900">${stockPrice.price.toFixed(2)}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Change</p>
                <p className={`text-2xl font-bold ${stockPrice.change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {stockPrice.change_percent >= 0 ? '+' : ''}{stockPrice.change_percent.toFixed(2)}%
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Previous Close</p>
                <p className="text-xl font-semibold text-gray-900">${stockPrice.previous_close.toFixed(2)}</p>
              </div>
            </div>
          )}
        </div>

        {/* AI Analysis Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">🤖 AI Analysis</h2>
        
          {/* Quick Analysis Button */}
          <div className="mb-4">
            <button
              onClick={() => fetchQuickDecision(symbol)}
              disabled={analyzing}
              className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
            >
              {analyzing ? 'Analyzing...' : 'Get Quick AI Analysis'}
            </button>
          </div>

          {/* Quick Decision Result (rendered when present) */}
          {quickDecision && (
            <div className="bg-gray-50 p-4 rounded-lg mb-4">
            <h4 className="font-semibold text-gray-700 mb-1">Quick Decision</h4>
              <p className="text-lg font-bold text-gray-900">{quickDecision.decision}</p>
              <p className="text-sm text-gray-600 mt-2">{quickDecision.reason}</p>
              </div>
          )}

        </div>

        {/* Price Chart */}
        {symbol && (
          <div className="mb-8">
            <PriceChart symbol={symbol} period="30d" />
          </div>
        )}

        {/* Market Overview*/}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">📊 Market Overview (Daily Percent Change)</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {marketData.map((item, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded-lg text-center">
                <h3 className="font-semibold text-gray-700">{item.symbol}</h3>
                <p className={`text-lg font-bold ${item.change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {item.change_percent >= 0 ? '+' : ''}{item.change_percent.toFixed(2)}%
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}