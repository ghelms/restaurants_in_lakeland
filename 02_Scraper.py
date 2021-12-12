import requests 
from bs4 import BeautifulSoup
import csv 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import glob

files = glob.glob("./url_lists/*.txt", )
# Removing cities that have already been scraped
cities_already_scraped = ["./url_lists/urls_København.txt","./url_lists/urls_Kolding.txt","./url_lists/urls_Silkeborg.txt"]
# Looping through the list and removing elements that match
files = [ele for ele in files if ele not in cities_already_scraped]

# Initializing the webdriver
options = Options()
options.headless=True
driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)

# Loop throug all cities
c = 1
for file in files:
    # Getting the city name
    city = file[17:-4]

    # Printing the city that are scraped next
    print("------------------\nScraping {}\nCity: {} out of {}\n-------------------\n".format(city,c,len(files)))
    # Opening the file with all the urls from that city
    url_file = open(file, "r")
    # Reading the file with the urls
    urls = url_file.readlines()

    pathToReviews = "./reviews/TripReviews_{}.csv".format(city)

    i = 1
    for url in urls:
        print("[ ] scraping {}Number: {} out of {}\nIn {}\n".format(url, i, len(urls),city))
        i += 1

        nextPage = True
        while nextPage:
            #Requests
            driver.get(url)
            time.sleep(1)
            #Click More button
            more = driver.find_elements_by_xpath("//span[contains(text(),'Mere')]")
            # Clicking the "mere" button to see the whole review
            for x in range(0,len(more)):
                try:
                    driver.execute_script("arguments[0].click();", more[x])
                    time.sleep(3)
                except:
                    pass
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            #Store name
            try:
                storeName = soup.find('h1', class_='fHibz').get_text(strip=True)
            except:
                break

            #Reviews
            results = soup.find('div', class_='listContainer hide-more-mobile')
            try:
                reviews = results.find_all('div', class_='prw_rup prw_reviews_review_resp')
            except Exception:
                continue
            #Export to csv
            try:
                with open(pathToReviews, mode='a', encoding="utf-8") as trip_data:
                    data_writer = csv.writer(trip_data, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                    for review in reviews:
                        ratingDate = review.find('span', class_='ratingDate').get('title')
                        text_review = review.find('p', class_='partial_entry')

                        if len(text_review.contents) > 2:
                            reviewText = str(text_review.contents[0][:-3]) + ' ' + str(text_review.contents[1].text)
                        else:
                            reviewText = text_review.text
                        reviewerUsername = review.find('div', class_='info_text pointer_cursor')
                        reviewerUsername = reviewerUsername.select('div > div')[0].get_text(strip=True)
                        rating = review.find('div', class_='ui_column is-9').findChildren('span')
                        rating = str(rating[0]).split('_')[3].split('0')[0]
                        data_writer.writerow([storeName, reviewerUsername, ratingDate, reviewText, rating, city])
            except:
                pass
            #Go to next page if exists
            try:
                unModifiedUrl = str(soup.find('a', class_ = 'nav next ui_button primary',href=True)['href'])
                url = 'https://www.tripadvisor.com' + unModifiedUrl
            except:
                nextPage = False
    # Adding to the enumerater
    c +=1



