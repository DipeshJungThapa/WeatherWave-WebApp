import requests
import json

BASE_URL = "http://localhost:8000/api/"

def test_predict_city(city_name):
    url = BASE_URL + "predict_city/"
    headers = {"Content-Type": "application/json"}
    data = {"city": city_name}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        print(f"--- Testing predict_city for {city_name} ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing predict_city for {city_name}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error Response: {e.response.json()}")

def test_predict_geo(lat, lon):
    url = BASE_URL + "predict_geo/"
    headers = {"Content-Type": "application/json"}
    data = {"lat": lat, "lon": lon}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print(f"\n--- Testing predict_geo for ({lat}, {lon}) ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing predict_geo for ({lat}, {lon}): {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error Response: {e.response.json()}")

if __name__ == "__main__":
    # Test valid city
    test_predict_city("Kathmandu")

    # Test invalid city
    test_predict_city("NonExistentCity")

    # Test valid coordinates
    test_predict_geo(27.7172, 85.3240)

    # Test coordinates that might not map perfectly (e.g., in a lake, or very remote)
    # You might get a "Could not find matching district" depending on your data
    # test_predict_geo(27.0, 84.0)

    # Test missing parameters
    test_predict_city(None) # This will cause an error in the script itself before sending
    test_predict_geo(None, None) # This too