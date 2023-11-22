from bs4 import BeautifulSoup
import json

def extract_and_save_json(html_file_path, json_file_path):
    # Read HTML content from a file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the <script> tag with type 'application/ld+json'
    script = soup.find('script', {'type': 'application/ld+json'})

    if script:
        # Extract JSON data
        json_data = json.loads(script.string)

        # Save JSON data to a file
        with open(json_file_path, 'w') as file:
            json.dump(json_data, file, indent=4)
        print(f"JSON data saved to {json_file_path}")
    else:
        print("No JSON data found in HTML.")

# Example usage
# Example usage
extract_and_save_json('C:/Users/tufan001/OneDrive - Wageningen University & Research/MIT/Food City/Scraping_Just_Eat/crawler/html file/SUPER COD SW20 restaurant menu in London - Order from Just Eat.html', 'data.json')