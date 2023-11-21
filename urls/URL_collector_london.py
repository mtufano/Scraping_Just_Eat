import requests
from bs4 import BeautifulSoup
import os

london_list = './modified_london_postcodes.txt'

class URLCollector:

    def __init__(self, city_list):
        self.__list = city_list
        self.__dir = './data'
        self.__failed_links = []

    def create_directory(self):
        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)
        self.collect_urls()
        self.log_failed_links()

    def collect_urls(self):
        all_urls = []
        for link in self.__list:
            try:
                reqs = requests.get(link)
                soup = BeautifulSoup(reqs.text, 'html.parser')

                for a_tag in soup.find_all('a'):
                    href = a_tag.get('href')
                    if href and href.startswith('/restaurant*'):
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
url_collector = URLCollector(london_list)
url_collector.create_directory()