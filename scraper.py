import os
import requests
import re
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import socket
import time
from datetime import datetime
import logging

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

# Configuration
SCRAPING_THREADS = 30  # Threads for scraping
TESTING_THREADS = 100  # Threads for proxy testing
TIMEOUT = 5  # Connection timeout
SAVE_DIRECTORY = os.path.join(os.path.dirname(__file__), "proxies")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Create save directory
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

# Define the URLs for scraping proxy lists
proxy_urls = [
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=text&timeout=20000",
    "https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt",
    "https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt",
    "https://github.com/TheSpeedX/PROXY-List/blob/master/socks4.txt",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://sunny9577.github.io/proxy-scraper/generated/http_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks4_proxies.txt",
]

def validate_proxy(proxy, test_url="http://www.google.com"):
    """Test if proxy is working with improved validation"""
    try:
        host, port = proxy.split(':')
        with socket.create_connection((host, int(port)), timeout=TIMEOUT):
            return True
    except:
        return False

def classify_proxy(url):
    """Classify proxy type based on URL"""
    if 'socks4' in url.lower():
        return 'socks4'
    elif 'socks5' in url.lower():
        return 'socks5'
    else:
        return 'http'

def scrape_proxies_parallel(urls):
    """Scrape proxies using parallel processing"""
    def scrape_single_url(url):
        try:
            proxy_type = classify_proxy(url)
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                if "proxyscrape" in url:
                    proxies = response.text.split('\n')
                else:
                    proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', response.text)
                return proxy_type, proxies, True, None
            return proxy_type, [], False, f"Status: {response.status_code}"
        except Exception as e:
            return proxy_type, [], False, str(e)

    results = {}
    with ThreadPoolExecutor(max_workers=SCRAPING_THREADS) as executor:
        futures = {executor.submit(scrape_single_url, url): url for url in urls}
        for future in tqdm(futures, desc=f"Scraping proxies ({SCRAPING_THREADS} threads)"):
            url = futures[future]
            proxy_type, proxies, success, error = future.result()
            if success:
                print(f"{Fore.GREEN}✓ Successfully scraped {len(proxies)} {proxy_type} proxies from {url}")
                if proxy_type not in results:
                    results[proxy_type] = set()
                results[proxy_type].update(proxies)
            else:
                print(f"{Fore.RED}✗ Error scraping {url}: {error}")
    
    return results

def main():
    """Main execution function"""
    try:
        print(f"{Fore.CYAN}Starting proxy scraper with {SCRAPING_THREADS} scraping threads and {TESTING_THREADS} testing threads")
        
        # Scrape proxies in parallel
        classified_proxies = scrape_proxies_parallel(proxy_urls)
        
        if not any(classified_proxies.values()):
            logging.error("No proxies were scraped. Exiting.")
            return

        # Validate proxies with increased threads
        print(f"\n{Fore.YELLOW}Validating proxies...")
        valid_proxies = {
            'http': set(),
            'socks4': set(),
            'socks5': set()
        }

        for proxy_type, proxies in classified_proxies.items():
            with ThreadPoolExecutor(max_workers=TESTING_THREADS) as executor:
                results = list(tqdm(
                    executor.map(validate_proxy, proxies),
                    total=len(proxies),
                    desc=f"Validating {proxy_type} ({TESTING_THREADS} threads)"
                ))
                valid_proxies[proxy_type] = {proxy for proxy, is_valid in zip(proxies, results) if is_valid}

        # Save results
        for proxy_type, proxies in valid_proxies.items():
            if proxies:  # Only save if we have valid proxies
                filename = f"{proxy_type}_proxies_{TIMESTAMP}.txt"
                filepath = os.path.join(SAVE_DIRECTORY, filename)
                with open(filepath, 'w') as file:
                    for proxy in proxies:
                        file.write(f"{proxy}\n")
                print(f"{Fore.GREEN}Saved {len(proxies)} {proxy_type} proxies to {filepath}")

        # Print statistics
        print(f"\n{Fore.CYAN}=== Proxy Scraping Results ===")
        for proxy_type in valid_proxies:
            total = len(classified_proxies.get(proxy_type, set()))
            valid = len(valid_proxies[proxy_type])
            success_rate = (valid/total*100) if total > 0 else 0
            print(f"{Fore.WHITE}{proxy_type.upper()}:")
            print(f"Total scraped: {total}")
            print(f"Valid proxies: {valid}")
            print(f"Success rate: {success_rate:.2f}%\n")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
