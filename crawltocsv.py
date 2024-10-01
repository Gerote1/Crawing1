import serpapi
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv

# Function to get the Google search results from SerpApi
def get_google_results(query):
    client = serpapi.Client(api_key="4a7c367bf5517d0d113bef4359092091d6766b7f42a4fed6326457835ff2b816")  # Use your SerpApi key here
    params = {
        'engine': 'google',
        'q': query,
        'num': 50  # Number of results to get
    }
    results = client.search(params)
    links = [result['link'] for result in results['organic_results']]  # Collect links from SerpApi response
    return links

# Function to crawl each website and extract domain, title, and description
def crawl_website(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the domain
        domain = urlparse(url).netloc
        
        # Extract the title
        title = soup.title.string if soup.title else 'No title'

        # Extract the meta description
        meta = soup.find("meta", attrs={"name": "description"})
        description = meta['content'] if meta else 'No description'
        
        return {"domain": domain, "title": title, "description": description}
    
    except Exception as e:
        return {"domain": url, "title": "Error", "description": str(e)}

# Function to save the data to a CSV file
def save_to_csv(data, filename='results.csv'):
    headers = ['Domain', 'Title', 'Description']
    
    # Open the file in write mode
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write the header if the file is new
        writer.writeheader()
        
        # Write each row of data
        for row in data:
            writer.writerow({'Domain': row['domain'], 'Title': row['title'], 'Description': row['description']})
            print(f"Domain: {row['domain']}")
            print(f"Title: {row['title']}")
            print(f"Description: {row['description']}")
            print("-" * 50)
    
    print(f"Data saved to {filename}")

# Main function that runs the search and crawling process
def main(query):
    # Get first 50 Google search results
    urls = get_google_results(query)
    
    # Crawl each URL and extract domain, title, description
    results = []
    for url in urls:
        data = crawl_website(url)
        results.append(data)
    
    # Save the crawled data to a CSV file
    save_to_csv(results)

# Example usage
query = "Data storage solutions "
main(query)

#it consulting companies in delhi ncr
#it consulting firms in delhi ncr
#it solutions delhi ncr
#it consultancy delhi ncr
#it companies delhi ncr
#it services delhi ncr
#msp provider delhi ncr
#msp delhi ncr
#it services gurugram
#it services noida
#it services delhi


#api parameter changed
#msp provider
#it solutions
    # network security solutions
    # Cybersecurity services
    # Cisco networking solutions
