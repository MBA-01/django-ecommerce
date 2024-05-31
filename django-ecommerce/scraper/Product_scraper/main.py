# # main.py
# import pandas as pd
# from fetch_product_links import fetch_and_save_product_links
# from extract_product_info import extract_and_save_product_info
# from config.websites import websites

# # Convert websites to DataFrame
# df = pd.DataFrame(websites, columns=["Website"])

# # Fetch and save product links
# fetch_and_save_product_links(df)

# # Extract and save product information
# extract_and_save_product_info()



# main.py
import pandas as pd
from fetch_product_links import fetch_and_save_product_links
from extract_product_info import extract_and_save_product_info

def main(domain_url, sanitized_url):
    # Convert websites to DataFrame
    websites = [domain_url]
    df = pd.DataFrame(websites, columns=["Website"])

    # Fetch and save product links
    fetch_and_save_product_links(df)

    # Extract and save product information
    extract_and_save_product_info(sanitized_url)

if __name__ == "__main__":
    import sys
    domain_url = sys.argv[1]
    sanitized_url = sys.argv[2]
    main(domain_url, sanitized_url)
