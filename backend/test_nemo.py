#!/usr/bin/env python3
"""
Test script for NeMo integration
Run this to test the NeMo API integration without starting the full server
"""

import requests
import json
from config import validate_config

def test_nemo_connection():
    """Test basic NeMo API connection"""
    print("🧪 Testing NeMo API Integration...")
    
    # Validate configuration
    if not validate_config():
        print("❌ Configuration validation failed")
        return False
    
    # Test API endpoint
    test_url = "http://localhost:8000/api/analyze/AAPL"
    
    try:
        print("📡 Sending test request to NeMo analysis endpoint...")
        response = requests.post(test_url, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ NeMo integration working!")
            print(f"📊 Analysis for {data['symbol']} completed")
            print(f"⏰ Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running:")
        print("   python -m uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_quick_analysis():
    """Test quick analysis endpoint"""
    print("\n🚀 Testing Quick Analysis...")
    
    try:
        response = requests.get("http://localhost:8000/api/quick-analysis/AAPL", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Quick analysis working!")
            print(f"📊 Quick analysis for {data['symbol']} completed")
            return True
        else:
            print(f"❌ Quick analysis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Quick analysis test failed: {str(e)}")
        return False

def test_without_nemo():
    """Test endpoints that don't require NeMo"""
    print("\n📈 Testing non-NeMo endpoints...")
    
    endpoints = [
        ("GET", "/api/price/AAPL"),
        ("GET", "/api/validate/AAPL"),
        ("GET", "/api/ticker")
    ]
    
    for method, endpoint in endpoints:
        try:
            url = f"http://localhost:8000{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {method} {endpoint} - Working")
            else:
                print(f"❌ {method} {endpoint} - Failed ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 AI Investment Research Analyst - NeMo Integration Test")
    print("=" * 60)
    
    # Test basic endpoints first
    test_without_nemo()
    
    # Test NeMo integration
    if test_nemo_connection():
        test_quick_analysis()
    
    print("\n" + "=" * 60)
    print("🏁 Test completed!")
    print("=" * 60)
