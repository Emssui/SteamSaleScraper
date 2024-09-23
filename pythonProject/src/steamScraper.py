import csv
import bs4 as bs
import urllib.request

# Opening a connection
my_url = urllib.request.urlopen('https://store.steampowered.com/search/?specials=1&os=win').read()

# Turning the HTML into a BeautifulSoup object
soup = bs.BeautifulSoup(my_url, 'lxml')

# Extracting game titles
data_body = soup.find_all('span', {'class': 'title'})

# Extracting discount blocks
discount_blocks = soup.find_all('div', {'class': 'search_discount_block'})

# Open a CSV file for writing
with open('steamSaleScraper.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['Game Name', 'Discount'])

    # Loop through both game titles and discount blocks
    for i in range(min(len(data_body), len(discount_blocks))):
        game_name = data_body[i].text.strip()

        # Extracting discount percentage from the data-discount attribute
        discount_percentage = discount_blocks[i].get('data-discount')

        if discount_percentage:
            discount_text = f"{discount_percentage}%"
        else:
            discount_text = "No discount"

        # Write the game name and discount to the CSV file
        writer.writerow([game_name, discount_text])
        print(f"Game: {game_name}, Discount: {discount_text}")
