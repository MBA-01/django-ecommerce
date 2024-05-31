# extract_product_info.py
import os
import json
import requests
from bs4 import BeautifulSoup
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define keywords to look for in tag attributes
keywords = ["title", "price", "description", "images"]

def clean_text(text):
    """Clean and remove redundant spaces from the text."""
    return ' '.join(text.split())

def encode_text(text):
    """Encode text to UTF-8."""
    return text.encode('utf8').decode('utf8')

def extract_product_page_info(url):
    try:
        logging.info(f"Fetching URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        product_info = {'link': url}

        for keyword in keywords[:-1]:  # Exclude "images" from initial keyword processing
            logging.info(f"Extracting {keyword} information")
            elements = soup.find_all(attrs={'class': lambda c: c and keyword in c.lower()})
            text_content = " ".join([element.get_text(strip=True) for element in elements])

            if keyword == "price":
                # Extract numerical value and currency using regex
                matches = re.findall(r'(\$\d+(?:\.\d{2})?)|([£€]\d+(?:\.\d{2})?)|(\d+(?:\.\d{2})?\s?(USD|EUR|GBP|CAD|AUD|JPY|CHF|CNY|INR|£|€))', text_content)
                unique_prices = set()
                for match in matches:
                    price = ''.join(match).strip()
                    if price:
                        unique_prices.add(price)
                unique_text_content = " ".join(unique_prices)
                unique_text_content = encode_text(unique_text_content)
            else:
                # Remove redundancy by preserving order and uniqueness for other keywords
                unique_words = []
                seen_words = set()
                for word in text_content.split():
                    if word not in seen_words:
                        unique_words.append(word)
                        seen_words.add(word)
                unique_text_content = " ".join(unique_words)
                unique_text_content = encode_text(unique_text_content)

            logging.info(f"Extracted {keyword} content: {unique_text_content}")
            product_info[keyword] = unique_text_content

        # Extract all image URLs, excluding those containing "logo"
        logging.info(f"Extracting image URLs")
        images = soup.find_all('img')
        image_urls = [img['src'] for img in images if 'src' in img.attrs and 'logo' not in img['src'].lower()]
        product_info['images'] = image_urls
        logging.info(f"Extracted image URLs: {image_urls}")

        # Check if any keyword is missing and try to extract from other tags
        for keyword in keywords[:-1]:  # Exclude "images" from fallback keyword processing
            if not product_info[keyword] or (keyword == "title" and len(product_info[keyword]) > 70):
                logging.info(f"Retrying extraction for missing {keyword} information")
                if keyword == "title":
                    # Try to find the title from the <title> tag
                    tag = soup.find('title')
                    if tag:
                        title_text = clean_text(tag.get_text(strip=True))
                        if len(title_text) <= 70:  # Consider title valid if it's not too long
                            product_info[keyword] = title_text
                        else:
                            product_info[keyword] = "Not found"
                    # Additional extraction logic for title
                    if not product_info[keyword] or product_info[keyword] == "Not found":
                        # Try to find the title from the <h1>, <h2>, or <h3> tags
                        elements = soup.find_all(['h1', 'h2', 'h3'])
                        for element in elements:
                            title_text = clean_text(element.get_text(strip=True))
                            if len(title_text) <= 70:  # Consider title valid if it's not too long
                                product_info[keyword] = title_text
                                break
                elif keyword == "price":
                    # Look for 'div' or 'span' tags with class or id containing 'price'
                    tag = soup.find(lambda tag: tag.name in ['div', 'span'] and 'price' in ''.join(tag.get('class', []) + [tag.get('id', '')]))
                    if tag:
                        text_content = tag.get_text(strip=True)
                        matches = re.findall(r'(\$\d+(?:\.\d{2})?)|([£€]\d+(?:\.\d{2})?)|(\d+(?:\.\d{2})?\s?(USD|EUR|GBP|CAD|AUD|JPY|CHF|CNY|INR|£|€))', text_content)
                        unique_prices = set()
                        for match in matches:
                            price = ''.join(match).strip()
                            if price:
                                unique_prices.add(price)
                        product_info[keyword] = " ".join(unique_prices)
                else:
                    tag = soup.find(lambda tag: tag.name in ['p', 'span', 'div'] and keyword in tag.get_text(strip=True).lower())
                    if tag:
                        product_info[keyword] = clean_text(tag.get_text(strip=True))

                if keyword in product_info and product_info[keyword] != "Not found":
                    logging.info(f"Extracted {keyword} content from fallback method: {product_info[keyword]}")
                else:
                    product_info[keyword] = "Not found"
                    logging.warning(f"{keyword} content not found in fallback method")

        return product_info
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return {}
from urllib.parse import urlparse
def extract_and_save_product_info(sanitized_url):
    # Directory containing JSON files with product links
    data_dir = '/app/scraper/Product_scraper/data'
    
    # Iterate over JSON files
    for filename in os.listdir(data_dir):
        if filename.endswith('_product_data.json'):
            domain = filename.replace('_product_data.json', '').replace('_', '.')
            logging.info(f"filename: {filename}")
            if urlparse(sanitized_url).netloc.replace('.', '_') in filename:
                logging.info(f"sanitized_url_parsed: {urlparse(sanitized_url).netloc.replace('.', '_')}")

                with open(os.path.join(data_dir, filename), 'r') as file:
                    product_links = json.load(file)
                
                product_info_list = []
                
                for url in product_links:
                    product_info = extract_product_page_info(url)
                    logging.info(f"extracting {url} product page info")
                    if product_info:
                        product_info_list.append(product_info)
                        logging.info(f"TRUE")
                    else:
                        logging.info(f"False")


                logging.info(f"Saving product info for {domain}")
                
                # Save the extracted product info to JSON
                output_json_path = os.path.join(data_dir, f"{domain}_product_info_details.json")
                with open(output_json_path, 'w') as output_file:
                    json.dump(product_info_list, output_file, indent=4)
                
                logging.info(f"Saved product info for {domain} to {output_json_path}")
            else :
                logging.info("failed")
                logging.info(f"sanitzed_url: {sanitized_url}")
                logging.info(f"domain: {domain}")
        logging.info("failed")

if __name__ == "__main__":
    import sys
    sanitized_url = sys.argv[1]
    extract_and_save_product_info(sanitized_url)
