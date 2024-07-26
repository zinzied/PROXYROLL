PROXYROLL is a proxy testing and scraping tool. It helps users in their quest for finding and validating proxies from various sources (you can add your own sources) in scraper.py. 

The app provides an efficient way to collect and verify the validity of proxies, making it a valuable asset for anyone in need of reliable proxy lists. Here's a breakdown of its key features and usage:
### 1. Proxy Scraping:
   - PROXYROLL can scrape proxies from various websites that offer proxy lists.
   - It has a list of predefined URLs to source these proxies, including both HTTP and SOCKS proxies.
   - Users can easily update the URL sources for more flexibility.

### 2. Proxy Testing:
   - The main functionality of PROXYROLL is to test the validity of proxies.
   - It sends requests through each proxy to a test URL, checking their reachability and responsiveness.
   - The tool handles common issues like timeouts and connection errors gracefully.

### 3. Concurrent Testing:
   - To increase efficiency, the app utilizes multithreading. It can handle up to 10 threads running concurrently, which speeds up the proxy testing process significantly.

### 4. Organized Valid Proxy Storage:
   - PROXYROLL categorizes valid proxies based on their types (HTTP, SOCKS4, SOCKS5).
   - These valid proxies are saved into separate files, making it convenient for users to access and use them later.

### 5. User-Friendly Logging:
   - Throughout the proxy scraping and testing process, PROXYROLL provides detailed logs, ensuring users are well informed.
   - It distinguishes between normal messages, warnings, and errors using color-coded logging.

### 6. Customizable:
   - The application allows users to customize the sources from which proxies are scraped.
   - Users can also specify the input file containing proxies to be tested.

### Usage:
   - PROXY is a command-line tool, and its usage goes like this:
     - Run the script with the `--scrape` flag to scrape proxies from the predefined sources.
     - Alternatively, provide the path to a file containing proxies to test them.
   - The tool will then proceed to scrape or test proxies, logging its progress and storing valid proxies in the respective output files.

In summary, PROXYROLL is an efficient and informative proxy testing and scraping tool. Its concurrent testing, organized results, and user-friendly interface make it a handy addition to anyone needing to work with proxies, whether for web scraping, anonymity, or any other purpose. It's a roll of the dice that's bound to bring you good proxies!
