# utils/robots.py
import requests
import logging
def get_sitemap_url_from_robots(url):
    try:
        response = requests.get(f"{url}/robots.txt")
        response.raise_for_status()
        for line in response.text.splitlines():
            if line.lower().startswith("sitemap:"):
                return line.split(":", 1)[1].strip()
    except requests.exceptions.RequestException as e:
        logging.warning(f"Failed to fetch {url}/robots.txt: {e}")
    return None
