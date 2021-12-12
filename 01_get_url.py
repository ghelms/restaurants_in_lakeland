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


i = 1
f = open(url_filepath, "w+")

nextPage = True
while nextPage:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links= soup.find_all("a", class_ = "bHGqj Cj b", href = True)

    for link in links:
        hep = 'https://www.tripadvisor.dk' + link["href"]
        f.write(hep + "\n")


        print(link["href"])
        print("Restaurant no: " + str(i))
        i += 1

    try:
        unModifiedUrl = str(soup.find('a', class_='nav next rndBtn ui_button primary taLnk', href=True)['href'])
        url = 'https://www.tripadvisor.com' + unModifiedUrl
    except:
        nextPage = False
        f.close()