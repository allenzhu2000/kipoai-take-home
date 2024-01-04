"""
Entry point for the scraper. Scrapes data, then cleans it and saves it to a json file.
"""
import json
from mouser import scrape_mouser_circular_connectors, clean_mouser_data

def main():
   
    scrape_mouser_circular_connectors()
    data = clean_mouser_data()

    with open("data.json", "w") as outfile: 
        json.dump(data, outfile)

if __name__ == '__main__':
   main()