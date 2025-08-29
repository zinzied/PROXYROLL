from flask import Flask, render_template
import os

app = Flask(__name__)

def read_proxy_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

@app.route('/')
def index():
    proxies_dir = 'proxies'
    http_proxies = read_proxy_file(os.path.join(proxies_dir, 'http-valid.txt'))
    socks4_proxies = read_proxy_file(os.path.join(proxies_dir, 'socks4-valid.txt'))
    socks5_proxies = read_proxy_file(os.path.join(proxies_dir, 'socks5-valid.txt'))
    
    return render_template('index.html', 
                           http_proxies=http_proxies,
                           socks4_proxies=socks4_proxies,
                           socks5_proxies=socks5_proxies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
