import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class Crawler:    
    @staticmethod
    def read_urls_from_file(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file]

    @staticmethod
    def scroll_to_bottom(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 5))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    @staticmethod
    def scrape_restaurant_menus(area_urls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Runs Chrome in headless mode.
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for url in area_urls:
            driver.get(url)
            time.sleep(random.uniform(2, 5))
            Crawler.scroll_to_bottom(driver)
            content = driver.page_source
            menu_items = Crawler.extract_menu_items(content)
            print(menu_items)  # Process or store the extracted data as needed

    @staticmethod
    def extract_menu_items(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        menu_items = soup.find_all('div', class_='c-menuItems-container')
        extracted_data = []

        for item in menu_items:
            name = item.find('h3', class_='c-menuItems-heading').get_text(strip=True) if item.find('h3') else 'No Name'
            description = item.find('p', class_='c-menuItems-description').get_text(strip=True) if item.find('p') else 'No Description'
            price = item.find('p', class_='c-menuItems-price').get_text(strip=True) if item.find('p') else 'No Price'
            image_container = item.find('div', class_='c-menuItems-imageContainer')
            image_url = image_container.img['src'] if image_container and image_container.img else 'No Image URL'
            
            extracted_data.append({
                'name': name,
                'description': description,
                'price': price,
                'image_url': image_url
            })

        return extracted_data
    
    @staticmethod
    def scrape_restaurant_details(area_urls):
        # Set up the Excel workbook and worksheet
        workbook = xlsxwriter.Workbook('Restaurants.xlsx')
        worksheet = workbook.add_worksheet()
        row_count = 0

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        for url in area_urls:
            try:
                driver.get(url)
                time.sleep(random.uniform(2, 5))  # Allow time for the page to load

                # Extract restaurant details
                details = driver.find_element(By.XPATH, "//div[@class='restaurantOverview o-card u-negativeSpace--top']/div[2]")
                rstName = details.find_element(By.XPATH, "//h1[@class='name']").text
                Foods = details.find_elements(By.XPATH, "//p[@class='cuisines']/span")

                if len(Foods) > 1:
                    rstFood = ', '.join([food.text for food in Foods[:2]])
                else:
                    rstFood = Foods[0].text if Foods else 'No Food Info'

                address_parts = details.find_elements(By.XPATH, "//p[@class='address']/span")
                rstAddress = ', '.join([part.text for part in address_parts])

                # Write to worksheet
                worksheet.write(row_count, 0, rstName)
                worksheet.write(row_count, 1, rstFood)
                worksheet.write(row_count, 2, rstAddress)

                print(f"{row_count} scraped {url} - {rstName}")
                row_count += 1

            except Exception as ex:
                print(f"Error scraping {url}: {ex}")

        # Close resources
        workbook.close()
        driver.quit()

# Example usage
area_urls = ['https://www.just-eat.co.uk/restaurants-jojo-peri-peri-earls-court/menu']
Crawler.scrape_restaurant_menus(area_urls)
