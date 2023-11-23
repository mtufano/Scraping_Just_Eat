from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json

class ScrapRestaurants:
    def __init__(self, url):
        self.url = url

    def fetch_and_parse(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except requests.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    @staticmethod
    def scroll_to_bottom(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Random sleep to mimic human behavior
            time.sleep(random.uniform(2, 5))

            # Calculate the new scroll height and compare it with the last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            # Additional random sleep after scroll
            time.sleep(random.uniform(2, 5))
    
    def extract_restaurant_details(self, soup):
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        if not script_tag or not script_tag.string:
            print("No restaurant details script tag found.")
            return {}

        try:
            data = json.loads(script_tag.string)
            if data.get('@type') == 'Restaurant':
                return {
                    'name': data.get('name', 'No Name'),
                    'servesCuisine': data.get('servesCuisine', []),
                    'streetAddress': data.get('address', {}).get('streetAddress', 'No Street Address'),
                    'addressLocality': data.get('address', {}).get('addressLocality', 'No Address Locality'),
                    'postalCode': data.get('address', {}).get('postalCode', 'No Postal Code'),
                    'addressCountry': data.get('address', {}).get('addressCountry', 'No Country')
                }
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        return {}
    

    def extract_menu_items_with_selenium(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        try:
            driver.get(self.url)
            # Wait for potential dynamic content to load
            time.sleep(random.uniform(5, 10))
            ScrapRestaurants.scroll_to_bottom(driver)
            #ScrapRestaurants.extract_restaurant_details(self)
            # Fetch page source and parse it
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            menu_items = soup.find_all('div', class_='c-menuItems-container')
            if not menu_items:
                print("No menu items found with the given selector.")
                return []

            extracted_data = []
            for item in menu_items:
                name_tag = item.find('h3', class_='c-menuItems-heading')
                name = name_tag.get_text(strip=True) if name_tag else 'No Name'

                description_tag = item.find('p', class_='c-menuItems-description')
                description = description_tag.get_text(strip=True) if description_tag else 'No Description'

                price_tag = item.find('p', class_='c-menuItems-price')
                price = price_tag.get_text(strip=True) if price_tag else 'No Price'

                image_container = item.find('div', class_='c-menuItems-imageContainer')
                image_url = image_container.img['src'] if image_container and image_container.img else 'No Image URL'

                extracted_data.append({
                    'name': name,
                    'description': description,
                    'price': price,
                    'image_url': image_url
                })

            if not extracted_data:
                print("Extraction logic executed, but no data was extracted.")
            return extracted_data
        finally:
            driver.quit()
    
    def scrape_restaurant(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(self.url)
            time.sleep(random.uniform(5, 10))  # Adjust as needed
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            restaurant_details = self.extract_restaurant_details(soup)
            menu_items = self.extract_menu_items_with_selenium(soup)

            return {
                'restaurant_details': restaurant_details,
                'menu_items': menu_items
            }
        finally:
            driver.quit()

# Usage example for a single URL
url = 'https://www.just-eat.co.uk/restaurants-jojo-peri-peri-earls-court/menu'  # Replace with your actual URL
scraper = ScrapRestaurants(url)
#menu_items = scraper.extract_menu_items_with_selenium()
#restaurant_details = scraper.extract_restaurant_details()
#print(menu_items)
#print(restaurant_details)

results = scraper.scrape_restaurant()
print(results)