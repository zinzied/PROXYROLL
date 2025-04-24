# 🚀 PROXYROLL 🚀

### 🔍 A powerful proxy testing and scraping tool that helps users find and validate proxies from various sources! 🔍

![image](https://github.com/user-attachments/assets/42d98e95-4a61-4ec0-807a-1d2988a4c333)

The app provides an efficient way to collect and verify the validity of proxies, making it a valuable asset for anyone in need of reliable proxy lists. Here's a breakdown of its key features and usage:
### 1. 🌐 Proxy Scraping:
   - PROXYROLL can scrape proxies from various websites that offer proxy lists.
   - It has a list of predefined URLs to source these proxies, including both HTTP and SOCKS proxies.
   - Users can easily update the URL sources for more flexibility.

### 2. 🧪 Proxy Testing:
   - The main functionality of PROXYROLL is to test the validity of proxies.
   - It sends requests through each proxy to a test URL, checking their reachability and responsiveness.
   - The tool handles common issues like timeouts and connection errors gracefully.

### 3. ⚡ Concurrent Testing:
   - To increase efficiency, the app utilizes multithreading.
   - Configurable thread counts:
     - Up to 30 threads for proxy scraping
     - Up to 100 threads for proxy testing
   - Significantly improved performance with parallel processing

### 4. 📁 Organized Valid Proxy Storage:
   - PROXYROLL categorizes valid proxies based on their types (HTTP, SOCKS4, SOCKS5)
   - Valid proxies are saved in two formats:
     - Standard names for easy access: `http-valid.txt`, `socks4-valid.txt`, `socks5-valid.txt`
     - Timestamped files for archiving: `http_proxies_YYYYMMDD_HHMMSS.txt`
   - Automated directory creation and management
   - Files are saved in a dedicated 'proxies' folder

### 5. 📊 User-Friendly Logging:
   - Comprehensive logging system with both file and console output
   - Color-coded progress bars showing real-time scraping and testing progress
   - Detailed statistics for each proxy type including:
     - Total proxies scraped
     - Number of valid proxies
     - Success rate percentage
   - Beautiful ASCII art interface with welcome message

### 6. 🛠️ Enhanced Features:
   - Improved proxy validation with multiple retry attempts
   - Automatic proxy type detection
   - Thread-safe file operations
   - Better error handling and reporting
   - Support for various proxy formats and automatic normalization

### 7. ⚙️ Technical Specifications:
   - Configurable timeout settings
   - Support for HTTP, SOCKS4, and SOCKS5 proxies
   - Parallel processing for both scraping and testing
   - Real-time progress tracking with tqdm
   - Automatic proxy format detection and cleaning

### 🚀 Usage:
```bash
# To start the proxy scraper:
python main.py

# The script will:
1. Display welcome message
2. Start scraping proxies from all sources
3. Test all scraped proxies
4. Save valid proxies in the 'proxies' folder with easy-to-identify names
5. Show detailed statistics
```

### 📂 Output Structure:
```
PROXYROLL/
├── proxies/
│   ├── http-valid.txt                    # Easy access to HTTP proxies
│   ├── socks4-valid.txt                  # Easy access to SOCKS4 proxies
│   ├── socks5-valid.txt                  # Easy access to SOCKS5 proxies
│   ├── http_proxies_YYYYMMDD_HHMMSS.txt  # Archived HTTP proxies
│   ├── socks4_proxies_YYYYMMDD_HHMMSS.txt # Archived SOCKS4 proxies
│   └── socks5_proxies_YYYYMMDD_HHMMSS.txt # Archived SOCKS5 proxies
└── scraper.log
```

### 💖 Donations
If you feel like showing your love and/or appreciation for this simple project, then how about buying me a coffee or milk? ☕🥛

[<img src="https://github.com/zinzied/Website-login-checker/assets/10098794/24f9935f-3637-4607-8980-06124c2d0225">](https://www.buymeacoffee.com/Zied)


