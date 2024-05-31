# fetch_product_links.py
import requests
from utils.robots import get_sitemap_url_from_robots
from utils.sitemap import get_product_links_from_sitemap_index
import json
from urllib.parse import urlparse
import logging
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_save_product_links(df):
    for website in df["Website"]:
        domain = urlparse(website).netloc.replace('.', '_')
        logging.info(f"Processing website: {website}")

        sitemap_url = get_sitemap_url_from_robots(website)
        if sitemap_url:
            product_links = get_product_links_from_sitemap_index(sitemap_url)
            if product_links:
                json_path = f"/app/scraper/Product_scraper/data/{domain}_product_data.json"
                
                with open(json_path, 'w') as json_file:
                    json.dump(list(product_links), json_file, indent=4)
                logging.info(f"Saved product links for {website} to {json_path}")
            else:
                logging.warning(f"No product links found for {website}")
        else:
            logging.warning(f"No sitemap found for {website}")
            logging.warning(str(sitemap_url))

if __name__ == "__main__":
    websites = [
        #"https://artisans-dumaroc.com/",
        "https://artisanglobal.org/",
        # Add more websites here
    ]
    df = pd.DataFrame(websites, columns=["Website"])
    fetch_and_save_product_links(df)
