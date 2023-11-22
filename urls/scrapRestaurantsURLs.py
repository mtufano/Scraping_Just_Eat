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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ScrapRestaurants:
    @staticmethod
    def read_urls_from_file(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    
    @staticmethod
    def scroll_to_bottom(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the page to load
            time.sleep(random.uniform(2, 5))

            # Calculate the new scroll height and compare it with the last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    @staticmethod
    def scrape_restaurant_urls(area_urls):
        restaurant_urls = []
        #current_path = './chromedriver.exe'
        
        driver = webdriver.Chrome(ChromeDriverManager().install())

        for url in area_urls:
            driver.get(url)
            # Wait for the page to load
            time.sleep(random.uniform(2, 5))

            # Scroll down to the bottom of the page
            ScrapRestaurants.scroll_to_bottom(driver)
            
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
        ScrapRestaurants.save_urls_to_file(restaurant_urls, 'scraped_urls.txt')
        return restaurant_urls

    @staticmethod
    def save_urls_to_file(urls, file_name):
        with open(file_name, 'w') as file:
            for url in urls:
                file.write(url + '\n')
        print(f'Saved {len(urls)} URLs to {file_name}')

# Usage
area_urls = ScrapRestaurants.read_urls_from_file('urls/modified_london_postcodes.txt')
scraped_urls = ScrapRestaurants.scrape_restaurant_urls(area_urls)
