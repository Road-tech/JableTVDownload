import argparse
from bs4 import BeautifulSoup
import random
from urllib.request import Request, urlopen
from config import headers
import re


def get_parser():
    parser = argparse.ArgumentParser(description="Jable TV Downloader")
    parser.add_argument("--server", action="store_true", help="啟動 Webhook 伺服器模式")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Webhook 伺服器位址 (預設: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Webhook 伺服器端口 (預設: 5000)")
    parser.add_argument("--config", type=str, default="", help="設定檔路徑 (預設: config.json)")
    parser.add_argument("--random", type=bool, default=False, help="Enter True for download random ")
    parser.add_argument("--url", type=str, default="", help="Jable TV URL to download")
    parser.add_argument("--all-urls", type=str, default="", help="Jable URL contains multiple avs")
    parser.add_argument("--proxy", type=str, default="", help="HTTP proxy URL (e.g., http://proxy.example.com:8080)")
    parser.add_argument("--enable-proxy", action="store_true", help="啟用代理 (需要配合 --proxy 使用)")
    parser.add_argument("--disable-proxy", action="store_true", help="停用代理")
    parser.add_argument("--cover", type=bool, default=None, help="是否下載封面圖片 (預設: True)")
    parser.add_argument("--encode", type=bool, default=None, help="是否轉碼影片 (預設: True)")
    parser.add_argument("--quality", type=int, default=None, help="轉碼品質 (1=最快, 2=適中, 3=最佳)")

    return parser


def av_recommand(proxy_url=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://jable.tv/'
    if proxy_url:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
    request = Request(url, headers=headers)
    web_content = urlopen(request).read()
    soup = BeautifulSoup(web_content, 'html.parser')
    h6_tags = soup.find_all('h6', class_='title')
    av_list = re.findall(r'https[^"]+', str(h6_tags))
    return random.choice(av_list)
