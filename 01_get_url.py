from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Link to scrape
url = "https://www.tripadvisor.dk/Restaurants-g189530-Aarhus_East_Jutland_Jutland.html"
city = "Aarhus"

# Path to store url
url_filepath = "./url_lists/urls_{}.txt".format(city)

# Setup webdriver
options = Options()
options.headless=True
driver = webdriver.Chrome(executable_path="./chromedriver",
                           chrome_options=options)

# Defining the enumerator
i = 1

# Creating a .txt file to write to
f = open(url_filepath, "w+")

# Variable to define whether the loop should continue
nextPage = True
# While nextPage = True
while nextPage:

    # Finding all restaurant links on the page
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links= soup.find_all("a", class_ = "bHGqj Cj b", href = True)

    # Loop through all the links and append them to the .txt file
    for link in links:
        hep = 'https://www.tripadvisor.dk' + link["href"]
        f.write(hep + "\n")

        # Printing the scraping status
        print(link["href"])
        print("Restaurant no: " + str(i))
        i += 1

    # Check if there is a "next page" button. If yes go to new page. Otherwith exit the loop.
    try:
        unModifiedUrl = str(soup.find('a', class_='nav next rndBtn ui_button primary taLnk', href=True)['href'])
        url = 'https://www.tripadvisor.com' + unModifiedUrl
    except:
        nextPage = False
        f.close()