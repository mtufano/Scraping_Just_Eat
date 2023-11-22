# Read the file
with open('scraped_urls_first_test.txt', 'r') as file:
    urls = file.readlines()

# Remove duplicates
unique_urls = set(urls)

# Write the unique URLs back to the file
with open('unique_restaurants_urls.txt', 'w') as file:
    for url in unique_urls:
        file.write(url)
