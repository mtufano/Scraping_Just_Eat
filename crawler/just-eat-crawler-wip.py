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
        # Extract restaurant name
        name_tag = soup.find('div', {'class': 'c-pageBanner c-pageBanner--negativeBottom--aboveMid c-pageBanner--shadowBottom u-zIndex--low'})
        name = name_tag.get_text(strip=True) if name_tag else 'No Name'

        # Extract cuisine types
        cuisine_tag = soup.find('p', {'data-js-test': 'header-cuisines'})
        if cuisine_tag:
            cuisines = [cuisine.strip() for cuisine in cuisine_tag.get_text().split(',') if cuisine.strip()]
        else:
            cuisines = []

        # Extract address
        address_tag = soup.find('p', {'class': 'l-centered c-restaurantHeader-address'})
        address = address_tag.get_text(strip=True) if address_tag else 'No Address'

        restaurant_details = {
            'name': name,
            'cuisines': cuisines,
            'address': address
        }

        return restaurant_details

    def extract_menu_items(self, soup):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        try:
            driver.get(self.url)
            # Wait for potential dynamic content to load
            time.sleep(random.uniform(5, 10))
            ScrapRestaurants.scroll_to_bottom(driver)
            #ScrapRestaurants.extract_restaurant_details(self)
            # Fetch page source and parse it
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            name_vendor = soup.find('h1', {'data-js-test': 'restaurant-heading'})
            address = soup.find('p', {'class': 'l-centered c-restaurantHeader-address'})
            menu_items = soup.find_all('div', class_='c-menuItems-container')
            print(name_vendor)
            print(address)
            #menu_items = soup.find_all('div', class_='c-menuItems-container')
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

    # def extract_restaurant_info(self, html_content):
    #     # Parse the HTML content
    #     soup = BeautifulSoup(html_content, 'html.parser')

    #     # Extract restaurant name
    #     name_tag = soup.find('h1', {'data-js-test': 'restaurant-heading'})
    #     restaurant_name = name_tag.get_text(strip=True) if name_tag else 'No Name'

    #     # Extract cuisine types
    #     cuisine_tag = soup.find('p', {'data-js-test': 'header-cuisines'})
    #     cuisines = [span.get_text(strip=True) for span in cuisine_tag.find_all('span')] if cuisine_tag else []

    #     # Extract address
    #     address_tag = soup.find('span', {'data-js-test': 'header-restaurantAddress'})
    #     address = address_tag.get_text(strip=True) if address_tag else 'No Address'

    #     return {
    #         'name': restaurant_name,
    #         'cuisines': cuisines,
    #         'address': address
    #     }
    

    # def extract_restaurant_details_from_script(self, soup):
    #     # Find the script tag with type application/ld+json and id structured-data-restaurant
    #     script_tag = soup.find('script', {'type': 'application/ld+json', 'data-vmid': 'structured-data-restaurant'})
    #     if not script_tag or not script_tag.string:
    #         print("No structured-data-restaurant script tag found.")
    #         return None

    #     try:
    #         data = json.loads(script_tag.string)
    #         if data.get('@type') == 'Restaurant':
    #             details = {
    #                 'name': data.get('name', 'No Name'),
    #                 'servesCuisine': data.get('servesCuisine', []),
    #                 'streetAddress': data.get('address', {}).get('streetAddress', 'No Street Address'),
    #                 'addressLocality': data.get('address', {}).get('addressLocality', 'No Address Locality'),
    #                 'postalCode': data.get('address', {}).get('postalCode', 'No Postal Code'),
    #                 'addressCountry': data.get('address', {}).get('addressCountry', 'No Country'),
    #                 # Add any other details you need
    #             }
    #             return details
    #     except json.JSONDecodeError as e:
    #         print(f"JSON decoding error: {e}")

    #     print("No valid restaurant details found in the structured-data-restaurant script tag.")
    #     return None

    def scrape_restaurant(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(self.url)
            time.sleep(random.uniform(5, 10))  # Adjust as needed
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            restaurant_info = self.extract_restaurant_details(soup)
            print(restaurant_info)
            menu_items = self.extract_menu_items(soup)  # Assuming this method exists and works correctly
            return {
                'restaurant_info': restaurant_info,
                'menu_items': menu_items
            }
        finally:
            driver.quit()
# Usage example for a single URL
url = 'https://www.just-eat.co.uk/restaurants-pizza-time-thornton-heath/menu'  # Replace with your actual URL
scraper = ScrapRestaurants(url)
#menu_items = scraper.extract_menu_items_with_selenium()
#restaurant_details = scraper.extract_restaurant_details()
#print(menu_items)
#print(restaurant_details)

results = scraper.scrape_restaurant()
print(results)