from bs4 import BeautifulSoup
import json

html_file_path = 'JoJo Peri Peri restaurant menu in London - Order from Just Eat.html'
# Output file path
output_file_path = 'extracted_data.txt'

# Read the HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find the script tag or the HTML element containing the JSON
script_tag = soup.find('script', text=lambda t: t and 'mxInfo' in t and 'menuList' in t)

def save_data_to_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"IOError occurred: {e}")

# Extract and parse the JSON data
if script_tag:
    json_string = script_tag.string
    data = json.loads(json_string)
    print(data)
    save_data_to_json('data.json', data)
    # Open the output file
   # with open(output_file_path, 'w', encoding='utf-8') as output_file:
