from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import sqlite3
import logging
import threading
from selenium.webdriver.chrome.options import Options
class ScrapRestaurants:
    def __init__(self, url):
        self.url = url

    # def fetch_and_parse(self):
    #     try:
    #         headers = {
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    #                         '(KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    #         }
    #         response = requests.get(url, headers=headers)
    #         soup = BeautifulSoup(response.content, 'html.parser')
    #         return soup
    #     except requests.HTTPError as e:
    #         print(f"HTTP Error: {e}")
    #         return None
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return None
    
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
    
    def extract_menu_items(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        try:
            driver.get(self.url)
            time.sleep(random.uniform(5, 10))
            self.scroll_to_bottom(driver)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            restaurant_info = {
                'name_vendor': soup.find('h1', {'data-js-test': 'restaurant-heading'}).get_text(strip=True),
                'cuisine_tag': ' '.join([cuisine.get_text(strip=True) for cuisine in soup.find('p', {'data-js-test': 'header-cuisines'}).find_all('span', class_='u-separator')]),
                'address': soup.find('p', {'class': 'l-centered c-restaurantHeader-address'}).get_text(strip=True)
            }

            menu_items = soup.find_all('div', class_='c-menuItems-container')
            extracted_data = []
            for item in menu_items:
                name_tag = item.find('h3', class_='c-menuItems-heading')
                name = name_tag.get_text(strip=True) if name_tag else 'No Name'

                description_tag = item.find('p', class_='c-menuItems-description')
                description = description_tag.get_text(strip=True) if description_tag else 'No Description'

                price_tag = item.find('p', class_='c-menuItems-price')
                price = price_tag.get_text(strip=True) if price_tag else 'No Price'

                image_container = item.find('div', class_='c-dishShowcase-image v-lazy-image')
                image_url = image_container.find('img')['src'] if image_container and image_container.find('img') else 'No Image URL'

                extracted_data.append({
                    'name': name,
                    'description': description,
                    'price': price,
                    'image_url': image_url
                })
                
            return restaurant_info, extracted_data
        finally:
            driver.quit()

    def save_to_db(self, db_name: str, restaurant_data: dict, menu_items: list[dict]) -> None:
        try:
            with sqlite3.connect(db_name) as conn:
                c = conn.cursor()

                c.execute('''CREATE TABLE IF NOT EXISTS restaurant (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                cuisine TEXT,
                                address TEXT
                            )''')

                c.execute('''INSERT INTO restaurant (name, cuisine, address) VALUES (?, ?, ?)''',
                        (restaurant_data['name_vendor'], restaurant_data['cuisine_tag'], restaurant_data['address']))

                restaurant_id = c.lastrowid

                c.execute('''CREATE TABLE IF NOT EXISTS menu (
                                id INTEGER PRIMARY KEY,
                                restaurant_id INTEGER,
                                name TEXT,
                                description TEXT,
                                price TEXT,
                                image_url TEXT,
                                FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
                            )''')

                for item in menu_items:
                    c.execute('''INSERT INTO menu (restaurant_id, name, description, price, image_url) VALUES (?, ?, ?, ?, ?)''',
                              (restaurant_id, item['name'], item['description'], item['price'], item['image_url']))

        except sqlite3.Error as e:
            logging.error(f"SQLite error: {e}")
        except Exception as e:
            logging.error(f"General error in save_to_db: {e}")

def process_url(url, db_name):
    scraper = ScrapRestaurants(url)
    restaurant_info, menu_items = scraper.extract_menu_items()
    scraper.save_to_db(db_name, restaurant_info, menu_items)

def main():
    db_name = 'data/restaurants.db'
    with open('../urls/data/unique_restaurants_urls.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    threads = []
    for i in range(0, len(urls), 3):
        for url in urls[i:i+3]:
            thread = threading.Thread(target=process_url, args=(url, db_name))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            print(f"Processed {thread.name}")

if __name__ == "__main__":
    main()
# Usage example for a single URL
# url = 'https://www.just-eat.co.uk/restaurants-pizza-time-thornton-heath/menu'  # Replace with your actual URL
# scraper = ScrapRestaurants(url)
# restaurant_info, menu_items = scraper.extract_menu_items()
# scraper.save_to_db('restaurant.db', restaurant_info, menu_items)

#     def extract_menu_items(self):
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
#         try:
#             driver.get(self.url)
#             # Wait for potential dynamic content to load
#             time.sleep(random.uniform(5, 10))
#             self.scroll_to_bottom(driver)
            
#             # Fetch page source and parse it
#             restaurant_info = []
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             name_vendor = soup.find('h1', {'data-js-test': 'restaurant-heading'}).text
#             cuisine_tag = soup.find('p', {'data-js-test': 'header-cuisines'}).text
#             address = soup.find('p', {'class': 'l-centered c-restaurantHeader-address'}).text
#             menu_items = soup.find_all('div', class_='c-menuItems-container')
#             restaurant_info.append({
#                 'name_vendor': name_vendor,
#                 'cuisine_tag': cuisine_tag,
#                 'address': address
#             })
#             print(restaurant_info)
#             #menu_items = soup.find_all('div', class_='c-menuItems-container')
#             if not menu_items:
#                 print("No menu items found with the given selector.")
#                 return []

#             self.extracted_data = []
#             for item in menu_items:
#                 name_tag = item.find('h3', class_='c-menuItems-heading')
#                 name = name_tag.get_text(strip=True) if name_tag else 'No Name'

#                 description_tag = item.find('p', class_='c-menuItems-description')
#                 description = description_tag.get_text(strip=True) if description_tag else 'No Description'

#                 price_tag = item.find('p', class_='c-menuItems-price')
#                 price = price_tag.get_text(strip=True) if price_tag else 'No Price'

#                 image_container = item.find('div', class_='c-menuItems-imageContainer')#<div class="c-menuItems-imageContainer"><img src="https://just-eat-prod-eu-res.cloudinary.com/image/upload/c_fill,q_auto,f_auto,h_99,w_132,dpr_1.0/v1/uk/dishes/191504/cheese-and-tomato" class="c-menuItems-image v-lazy-image v-lazy-image-loaded" alt="" srcset="https://just-eat-prod-eu-res.cloudinary.com/image/upload/c_fill,q_auto,f_auto,h_99,w_132,dpr_1.0/v1/uk/dishes/191504/cheese-and-tomato 1x, https://just-eat-prod-eu-res.cloudinary.com/image/upload/c_fill,q_auto,f_auto,h_99,w_132,dpr_2.0/v1/uk/dishes/191504/cheese-and-tomato 2x, https://just-eat-prod-eu-res.cloudinary.com/image/upload/c_fill,q_auto,f_auto,h_99,w_132,dpr_3.0/v1/uk/dishes/191504/cheese-and-tomato 3x"></div>
#                 image_url = image_container.find('img')['src'] if image_container and image_container.find('img') else 'No Image URL'

#                 self.extracted_data.append({
#                     'name': name,
#                     'description': description,
#                     'price': price,
#                     'image_url': image_url
#                 })

#             if not self.extracted_data:
#                 print("Extraction logic executed, but no data was extracted.")
#             return self.extracted_data
#         finally:
#             driver.quit()
    
    
#     def save_to_db(self, db_name: str, restaurant_data: dict, menu_items: list[dict]) -> None:
#         try:
#             with sqlite3.connect(db_name) as conn:
#                 c = conn.cursor()

#                 # Create restaurant table with a combined 'Address' field
#                 c.execute('''CREATE TABLE IF NOT EXISTS restaurant (
#                                 id INTEGER PRIMARY KEY,
#                                 name TEXT,
#                                 cuisine TEXT,
#                                 address TEXT
#                             )''')

#                 # Insert restaurant data
#                 c.execute('''INSERT INTO restaurant 
#                             (name, cuisine, address) 
#                             VALUES (?, ?, ?)''',
#                         (restaurant_data['name_vendor'], restaurant_data['cuisine_tag'], restaurant_data['address']))

#                 # Create menu table if it doesn't exist
#                 c.execute('''CREATE TABLE IF NOT EXISTS menu (
#                                 id INTEGER PRIMARY KEY,
#                                 restaurant_id INTEGER,
#                                 name TEXT,
#                                 description TEXT,
#                                 price REAL,
#                                 image_url TEXT,
#                                 FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
#                             )''')

#                 # Get the last inserted restaurant id
#                 restaurant_id = c.lastrowid

#                 # Insert menu items
#                 for item in menu_items:
#                     c.execute('''INSERT INTO menu 
#                                  (restaurant_id, name, description, price, image_url) 
#                                  VALUES (?, ?, ?, ?, ?)''',
#                               (restaurant_id, self.extracted_data['name'], self.extracted_data['description'], self.extracted_data['price'], self.extracted_data['image_url']))

#         except sqlite3.Error as e:
#             logging.error(f"SQLite error: {e}")
#             # Optionally, handle or re-raise

#         except Exception as e:
#             logging.error(f"General error in save_to_db: {e}")
#             # Optionally, handle or re-raise



# # Usage example for a single URL
# url = 'https://www.just-eat.co.uk/restaurants-pizza-time-thornton-heath/menu'  # Replace with your actual URL
# scraper = ScrapRestaurants(url)
# #menu_items = scraper.extract_menu_items_with_selenium()
# #restaurant_details = scraper.extract_restaurant_details()
# #print(menu_items)
# #print(restaurant_details)

# results = scraper.extract_menu_items()
# print(results)