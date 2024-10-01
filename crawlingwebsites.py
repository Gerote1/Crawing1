import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv
import os
from datetime import datetime
from collections import Counter
import re

# Function to initialize the CSV file with headers
def initialize_csv(filename='b2b_portfolio_data.csv'):
    if not os.path.isfile(filename):  # Check if file exists
        headers = ['Business Name', 'Domain', 'Meta Description', 'Bag of Words', 'Date Crawled']
        
        # Open the file in write mode to create it and add headers
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
        print(f"CSV file '{filename}' initialized with headers.")
    else:
        print(f"CSV file '{filename}' already exists. No need to initialize.")

# Function to crawl each website and extract portfolio-related information
def crawl_b2b_website(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract domain
        domain = urlparse(url).netloc
        
        # Extract business name (e.g., from title or meta tags)
        business_name = soup.title.string if soup.title else 'No business name'
        
        # Extract meta description
        meta = soup.find("meta", attrs={"name": "description"})
        meta_description = meta['content'] if meta else 'No description'
        
        # Extract all text from the website for the bag of words
        page_text = soup.get_text(separator=' ')
        
        # Clean and tokenize text
        words = re.findall(r'\b\w+\b', page_text.lower())
        
        # Create bag of words (word frequency)
        bag_of_words = Counter(words)
        
        # Return the crawled data
        return {
            "Business Name": business_name,
            "Domain": domain,
            "Meta Description": meta_description,
            "Bag of Words": bag_of_words,
            "Date Crawled": datetime.now().strftime('%Y-%m-%d')
        }
    except Exception as e:
        return {"Domain": url, "Error": str(e)}

# Function to save data to CSV
def save_to_csv(data, filename='b2b_portfolio_data.csv'):
    file_exists = os.path.isfile(filename)
    headers = ['Business Name', 'Domain', 'Meta Description', 'Bag of Words', 'Date Crawled']
    
    # Open the file in append mode
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        # Convert the bag of words Counter to a string for CSV storage
        data['Bag of Words'] = str(dict(data['Bag of Words']))
        
        # Write each row of data
        writer.writerow(data)

# Example usage
if __name__ == "__main__":
    # Initialize CSV before saving data
    initialize_csv()

    # Crawl a sample URL and save the data
    url = "www.cisa.gov"
    crawled_data = crawl_b2b_website(url)
    save_to_csv(crawled_data)
