"""
Operational Metrics Measurement Script
======================================
Measures actual performance metrics for WeatherWave backend
- API response times
- ML inference latency
- Memory usage
- Request patterns
"""

import time
import requests
import json
import sys
import psutil
import os
from datetime import datetime

# Backend URL (adjust if different)
BACKEND_URL = "http://127.0.0.1:8000"

# Test location
TEST_CITY = "Kathmandu"
TEST_LAT = "27.7172"
TEST_LON = "85.3240"

def measure_endpoint(endpoint, method="GET", data=None, params=None):
    """Measure response time for an endpoint"""
    url = f"{BACKEND_URL}{endpoint}"
    
    times = []
    for i in range(10):  # 10 requests to get average
        start = time.time()
        try:
            if method == "GET":
                response = requests.get(url, params=params, timeout=30)
            else:
                response = requests.post(url, json=data, timeout=30)
            
            elapsed = (time.time() - start) * 1000  # Convert to ms
            times.append(elapsed)
            
            if response.status_code not in [200, 201]:
                print(f"  ⚠️ Request {i+1}: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ Request {i+1} failed: {e}")
            times.append(-1)
    
    # Filter out failed requests
    valid_times = [t for t in times if t > 0]
    
    if valid_times:
        import statistics
        return {
            'mean': statistics.mean(valid_times),
            'std': statistics.stdev(valid_times) if len(valid_times) > 1 else 0,
            'min': min(valid_times),
            'max': max(valid_times),
            'samples': len(valid_times),
            'success_rate': (len(valid_times) / len(times)) * 100
        }
    else:
        return None

def get_system_specs():
    """Get current system specifications"""
    return {
        'cpu_count': psutil.cpu_count(logical=False),
        'cpu_count_logical': psutil.cpu_count(logical=True),
        'cpu_freq_mhz': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A',
        'ram_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        'ram_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'ram_percent': psutil.virtual_memory().percent
    }

def count_api_calls_per_request():
    """Count external API calls made per user request"""
    # Based on code analysis
    return {
        'full_dashboard_load': {
            'description': 'User loads dashboard for one location',
            'api_calls': {
                'OpenWeather_current': 1,
                'OpenWeather_forecast': 1,
                'WeatherAPI_aqi': 1,
                'Supabase_ml_prediction': 1  # CSV download
            },
            'total': 4
        },
        'location_change': {
            'description': 'User changes location',
            'api_calls': {
                'OpenWeather_current': 1,
                'OpenWeather_forecast': 1,
                'WeatherAPI_aqi': 1,
                'Supabase_ml_prediction': 1
            },
            'total': 4
        },
        'news_load': {
            'description': 'Weather news section',
            'api_calls': {
                'NewsAPI_or_RSS': 1
            },
            'total': 1
        }
    }

def estimate_api_costs():
    """Estimate monthly API costs based on pricing tiers"""
    # Pricing as of Dec 2024
    pricing = {
        'OpenWeather': {
            'free_tier': '1,000 calls/day (60,000/month)',
            'paid_starter': '$40/month for 100,000 calls',
            'cost_per_call': 40 / 100000  # $0.0004 per call
        },
        'WeatherAPI': {
            'free_tier': '1,000,000 calls/month',
            'paid_starter': '$4/month for 1.5M calls',
            'cost_per_call': 4 / 1500000  # $0.00000267 per call
        },
        'NewsAPI': {
            'free_tier': '100 requests/day (3,000/month)',
            'paid': '$449/month for unlimited',
            'cost_per_call': 0  # Using RSS feeds (free)
        },
        'Supabase': {
            'free_tier': '500MB storage, 2GB transfer',
            'paid': '$25/month for 8GB storage, 50GB transfer',
            'storage_cost': 25 / 8  # $3.125 per GB
        }
    }
    
    # Calculate for different user volumes
    scenarios = {}
    for users in [10, 50, 100, 500, 1000]:
        # Assumptions:
        # - Each user checks weather 3 times/day
        # - Each check = 4 API calls (weather + forecast + AQI + ML)
        # - News loaded once per day
        # - Cache reduces calls by 80% (5-min cache)
        
        daily_requests = users * 3
        monthly_requests = daily_requests * 30
        
        # With 80% cache hit rate
        actual_api_calls = monthly_requests * 0.2
        
        # OpenWeather (current + forecast = 2 calls per request)
        openweather_calls = actual_api_calls * 2
        openweather_cost = max(0, (openweather_calls - 60000) * pricing['OpenWeather']['cost_per_call'])
        
        # WeatherAPI (AQI = 1 call per request)
        weatherapi_calls = actual_api_calls * 1
        weatherapi_cost = 0 if weatherapi_calls < 1000000 else 4
        
        # Supabase (ML predictions CSV download)
        # CSV size: ~50KB, downloaded per request (with cache)
        monthly_transfer_gb = (actual_api_calls * 50) / (1024**2)  # KB to GB
        supabase_cost = 0 if monthly_transfer_gb < 2 else 25
        
        # News (RSS feeds - free)
        news_cost = 0
        
        total_cost = openweather_cost + weatherapi_cost + supabase_cost + news_cost
        
        scenarios[f'{users}_users'] = {
            'monthly_requests': monthly_requests,
            'actual_api_calls': actual_api_calls,
            'cache_hit_rate': '80%',
            'openweather_calls': openweather_calls,
            'weatherapi_calls': weatherapi_calls,
            'supabase_transfer_gb': round(monthly_transfer_gb, 2),
            'costs': {
                'openweather': round(openweather_cost, 2),
                'weatherapi': round(weatherapi_cost, 2),
                'supabase': round(supabase_cost, 2),
                'news': news_cost,
                'total_monthly': round(total_cost, 2)
            }
        }
    
    return {
        'pricing_tiers': pricing,
        'scenarios': scenarios
    }

def main():
    print("=" * 80)
    print("WeatherWave Operational Metrics Measurement")
    print("=" * 80)
    print()
    
    # Check if backend is running
    print("1. Checking backend availability...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/current-weather/?city=Kathmandu", timeout=5)
        print(f"   ✅ Backend is running (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Backend not accessible: {e}")
        print("\n   Please start backend first:")
        print("   cd backend && python manage.py runserver")
        return
    
    print()
    
    # Get system specs
    print("2. System Specifications:")
    specs = get_system_specs()
    print(f"   CPU: {specs['cpu_count']} cores ({specs['cpu_count_logical']} logical)")
    print(f"   CPU Frequency: {specs['cpu_freq_mhz']} MHz")
    print(f"   RAM: {specs['ram_total_gb']} GB total, {specs['ram_available_gb']} GB available")
    print(f"   Current Usage: CPU {specs['cpu_percent']}%, RAM {specs['ram_percent']}%")
    print()
    
    # Measure endpoint latencies
    print("3. API Endpoint Latencies (10 requests each):")
    print()
    
    endpoints = [
        {
            'name': 'Current Weather',
            'endpoint': '/api/current-weather/',
            'method': 'GET',
            'params': {'city': TEST_CITY}
        },
        {
            'name': '5-Day Forecast',
            'endpoint': '/api/forecast/',
            'method': 'GET',
            'params': {'city': TEST_CITY}
        },
        {
            'name': 'Air Quality Index',
            'endpoint': '/api/aqi/',
            'method': 'GET',
            'params': {'city': TEST_CITY}
        },
        {
            'name': 'ML Prediction',
            'endpoint': '/api/predict-city/',
            'method': 'POST',
            'data': {'city': TEST_CITY}
        }
    ]
    
    results = {}
    for ep in endpoints:
        print(f"   Testing {ep['name']}...")
        result = measure_endpoint(
            ep['endpoint'],
            method=ep['method'],
            data=ep.get('data'),
            params=ep.get('params')
        )
        
        if result:
            results[ep['name']] = result
            print(f"   ✅ Mean: {result['mean']:.2f}ms ± {result['std']:.2f}ms")
            print(f"      Range: {result['min']:.2f}ms - {result['max']:.2f}ms")
            print(f"      Success: {result['success_rate']:.1f}% ({result['samples']}/10)")
        else:
            print(f"   ❌ All requests failed")
        print()
    
    # Calculate total dashboard load time
    if results:
        total_mean = sum(r['mean'] for r in results.values())
        print(f"   📊 Total Dashboard Load Time: {total_mean:.2f}ms ({total_mean/1000:.2f}s)")
        print()
    
    # API calls per request
    print("4. API Calls Per User Request:")
    api_calls = count_api_calls_per_request()
    for scenario, info in api_calls.items():
        print(f"   {info['description']}:")
        for api, count in info['api_calls'].items():
            print(f"     - {api}: {count}")
        print(f"     Total: {info['total']} calls")
        print()
    
    # Cost estimation
    print("5. Monthly API Cost Estimation:")
    costs = estimate_api_costs()
    print()
    print("   Cost Scenarios (with 80% cache hit rate):")
    for scenario, data in costs['scenarios'].items():
        users = scenario.replace('_users', '')
        print(f"\n   📈 {users} Users:")
        print(f"      Monthly Requests: {data['monthly_requests']:,}")
        print(f"      Actual API Calls: {data['actual_api_calls']:,.0f} (after cache)")
        print(f"      Costs:")
        print(f"        - OpenWeather: ${data['costs']['openweather']}")
        print(f"        - WeatherAPI: ${data['costs']['weatherapi']}")
        print(f"        - Supabase: ${data['costs']['supabase']}")
        print(f"        💰 Total: ${data['costs']['total_monthly']}/month")
    
    print()
    
    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'system_specs': specs,
        'endpoint_latencies': results,
        'api_calls_pattern': api_calls,
        'cost_estimation': costs
    }
    
    with open('analysis/operational_metrics.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("✅ Results saved to analysis/operational_metrics.json")
    print()
    print("=" * 80)
    print("Measurement Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
