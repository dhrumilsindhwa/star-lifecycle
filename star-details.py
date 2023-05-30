import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import re

def clean_data(value):
    # Remove everything within square brackets
    value = re.sub(r'\[.*\]', '', value)
    # Remove non-ASCII characters
    value = value.encode("ascii", "ignore").decode()
    # Remove comma
    value = value.replace(',', '')
    # Remove everything after the first non-digit character
    value = re.sub(r'[^0-9.].*', '', value)
    return value

def get_star_data(star_names):
    star_data = []

    for star_name in star_names:
        url = f"https://en.wikipedia.org/wiki/{star_name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Select all the table rows in the star's info box
        rows = soup.select(".infobox tr")

        data = {"name": star_name}

        for row in rows:
            # Get the first and second td elements in this row
            cells = row.select("td")
            if len(cells) > 1:
                # Get the text of the first cell (the data name)
                data_name = cells[0].get_text(strip=True).lower()
                # Get the text of the second cell (the data value)
                data_value = clean_data(cells[1].get_text(strip=True))
                # If the data name is one of the ones we're interested in, save it
                if data_name in ["mass", "temperature", "distance", "radius", "luminosity"]:
                    data[data_name] = data_value

        star_data.append(data)

        # Sleep for a bit in between requests to avoid overwhelming the server
        sleep(1)

    return star_data

# Read the star names from a file
with open("star_names.txt", "r") as file:
    star_names = [line.strip() for line in file]

star_data = get_star_data(star_names)

# Write the star data to a CSV file
with open("star_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Star", "Mass(Solar Mass)", "Temperature(K)", "Distance(ly)", "Radius(Solar Radius)", "Luminosity(Solar Luminosity)"])
    writer.writeheader()
    for data in star_data:
        writer.writerow(data)
