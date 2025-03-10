# PROXYROLL
# Author: Zied Boughdir
# Email ziedboughdir@gmail.com
# GitHub: https://github.com/zinzied
import sys
import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import concurrent.futures
import logging
from colorama import init, Fore, Style
import re
import pyfiglet  # For ASCII art
from threading import Lock
from scraper import main as scrape_proxies

# Initialize Colorama
init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize lock for thread-safe file writing
file_lock = Lock()

# Print a welcome message
def print_welcome_message():
    # Larger logo for 'H' using block characters
    logo = """
██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗  ██████╗ ██╗     ██╗     
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔═══██╗██║     ██║     
██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ ██████╔╝██║   ██║██║     ██║     
██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  ██╔══██╗██║   ██║██║     ██║     
██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║╚██████╔╝███████╗███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
                                                                                                                                                             
    """
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "     Proxy Testing Script     ")
    
    # Print Emoji-style logo
    print(Fore.GREEN + Style.BRIGHT + logo)
    
    # Create a large ASCII art version of your name
    ascii_name = pyfiglet.figlet_format("BY ZIED", font="univers")
    print(Fore.YELLOW + Style.BRIGHT + ascii_name)
    
    print(Fore.CYAN + Style.BRIGHT + "=============================")
    print(Fore.CYAN + Style.BRIGHT + " Enjoy the Proxies Checker!! ")
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Style.RESET_ALL)

# Function to read proxies from file and normalize them
def read_proxies_from_file(filename):
    try:
        with open(filename, 'r') as file:
            proxies = file.readlines()
        # Normalize proxies: remove prefixes and extra spaces
        normalized_proxies = []
        for proxy in proxies:
            proxy = proxy.strip()
            # Remove protocol prefixes
            proxy = re.sub(r'^socks4://|^socks5://|^http://|^https://', '', proxy)
            normalized_proxies.append(proxy)
        return normalized_proxies
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
        return []

# Function to generate a random user agent
def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

# Function to determine proxy type based on port
def determine_proxy_type(proxy):
    if ':80' in proxy or ':443' in proxy:
        return 'http'
    if ':1080' in proxy or ':1081' in proxy:
        return 'socks5'
    if ':5210' in proxy:
        return 'socks4'
    return 'unknown'

# Function to test proxy connectivity
def check_proxy(proxy, valid_proxies):
    user_agent = get_random_user_agent()
    headers = {'User-Agent': user_agent}
    
    proxy_type = determine_proxy_type(proxy)
    
    proxy_dict = {
        "http": proxy if proxy_type == 'http' else None,
        "https": proxy if proxy_type == 'http' else None
    }
    
    retries = 100  # Number of retries
    timeout = 5  # Initial timeout
    for attempt in range(retries):
        try:
            url = 'http://httpbin.org/get'
            r = requests.get(url, proxies=proxy_dict, headers=headers, timeout=timeout)
            if r.status_code == 200:
                # Save valid proxy immediately
                filename = {
                    'http': "http-valid.txt",
                    'socks4': "socks4-valid.txt",
                    'socks5': "socks5-valid.txt"
                }.get(proxy_type, None)
                
                if filename:
                    print(Fore.GREEN + f"Proxy {proxy} is valid." + Style.RESET_ALL)
                    valid_proxies.append(proxy)
                    
                    # Use lock to ensure thread-safe file writing
                    with file_lock:
                        with open(filename, 'a') as file:
                            file.write(proxy + "\n")
                return
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout occurred for proxy {proxy} on attempt {attempt + 1}. Retrying...")
        except requests.exceptions.ConnectionError:
            logging.error(f"Connection error for proxy {proxy}.")
            break  # No point in retrying if connection error occurred
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception for proxy {proxy}: {str(e)}")
        time.sleep(2 ** attempt)  # Exponential backoff for retry
        timeout *= 2  # Double the timeout for next retry
    print(Fore.RED + f"Proxy {proxy} is not valid." + Style.RESET_ALL)

def main():
    print_welcome_message()
    
    try:
        # Call the scraper
        print(f"{Fore.CYAN}Starting proxy scraper...{Style.RESET_ALL}")
        scrape_proxies()
        print(f"{Fore.GREEN}Proxy scraping completed! Check the 'proxies' folder for results.{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Scraping interrupted by user.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
