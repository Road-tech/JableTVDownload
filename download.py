
import requests
import os
import re
import urllib.request
import m3u8
from config import headers, get_proxy_dict
from crawler import prepareCrawl
from merge import mergeMp4
from encode import ffmpegEncode
from delete import deleteM3u8, deleteMp4
from cover import getCover
from args import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def download(url, proxy_url=None, download_cover=True, download_encode=True, encode_quality=1):

  print('正在下載影片: ' + url)
  if proxy_url:
      print(f'使用代理: {proxy_url}')

  urlSplit = url.split('/')
  dirName = urlSplit[-2]
  if os.path.exists(f'{dirName}/{dirName}.mp4'):
    print('番號資料夾已存在, 跳過...')
    return
  if not os.path.exists(dirName):
      os.makedirs(dirName)
  folderPath = os.path.join(os.getcwd(), dirName)

  options = Options()
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--disable-extensions')
  options.add_argument('--headless')
  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
  if proxy_url:
      options.add_argument(f'--proxy-server={proxy_url}')
  dr = webdriver.Chrome(options=options)
  dr.get(url)
  result = re.search("https://.+m3u8", dr.page_source)
  print(f'result: {result}')
  m3u8url = result[0]
  print(f'm3u8url: {m3u8url}')

  m3u8urlList = m3u8url.split('/')
  m3u8urlList.pop(-1)
  downloadurl = '/'.join(m3u8urlList)

  m3u8file = os.path.join(folderPath, dirName + '.m3u8')
  if proxy_url:
      proxy_handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
      opener = urllib.request.build_opener(proxy_handler)
      urllib.request.install_opener(opener)
  urllib.request.urlretrieve(m3u8url, m3u8file)

  m3u8obj = m3u8.load(m3u8file)
  m3u8uri = ''
  m3u8iv = ''

  for key in m3u8obj.keys:
      if key:
          m3u8uri = key.uri
          m3u8iv = key.iv

  tsList = []
  for seg in m3u8obj.segments:
      tsUrl = downloadurl + '/' + seg.uri
      tsList.append(tsUrl)

  if m3u8uri:
      m3u8keyurl = downloadurl + '/' + m3u8uri
      proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None
      response = requests.get(m3u8keyurl, headers=headers, timeout=10, proxies=proxies)
      contentKey = response.content
      vt = m3u8iv.replace("0x", "")[:16].encode()
      ci_params = {'key': contentKey, 'iv': vt}
  else:
      ci_params = None

  deleteM3u8(folderPath)

  prepareCrawl(ci_params, folderPath, tsList, proxy_url)

  mergeMp4(folderPath, tsList)

  if download_encode:
      print(f'開始轉檔 (質量模式: {encode_quality})')
      ffmpegEncode(folderPath, dirName, encode_quality)

  deleteMp4(folderPath)

  if download_cover:
      print('下載封面圖片...')
      getCover(html_file=dr.page_source, folder_path=folderPath, proxy_url=proxy_url)
