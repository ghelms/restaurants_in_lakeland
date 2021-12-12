# Seeded LDA analysis of TripAdvisor reviews on Danish Restaurants.  
An implementation on python for scraping unique Restaurants's reviews or scraping a whole geographical area's reviews from TripAdvisor along with a markdown that conducts a seeded LDA analysis of the scraped reviews. 

## How to use:

The pipeline consists of three scripts that should be run in asscending order. 

### 01_get_url.py
- This script takes a city and a URL to a tripadvisor webpage for a specific city as input. The script will loop through all restaurants in a specific city and collect the URLs to the restaurants' TripAdvisor page. The URL links are stored in a .txt file. 

### 02_scraper.py
- This script loops through all .txt files made from the 01_get_url.py script. For each .txt file it loops through all restaurant links inside it and scrapes all reviews for each restaurant which is stored in .csv file. The script can take an input for which cities to not scrape. 

### 03_analysis.Rmd
- In this markdown the analysis can be replicated. The script is divided into four parts. The first part is preprocessing. In the second part of the script the seeded LDA analysis are conducted. In the third part, the estimates from the LDA analysis are visualized. In the fourth part an lmer are conducted on the data. 

If you have any feature requests, don't hesitate to contact us :)

Use at own risk, it might violate TripAdvisor policies.
