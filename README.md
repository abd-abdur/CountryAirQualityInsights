# Population-Air Quality Data Pipeline

## Overview

The **Population-Air Quality Data Pipeline** is a project that combines demographic data with environmental metrics to provide insightful analyses on how population dynamics influence air quality across different countries. This pipeline leverages data scraped from [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population) and fetched from the [OpenAQ API](https://openaq.org/), culminating in a unique, cleaned dataset that is not publicly available for free. This merged dataset offers valuable insights for researchers, policymakers, and environmental analysts aiming to understand and address the interplay between population growth and air pollution.

## Data Sources

### 1. Wikipedia

- **Purpose:** Scrapes the latest population data for countries and dependencies.
- **Data Retrieved:**
  - **Country:** Name of the country or dependency.
  - **Population:** Total population count.
  - **% of World Population:** The country's population as a percentage of the global population.
- **Reason for Choice:** Wikipedia maintains an up-to-date and comprehensive list of countries and their populations. Its structured tables make it an ideal source for demographic data scraping, ensuring accuracy and reliability.

### 2. OpenAQ API

- **Purpose:** Fetches current air quality measurements for countries worldwide.
- **Data Retrieved:**
  - **Pollution Value:** Measurement value of pollutants (e.g., PM2.5, NO2).
  - **Parameter:** Type of pollutant measured.
- **Reason for Choice:** OpenAQ offers a free and extensive repository of air quality data, providing real-time and historical pollution measurements. Its API facilitates seamless data retrieval making it essential for environmental analysis.

## Value Proposition

The **Population-Air Quality Data Pipeline** delivers a unique dataset that merges population statistics with air quality indicators. This integration allows for comprehensive analyses to understand how population density and demographics correlate with pollution levels. The dataset's uniqueness stems from its combination of two distinct data sources which are not typically merged and made publicly available for free. 

**Benefits to Users:**

- **Researchers:** Enables studies on the impact of population growth on environmental health.
- **Policy Makers:** Assists in developing targeted policies to mitigate pollution in densely populated areas.
- **Environmental Analysts:** Facilitates the identification of high-risk regions for air quality interventions.
- **Urban Planners:** Informs sustainable city planning to balance population growth with environmental preservation.

**Uniqueness of the Dataset:**

While both population and air quality data are available individually their combined analysis provides deeper insights that are not readily accessible. This merged dataset is not publicly available for free, offering novel value by bridging the gap between demographic and environmental data.

## How to Run the Project

### Prerequisites

- **Python 3.x:** Ensure Python is installed on your machine. Download it from [here](https://www.python.org/downloads/).
- **OpenAQ API Key:** Register for a free API key at [OpenAQ](https://openaq.org/#/sign-up) to enhance your data retrieval capabilities.

### Steps

1. **Clone the Repository:**

   Replace `abd-abdur` with your actual GitHub username.

   ```bash
   git clone https://github.com/abd-abdur/CountryAirQualityInsights.git
   cd population-air-quality-pipeline
