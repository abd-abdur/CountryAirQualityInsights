import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

# Send a request to the webpage
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Try to find the table that contains the population data
tables = soup.find_all("table", {"class": "wikitable"})

if not tables:
    print("Error: Could not find any table with class 'wikitable'. The structure of the page might have changed.")
else:
    print(f"Found {len(tables)} tables with class 'wikitable'.")

    for i, table in enumerate(tables):

        caption = table.find("caption")
        if caption and "population" in caption.text.lower():
            print(f"Using table {i+1} with caption: {caption.text.strip()}")
            break
    else:
        print("Error: Could not find a table with a relevant caption about population.")
        table = None

if table:
    # Initialize empty lists to store data
    countries = []
    populations = []
    percent_world = []
    dates = []

    # Iterate through the rows of the table and extract the relevant columns
    for row in table.find_all("tr")[1:]:  # Skip the header
        columns = row.find_all("td")
        
        if len(columns) >= 4:  # Ensure the row has enough columns
            country = columns[0].text.strip()
            population = columns[1].text.strip().replace(",", "")  # Remove commas in population
            percent = columns[2].text.strip()
            date = columns[3].text.strip()
            
            if country: 
                countries.append(country)
                populations.append(population)
                percent_world.append(percent)
                dates.append(date)

    # a DataFrame to store the data
    df = pd.DataFrame({
        "Country": countries,
        "Population": populations,
        "% of World Population": percent_world,
        "Date": dates
    })

    df['Country'] = df['Country'].str.replace(r'\[\w+\]', '', regex=True) 
    df['Country'] = df['Country'].str.replace(r'\d+/?\d*', '', regex=True)  
    df['Country'] = df['Country'].str.replace(r'–', '', regex=True) 
    df['Country'] = df['Country'].str.strip() 

    # Display the cleaned DataFrame
    print(df)

    df.to_csv("cleaned_countries_by_population.csv", index=False)
