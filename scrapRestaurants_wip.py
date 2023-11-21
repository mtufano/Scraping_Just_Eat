from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import random


class ScrapRestaurants:
    @staticmethod
    def read_urls_from_file(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file]

    @staticmethod
    def scrape_restaurant_urls(area_urls):
        restaurant_urls = []
        #current_path = './chromedriver.exe'
        
        driver = webdriver.Chrome(ChromeDriverManager().install())

        for url in area_urls:
            driver.get(url)
            # Wait for the page to load
            time.sleep(random.uniform(2, 5))


            # Find all <a> tags that contain restaurant URLs
            restaurant_links = driver.find_elements(By.CSS_SELECTOR, "a[data-test-id='f-restaurant-card--restaurant-card-component']")

            for link in restaurant_links:
                restaurant_url = link.get_attribute('href')
                if restaurant_url:
                    # Append the full URL if it's relative
                    if restaurant_url.startswith("/"):
                        restaurant_url = "https://www.just-eat.co.uk" + restaurant_url
                    restaurant_urls.append(restaurant_url)

            print(f'{len(restaurant_urls)} URLs scraped from {url}')

            # Wait before loading the next page
            time.sleep(random.uniform(2, 5))

        driver.quit()
        return restaurant_urls

# Usage
area_urls = ScrapRestaurants.read_urls_from_file('test.txt')
scraped_urls = ScrapRestaurants.scrape_restaurant_urls(area_urls)
print(scraped_urls)
