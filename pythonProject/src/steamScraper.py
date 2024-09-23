import csv
import requests
from bs4 import BeautifulSoup

# Opening a connection
url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&specials=1&infinite=1'


def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']


def parse(data):
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')

    # Open a CSV file for writing
    with open('steamScraper.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Discount', 'Old Price', 'New Price'])  # CSV headers

        for game in games:
            title = game.find('span', {'class': 'title'}).text.strip()

            # Extracting discount information
            discount_info = game.find('div', {'class': 'search_price_discount_combined'}).text.strip()
            if discount_info:
                # Split based on spaces and euro symbol
                parts = discount_info.split('€')
                discount_part = parts[0].strip()
                prices = [price.strip() for price in parts[1:]]

                # Extract discount percentage
                discount_percentage = discount_part.split(' ')[0]  # First part is the discount percentage

                # Assign old and new prices
                old_price = prices[0] if len(prices) > 0 else "N/A"  # Original price
                new_price = prices[1] if len(prices) > 1 else "N/A"  # Discounted price
            else:
                discount_percentage = "N/A"
                old_price = "N/A"
                new_price = "N/A"

            # Write the row to CSV
            writer.writerow([title, discount_percentage, old_price, new_price])
            print(f"Game: {title}, Discount: {discount_percentage}, Old Price: {old_price}, New Price: {new_price}")


data = get_data(url)
parse(data)
