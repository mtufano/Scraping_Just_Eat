from bs4 import BeautifulSoup

# Function to extract menu items from the HTML content
def extract_menu_items_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Find all menu items based on provided HTML structure
    menu_items = soup.find_all('div', class_='c-menuItems-container')

    extracted_data = []
    for item in menu_items:
        # Extracting name, description, price, and image URL with checks for None
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

    return extracted_data

# Path to the saved HTML file
html_file_path = 'JoJo Peri Peri restaurant menu in London - Order from Just Eat.html'

# Extract the menu items
menu_items = extract_menu_items_from_html(html_file_path)
print(menu_items[:5])  # Displaying the first 5 items for brevity


