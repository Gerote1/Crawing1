import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv
import os
from datetime import datetime

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
        
        # Extract portfolio details (you will need to adjust this part based on the website's structure)
        portfolio_details = soup.find('section', class_='portfolio')  # Example (based on site's HTML)
        portfolio_details = portfolio_details.text.strip() if portfolio_details else 'No portfolio details'

        # Extract services (again, adjust based on the site structure)
        services = soup.find('div', class_='services')  # Example (based on site's HTML)
        services = services.text.strip() if services else 'No services listed'
        
        # Extract contact information
        contact_info = soup.find('a', href=lambda href: href and "mailto:" in href)
        contact_info = contact_info['href'].replace('mailto:', '') if contact_info else 'No contact info'
        
        # Extract other info if needed (e.g., social links, location, client info, etc.)
        # Adjust these based on the HTML structure of the websites you're crawling.

        return {
            "business_name": business_name,
            "domain": domain,
            "services_products": services,
            "portfolio_details": portfolio_details,
            "contact_info": contact_info,
            "meta_description": meta_description,
            "website_title": business_name,
            "date_crawled": datetime.now().strftime('%Y-%m-%d')
        }
    except Exception as e:
        return {"domain": url, "error": str(e)}

# Function to save data to CSV
def save_to_csv(data, filename='b2b_portfolio_data.csv'):
    file_exists = os.path.isfile(filename)
    headers = ['Business Name', 'Domain', 'Services Products', 'Portfolio Details', 'Contact Info', 'Meta Description', 'Website Title', 'Date Crawled']
    
    # Open the file in append mode
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        # Write each row of data
        writer.writerow(data)

# Example usage (You'd call this in a loop for multiple B2B sites)
url = "https://example.com"
crawled_data = crawl_b2b_website(url)
save_to_csv(crawled_data)
