# utils/sitemap.py
import requests
from xml.etree import ElementTree as ET

def get_product_links_from_sitemap_index(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        product_sitemap_url = None
        for elem in root.iter():
            if elem.tag.endswith("loc") and "product" in elem.text:
                product_sitemap_url = elem.text
                break
        
        if product_sitemap_url:
            return get_product_links_from_sitemap(product_sitemap_url)
        else:
            return set()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch sitemap index {sitemap_url}: {e}")
        return set()

# def get_product_links_from_sitemap(sitemap_url):
#     try:
#         response = requests.get(sitemap_url)
#         response.raise_for_status()
#         root = ET.fromstring(response.content)
#         product_links = set()
#         for elem in root.iter():
#             if elem.tag.endswith("loc") and "product" in elem.text:
#                 product_links.add(elem.text)
#         return product_links
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch sitemap {sitemap_url}: {e}")
#         return set()


# def get_product_links_from_sitemap(sitemap_url):
#     try:
#         response = requests.get(sitemap_url)
#         response.raise_for_status()
#         root = ET.fromstring(response.content)
#         product_links = set()
#         image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
#         for elem in root.iter():
#             if elem.tag.endswith("loc"):
#                 url = elem.text
#                 if not any(url.lower().endswith(ext) for ext in image_extensions):
#                     product_links.add(url)
#         return product_links
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to fetch sitemap {sitemap_url}: {e}")
#         return set()


def get_product_links_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        product_links = set()
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
        for elem in root.iter():
            if elem.tag.endswith("loc"):
                url = elem.text
                if not any(ext in url.lower() for ext in image_extensions):
                    product_links.add(url)
        return product_links
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch sitemap {sitemap_url}: {e}")
        return set()