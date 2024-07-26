import requests
import re
from colorama import Fore, init

init()
# Define the URLs for scraping proxy lists
proxy_urls = [
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=text&timeout=20000",
    "https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt",
    "https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt",
    "https://github.com/TheSpeedX/PROXY-List/blob/master/socks4.txt",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.proxy-list.download/api/v1/get?type=http",
]

# Initialize an empty list to store all proxies
all_proxies = []

# Send GET requests to each URL and extract proxies
for url in proxy_urls:
    response = requests.get(url)
    proxy_urls = ["***" if "proxyscrape" not in url else url for url in proxy_urls]
    print(Fore.YELLOW + "Start Scraping Proxies From:  "  )  # Yellow color for the message

    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the proxies from the response
        if "proxyscrape" in url:
            proxies = response.text.split('\n')
        else:
            proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', response.text)
        
        # Add the proxies from the current source to the master list
        all_proxies.extend(proxies)
        print(f"Proxies from {url} added to the list.")
    else:
        print(f"Failed to retrieve proxy list from {url}. Status code: {response.status_code}")

# Save all the proxies to a file
with open("proxies.txt", 'w') as file:
    for proxy in all_proxies:
        file.write(proxy + '\n')

print("All proxies saved to 'proxies.txt'.")
