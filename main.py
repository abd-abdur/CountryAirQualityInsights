import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -------------------------------
# Step 1: Scrape and Clean Population Data
# -------------------------------

def scrape_population_data():
    # URL of the Wikipedia page
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    
    # Send a request to the webpage
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all tables with class 'wikitable'
    tables = soup.find_all("table", {"class": "wikitable"})
    
    if not tables:
        raise ValueError("Error: Could not find any table with class 'wikitable'. The structure of the page might have changed.")
    else:
        print(f"Found {len(tables)} tables with class 'wikitable'.")
    
    target_table = None
    for i, table in enumerate(tables):
        caption = table.find("caption")
        if caption and "population" in caption.text.lower():
            print(f"Using table {i+1} with caption: {caption.text.strip()}")
            target_table = table
            break
    else:
        raise ValueError("Error: Could not find a table with a relevant caption about population.")
    
    # Initialize empty lists to store data
    countries = []
    populations = []
    percent_world = []
 
    for row in target_table.find_all("tr")[1:]:  # Skip the header
        columns = row.find_all(["td", "th"])
        
        if len(columns) >= 4: 
            country = columns[1].text.strip()  
            population = columns[2].text.strip().replace(",", "")  
            percent = columns[3].text.strip()

            # Append only if country is not empty
            if country:
                countries.append(country)
                populations.append(population)
                percent_world.append(percent)
                # Skipped appending 'date'
    
    #  a DataFrame to store the data
    df_population = pd.DataFrame({
        "Country": countries,
        "Population": populations,
        "% of World Population": percent_world
    })
    
    # Clean the 'Country' column
    df_population['Country'] = df_population['Country'].str.replace(r'^\W+', '', regex=True)  
    df_population['Country'] = df_population['Country'].str.replace(r'\[\w+\]', '', regex=True)  
    df_population['Country'] = df_population['Country'].str.replace(r'\d+/?\d*', '', regex=True)  
    df_population['Country'] = df_population['Country'].str.replace(r'–', '', regex=True) 
    df_population['Country'] = df_population['Country'].str.strip() 
    print("Scraped and cleaned population data:")
    print(df_population.head())

    return df_population

# -------------------------------
# Step 2: Fetch and Clean Air Quality Data
# -------------------------------

def get_all_countries(api_key):
    """Fetch a list of countries from OpenAQ API."""
    countries = []
    page = 1
    while True:
        url = f"https://api.openaq.org/v2/countries?limit=100&page={page}"
        headers = {
            "X-API-Key": api_key
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            countries.extend(data['results'])
            if len(data['results']) < 100:
                break  
            page += 1
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

def fetch_air_quality_data(api_key):
    """Fetch air quality data for all countries from OpenAQ API."""
    countries = get_all_countries(api_key)
    if not countries:
        print("No countries fetched from OpenAQ API.")
        return pd.DataFrame()

    results = []

    for country in countries:
        country_code = country['code']
        country_name = country['name']
        air_quality = get_air_quality(api_key, country_code)
        
        if air_quality:
            measurement = air_quality[0]
            pollution_value = measurement['value']
            parameter = measurement['parameter']
            results.append({
                "Country": country_name,
                "Pollution_Value": pollution_value,
                "Parameter": parameter
            })
    
    # DataFrame to store the data
    df_air_quality = pd.DataFrame(results)
    
    print("Fetched and cleaned air quality data:")
    print(df_air_quality.head())

    return df_air_quality

# -------------------------------
# Step 3: Merge Datasets
# -------------------------------

def merge_datasets(df_population, df_air_quality):
    """Merge population and air quality data on the 'Country' column."""
    df_population['Country_clean'] = df_population['Country'].str.lower().str.strip()
    df_air_quality['Country_clean'] = df_air_quality['Country'].str.lower().str.strip()

    # Merge on the cleaned country names
    df_combined = pd.merge(df_population, df_air_quality, on='Country_clean', how='inner', suffixes=('_Population', '_AirQuality'))

    # Drop the helper 'Country_clean' column
    df_combined.drop(columns=['Country_clean'], inplace=True)

    # Remove the 'Country_AirQuality' column
    if 'Country_AirQuality' in df_combined.columns:
        df_combined.drop(columns=['Country_AirQuality'], inplace=True)
        print("Dropped 'Country_AirQuality' column.")
    df_combined['Pollution_Value'] = pd.to_numeric(df_combined['Pollution_Value'], errors='coerce')

    # Remove rows with negative pollution values
    initial_count = df_combined.shape[0]
    df_combined = df_combined[df_combined['Pollution_Value'] >= 0]
    final_count = df_combined.shape[0]
    removed_count = initial_count - final_count
    print(f"Removed {removed_count} countries with negative pollution values.")

    print("Merged and cleaned population and air quality data:")
    print(df_combined.head())

    return df_combined

# -------------------------------
# Step 4: Main Function
# -------------------------------

def main():

    api_key = os.getenv('OPENAQ_API_KEY')
    
    # Scrape population data
    df_population = scrape_population_data()
    
    # Fetch air quality data
    df_air_quality = fetch_air_quality_data(api_key)
    
    if df_air_quality.empty:
        print("Air quality data is empty. Exiting the script.")
        return
    
    # Merge datasets
    df_combined = merge_datasets(df_population, df_air_quality)
    
    if df_combined.empty:
        print("Merged dataset is empty. No data to save.")
        return
    
    # Save the combined data to a CSV file
    df_combined.to_csv("combined_population_air_quality.csv", index=False)
    print("Combined data saved to combined_population_air_quality.csv")

if __name__ == "__main__":
    main()
