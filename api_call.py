import requests
import pandas as pd
import time

def get_all_countries(api_key):
    """Fetch a list of countries from OpenAQ API."""
    countries = []
    for page in range(1, 3): 
        url = f"https://api.openaq.org/v2/countries?limit=100&page={page}"
        headers = {
            "X-API-Key": api_key
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            countries.extend(response.json()['results'])
        else:
            print(f"Error fetching page {page}: {response.status_code} - {response.text}")
            break

    return countries

def get_air_quality(api_key, country_code, retry_delay=10, max_retries=5):
    """Fetch air quality data for a specific country, with exponential backoff for rate limiting."""
    url = f"https://api.openaq.org/v2/measurements?country={country_code}&limit=1"
    headers = {
        "X-API-Key": api_key
    }
    
    retries = 0
    while retries < max_retries:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()['results']
        elif response.status_code == 429:  # Rate limiting
            retries += 1
            wait_time = retry_delay * (2 ** retries)  # Exponential backoff
            print(f"Rate limit reached. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    print(f"Max retries reached for country: {country_code}")
    return None

def main(api_key):
    """Main function to fetch air quality data for all countries and save it to a CSV file."""
    countries = get_all_countries(api_key)
    if countries:
        results = []

        for country in countries:
            country_code = country['code']
            air_quality = get_air_quality(api_key, country_code)
            
            if air_quality:
                pollution_value = air_quality[0]['value']
                results.append({
                    "country": country['name'],
                    "pollution_value": pollution_value,
                    "parameter": air_quality[0]['parameter'],
                    "date": air_quality[0]['date']['utc']
                })

        df = pd.DataFrame(results)
        df.to_csv('country_pollution_data.csv', index=False)
        print("Data saved to country_pollution_data.csv")

# Example usage
api_key = 'e74fed8fe4215b0a72d8d7314977565153f6e5bcd08bb98156221fce9f48d0e9'  
main(api_key)
