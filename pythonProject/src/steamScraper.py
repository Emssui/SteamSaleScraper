import csv
import tkinter
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk

# Opening a connection
url = 'https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&specials=1&infinite=1'

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

def parse(data):
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')

    # List to store parsed game data
    parsed_data = []

    # Open a CSV file for writing
    with open('steamScraper.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Discount', 'Old Price', 'New Price'])  # CSV headers

        for game in games:
            title = game.find('span', {'class': 'title'}).text.strip()

            # Extracting discount information
            discount_info = game.find('div', {'class': 'search_price_discount_combined'}).text.strip()
            if discount_info:
                try:
                    # Step 1: Extract the discount percentage
                    discount_percentage = discount_info.split('%')[0] + '%'  # e.g., -40%

                    # Step 2: Extract old and new prices from the remaining part after the discount
                    price_info = discount_info.split('%')[1].strip()  # e.g., "59,99€35,99€"
                    prices = price_info.split('€')  # Split by the euro sign

                    old_price = prices[0].strip() + '€'  # First part is the old price
                    new_price = prices[1].strip() + '€'  # Second part is the new price

                except IndexError:
                    old_price = "N/A"
                    new_price = "N/A"
                    discount_percentage = "N/A"

            else:
                discount_percentage = "N/A"
                old_price = "N/A"
                new_price = "N/A"

            # Append parsed data to the list
            parsed_data.append([title, discount_percentage, old_price, new_price])

            # Write the data to the CSV file
            writer.writerow([title, discount_percentage, old_price, new_price])

    return parsed_data

# Function to display the data in the Tkinter window
def display_data_in_table(data):
    root = Tk()
    root.title("Steam Sales Scraper")

    frame = tkinter.Frame(root)
    frame.pack(fill=tkinter.BOTH, expand=True)

    # Create Treeview for displaying the table
    tree = ttk.Treeview(frame, columns=('Name', 'Discount', 'Old Price', 'New Price'), show='headings', height=24)

    # Define headings
    tree.heading('Name', text='Game Name')
    tree.heading('Discount', text='Discount')
    tree.heading('Old Price', text='Old Price')
    tree.heading('New Price', text='New Price')

    # Define column widths
    tree.column('Name', width=300)
    tree.column('Discount', width=100, anchor=CENTER)
    tree.column('Old Price', width=100, anchor=CENTER)
    tree.column('New Price', width=100, anchor=CENTER)

    # Create a vertical scrollbar and attach it to the treeview
    scrollbar = ttk.Scrollbar(frame, orient=tkinter.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Pack the treeview and scrollbar side by side
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Insert data into the treeview
    for game in data:
        tree.insert('', 'end', values=game)

    # Run the Tkinter event loop
    root.mainloop()

# Get data from the URL
data = get_data(url)
parsed_data = parse(data)

# Display the data in the Tkinter table
display_data_in_table(parsed_data)
