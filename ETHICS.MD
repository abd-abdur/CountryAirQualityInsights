# Ethical Considerations

## Purpose of Data Collection

The primary purpose of this project is to analyze the relationship between population metrics and air quality across different countries. By combining population data with air quality measurements we aim to provide valuable insights that can inform policymakers, environmental analysts, and urban planners in making data-driven decisions to improve public health and environmental standards.

## Why Are You Collecting This Data?

Collecting and merging population data with air quality information allows for a comprehensive analysis of how population density and demographics influence environmental conditions. Understanding these correlations can help identify regions at higher risk of air pollution-related health issues, optimize resource allocation for environmental interventions, and guide sustainable urban development strategies.

## Data Sources and robots.txt

### Data Sources

1. **Wikipedia:**
   - **URL:** [List of countries and dependencies by population](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population)
   - **Purpose:** Scrapes the latest population data for countries and dependencies.
   
2. **OpenAQ API:**
   - **URL:** [OpenAQ API Documentation](https://docs.openaq.org/)
   - **Purpose:** Fetches current air quality measurements for countries worldwide.

### robots.txt Compliance

Before initiating any scraping activities, the `robots.txt` files of the target websites were thoroughly reviewed to ensure compliance with their scraping policies.

- **Wikipedia robots.txt:**
  - **URL:** [https://en.wikipedia.org/robots.txt](https://en.wikipedia.org/robots.txt)
  - **Compliance:** The sections containing population data are allowed to be scraped. The scraping script respects the `Crawl-delay` directives and avoids restricted areas.

- **OpenAQ API:**
  - **Access:** As an API, OpenAQ provides structured access to its data without the need for scraping. The usage adheres to the API's terms of service and rate limiting policies.

**Note:** Only websites that permit scraping in their `robots.txt` and terms of service were selected to ensure ethical data collection practices.

## Collection Practices

### Limiting Scraping to Avoid Disruption

To minimize the impact on the target websites' servers, the scraping script incorporates the following measures:

- **Rate Limiting:** Implements delays (`delay=2` seconds) between successive scraping requests to avoid overwhelming the server.
- **Pagination Limits:** Restricts the number of pages scraped (e.g., `max_pages=5`) to prevent excessive data requests in a short period.
- **Respecting Crawl-Delays:** Adheres to any `Crawl-delay` directives specified in the `robots.txt` file.

### Do Not Bypass Password Protection

The scraping activities are confined to publicly accessible sections of the websites. The script does not attempt to access or bypass any password-protected areas or restricted content, ensuring compliance with ethical standards and legal requirements.

## Data Handling and Privacy

### Do Not Collect Personally Identifiable Information (PII)

The project strictly avoids collecting any PII or sensitive user data. The data sources used provide aggregated population and air quality metrics without delving into individual-level information. This approach ensures the privacy and confidentiality of individuals.

### Store Data Securely

To safeguard any sensitive configurations and maintain data integrity, the project employs the following practices:

- **Environment Variables:** API keys and other sensitive information are stored in a `.env` file, which is excluded from version control using the `.gitignore` file.
  
  ```gitignore
  # Environment Variables
  .env
