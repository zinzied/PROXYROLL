import os
import requests
import re
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from tqdm import tqdm
import socket
import time
from datetime import datetime
import logging
import random
import threading
import sys

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
TESTING_THREADS = 500  # Threads for proxy testing (increased for faster validation)
TIMEOUT = 5  # Connection timeout
SAVE_DIRECTORY = os.path.join(os.path.dirname(__file__), "proxies")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Animation configuration
ANIMATION_ACTIVE = False  # Flag to control animation thread
ANIMATION_SPEED = 0.05  # Animation refresh rate in seconds (faster for smoother animation)
ANIMATION_LOCK = threading.Lock()  # Lock for thread-safe animation updates
CURRENT_PROXY_INFO = {"type": "", "count": 0, "total_scraped": 0, "mode": "scraping", "progress": 0, "total": 0}  # Current proxy info for animation

# Scraping delay (in seconds) to slow down the process and better see the animation
SCRAPING_DELAY = 2.0  # Add a delay between scraping operations
VALIDATION_DELAY = 0.05  # Reduced delay between validation operations for faster processing

# Create save directory
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

# Define the URLs for scraping proxy lists
proxy_urls = [
    # Existing sources
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

    # Additional sources
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://proxyspace.pro/socks5.txt",
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

def update_proxy_info(proxy_type, count, mode="scraping", progress=0, total=0):
    """Update the current proxy info for the animation thread"""
    with ANIMATION_LOCK:
        CURRENT_PROXY_INFO["type"] = proxy_type
        CURRENT_PROXY_INFO["count"] = count
        CURRENT_PROXY_INFO["mode"] = mode
        CURRENT_PROXY_INFO["progress"] = progress
        CURRENT_PROXY_INFO["total"] = total

def run_animation():
    """Run a continuous animation in a separate thread"""
    # Animation characters (Braille patterns for a spinning effect)
    animation_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']

    # Flowing animation patterns
    flow_patterns = [
        '▁▂▃▄▅▆▇█▇▆▅▄▃▂▁',
        '←←←←←←←←',
        '→→→→→→→→',
        '▌▀▐▄',
        '▖▘▝▗',
        '▉▊▋▌▍▎▏▎▍▌▋▊▉',
        '▁▃▄▅▆▇█▇▆▅▄▃▁'
    ]

    # Progress bar characters
    progress_chars = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']

    # Cool symbols for variety
    symbols = ['🔄', '✨', '🔍', '📡', '🌐', '⚡', '💻', '🔎', '📶', '🛰️']

    # Error symbols
    error_symbols = ['❌', '⚠️', '🚫', '⛔', '🔴']

    # Colors for visual appeal
    colors = [Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

    frame = 0
    symbol_idx = 0
    color_idx = 0
    error_idx = 0
    flow_idx = 0
    flow_pos = 0

    while ANIMATION_ACTIVE:
        with ANIMATION_LOCK:
            proxy_type = CURRENT_PROXY_INFO["type"]
            count = CURRENT_PROXY_INFO["count"]
            mode = CURRENT_PROXY_INFO["mode"]
            progress = CURRENT_PROXY_INFO["progress"]
            total = CURRENT_PROXY_INFO["total"]

        # Clear the current line
        sys.stdout.write("\r" + " " * 120)

        if proxy_type == "error":
            # Display error animation
            error_symbol = error_symbols[error_idx]
            flow_char = flow_patterns[flow_idx][flow_pos % len(flow_patterns[flow_idx])]
            sys.stdout.write(f"\r{Fore.RED}{error_symbol} {flow_char} Error scraping a source {flow_char} {error_symbol}")
            error_idx = (error_idx + 1) % len(error_symbols)
        elif mode == "validating" and total > 0:
            # Get animation character based on frame
            char = animation_chars[frame % len(animation_chars)]

            # Get flow pattern character
            flow_char = flow_patterns[flow_idx][flow_pos % len(flow_patterns[flow_idx])]

            # Get symbol and color based on frame for smooth transitions
            symbol = symbols[symbol_idx]
            color = colors[color_idx]

            # Calculate percentage
            percentage = (progress / total) * 100 if total > 0 else 0

            # Create a custom progress bar
            progress_bar_length = 20
            filled_length = int(progress_bar_length * progress // total) if total > 0 else 0
            progress_bar = '█' * filled_length + '░' * (progress_bar_length - filled_length)

            # Display the validation animation with progress bar and percentage
            sys.stdout.write(f"\r{color}{char} {flow_char} {symbol} Validating {proxy_type} proxies: [{progress_bar}] {percentage:.1f}% ({progress}/{total}) {symbol} {flow_char} {char}")
        elif proxy_type and count > 0:
            # Get animation character based on frame
            char = animation_chars[frame % len(animation_chars)]

            # Get flow pattern character
            flow_char = flow_patterns[flow_idx][flow_pos % len(flow_patterns[flow_idx])]

            # Get symbol and color based on frame for smooth transitions
            symbol = symbols[symbol_idx]
            color = colors[color_idx]

            # Display the animation with flowing pattern
            sys.stdout.write(f"\r{color}{char} {flow_char} {symbol} Successfully scraped {count} {proxy_type} proxies {symbol} {flow_char} {char}")

        # Update all animation counters
        frame = (frame + 1) % len(animation_chars)
        flow_pos = (flow_pos + 1) % len(flow_patterns[flow_idx])

        # Occasionally change various animation elements
        if frame % 3 == 0:  # More frequent updates for smoother animation
            symbol_idx = (symbol_idx + 1) % len(symbols)
        if frame % 7 == 0:
            color_idx = (color_idx + 1) % len(colors)
        if frame % 15 == 0:
            flow_idx = (flow_idx + 1) % len(flow_patterns)

        sys.stdout.flush()
        time.sleep(ANIMATION_SPEED)

def display_scraping_animation(proxy_type, count):
    """Update the proxy info for the animation thread for scraping mode"""
    update_proxy_info(proxy_type, count, mode="scraping")

def display_validation_animation(proxy_type, progress, total):
    """Update the proxy info for the animation thread for validation mode"""
    update_proxy_info(proxy_type, 0, mode="validating", progress=progress, total=total)

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
                # Use animation instead of showing the URL
                display_scraping_animation(proxy_type, len(proxies))
                if proxy_type not in results:
                    results[proxy_type] = set()
                results[proxy_type].update(proxies)

                # Add a delay to slow down the scraping process and better see the animation
                time.sleep(SCRAPING_DELAY)
            else:
                # For errors, just update the animation with error info
                # We'll use a special "error" type to indicate an error
                update_proxy_info("error", 0)

                # Brief pause to show the error in the animation
                time.sleep(1.0)

    return results

def main():
    """Main execution function"""
    global ANIMATION_ACTIVE

    try:
        print(f"{Fore.CYAN}Starting proxy scraper with {SCRAPING_THREADS} scraping threads and {TESTING_THREADS} testing threads")

        # Start animation thread
        ANIMATION_ACTIVE = True
        animation_thread = threading.Thread(target=run_animation, daemon=True)
        animation_thread.start()

        # Scrape proxies in parallel
        classified_proxies = scrape_proxies_parallel(proxy_urls)

        # Stop animation thread
        ANIMATION_ACTIVE = False
        animation_thread.join(timeout=1.0)

        # Clear the animation line
        sys.stdout.write("\r" + " " * 100)
        sys.stdout.write("\r")
        sys.stdout.flush()

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

        # Start animation thread again for validation
        ANIMATION_ACTIVE = True
        animation_thread = threading.Thread(target=run_animation, daemon=True)
        animation_thread.start()

        for proxy_type, proxies in classified_proxies.items():
            proxies_list = list(proxies)  # Convert set to list for indexing
            total_proxies = len(proxies_list)
            valid_count = 0

            # Initialize the validation animation
            display_validation_animation(proxy_type, 0, total_proxies)

            with ThreadPoolExecutor(max_workers=TESTING_THREADS) as executor:
                futures = {executor.submit(validate_proxy, proxy): i for i, proxy in enumerate(proxies_list)}

                # Process futures in batches to reduce animation update overhead
                completed_count = 0
                update_frequency = 50  # Update animation every 50 completed proxies

                for i, future in enumerate(concurrent.futures.as_completed(futures)):
                    proxy_index = futures[future]
                    proxy = proxies_list[proxy_index]
                    is_valid = future.result()

                    completed_count += 1

                    if is_valid:
                        valid_proxies[proxy_type].add(proxy)
                        valid_count += 1

                    # Update the animation less frequently to reduce overhead
                    if completed_count % update_frequency == 0 or completed_count == total_proxies:
                        display_validation_animation(proxy_type, completed_count, total_proxies)
                        # Brief delay only when updating the animation
                        time.sleep(VALIDATION_DELAY)

            # Print a newline after each proxy type validation is complete
            print()

        # Stop animation thread
        ANIMATION_ACTIVE = False
        animation_thread.join(timeout=1.0)

        # Clear the animation line
        sys.stdout.write("\r" + " " * 120)
        sys.stdout.write("\r")
        sys.stdout.flush()

        # Save results
        for proxy_type, proxies in valid_proxies.items():
            if proxies:  # Only save if we have valid proxies
                # Save with timestamp for archiving
                timestamp_filename = f"{proxy_type}_proxies_{TIMESTAMP}.txt"
                timestamp_filepath = os.path.join(SAVE_DIRECTORY, timestamp_filename)
                with open(timestamp_filepath, 'w') as file:
                    for proxy in proxies:
                        file.write(f"{proxy}\n")

                # Save with standard name for easy identification
                standard_filename = f"{proxy_type}-valid.txt"
                standard_filepath = os.path.join(SAVE_DIRECTORY, standard_filename)
                with open(standard_filepath, 'w') as file:
                    for proxy in proxies:
                        file.write(f"{proxy}\n")

                print(f"{Fore.GREEN}Saved {len(proxies)} {proxy_type} proxies to:")
                print(f"{Fore.GREEN}- {timestamp_filepath} (archived)")
                print(f"{Fore.GREEN}- {standard_filepath} (for easy access)")

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
