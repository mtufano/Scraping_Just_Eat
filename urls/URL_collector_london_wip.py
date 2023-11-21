import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent

class URLCollector:

    def __init__(self, city_list_file):
        self.__list_file = city_list_file
        self.__dir = './data'
        self.__failed_links = []

                # Initialize a session with a random User-Agent
        self.session = requests.Session()
        self.session.headers['User-Agent'] = UserAgent().random

    def create_directory(self):
        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)
        self.collect_urls()
        self.log_failed_links()

    def collect_urls(self):
        all_urls = []
        with open(self.__list_file, 'r') as file:
            # Read lines from the file
            links = file.readlines()
            for link in links:
                try:
                    # Removing leading/trailing whitespace and newline characters
                    link = link.strip()
                    reqs = requests.get(link)
                    reqs.raise_for_status()  # Raise an error for 4xx/5xx responses

                    soup = BeautifulSoup(reqs.text, 'html.parser')

                    for a_tag in soup.find_all('a'):
                        href = a_tag.get('href')
                        if href and href.startswith('/restaurants'):
                            modified_href = 'https://just-eat.co.uk/' + href
                            all_urls.append(modified_href)
                except Exception as e:
                    print(f"Failed to process {link}: {e}")
                    self.__failed_links.append(link)

            # Write all URLs to a single file
            with open(os.path.join(self.__dir, "london_rest_links_justeat.txt"), "w") as f:
                for url in all_urls:
                    f.write(url + "\n")

    def log_failed_links(self):
        if self.__failed_links:
            with open(os.path.join(self.__dir, "failed_links.txt"), "w") as f:
                for link in self.__failed_links:
                    f.write(link + "\n")

# Usage
city_list_file = 'data/test.txt'
url_collector = URLCollector(city_list_file)
url_collector.create_directory()
