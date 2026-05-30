#!/usr/bin/env python
# coding: utf-8
from args import *
from download import download
from movies import movieLinks
from config import load_config, get_proxy, is_cover_enabled, is_encode_enabled, get_encode_quality, config
from webhook_server import run_server

parser = get_parser()
args = parser.parse_args()

config_file = args.config if args.config else None
load_config(config_file)

if args.proxy:
    config['proxy']['url'] = args.proxy
    config['proxy']['enabled'] = True

if args.enable_proxy:
    config['proxy']['enabled'] = True

if args.disable_proxy:
    config['proxy']['enabled'] = False

if args.cover is not None:
    config['download']['cover'] = args.cover

if args.encode is not None:
    config['download']['encode'] = args.encode

if args.quality is not None:
    config['download']['quality'] = args.quality

# Webhook 伺服器模式
if args.server:
    run_server(host=args.host, port=args.port)
else:
    proxy_url = get_proxy()
    download_cover = is_cover_enabled()
    download_encode = is_encode_enabled()
    encode_quality = get_encode_quality()

    if(len(args.url) != 0):
        url = args.url
        download(url, proxy_url, download_cover, download_encode, encode_quality)
    elif(args.random == True):
        url = av_recommand(proxy_url)
        download(url, proxy_url, download_cover, download_encode, encode_quality)
    elif(args.all_urls != ""):
        all_urls = args.all_urls
        urls = movieLinks(all_urls, proxy_url)
        for url in urls:
            download(url, proxy_url, download_cover, download_encode, encode_quality)
    else:
        url = input('輸入jable網址:')
        download(url, proxy_url, download_cover, download_encode, encode_quality)
