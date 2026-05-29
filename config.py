import os
import json
from pathlib import Path

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
}

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    'proxy': {
        'enabled': False,
        'url': ''
    },
    'download': {
        'cover': True,
        'encode': True,
        'quality': 1
    }
}

config = DEFAULT_CONFIG.copy()

def load_config(config_file=None):
    global config
    if config_file is None:
        config_file = CONFIG_FILE

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                config = merge_config(DEFAULT_CONFIG, loaded)
            print(f'已加载配置文件: {config_file}')
        except Exception as e:
            print(f'加载配置文件失败: {e}, 使用默认配置')
            config = DEFAULT_CONFIG.copy()
    else:
        print(f'配置文件 {config_file} 不存在，使用默认配置')
        config = DEFAULT_CONFIG.copy()

    return config

def merge_config(default, loaded):
    result = default.copy()
    for key, value in loaded.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result

def save_config(config_file=None):
    if config_file is None:
        config_file = CONFIG_FILE

    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f'配置已保存到: {config_file}')
    except Exception as e:
        print(f'保存配置文件失败: {e}')

def get_proxy():
    if config.get('proxy', {}).get('enabled', False):
        return config.get('proxy', {}).get('url', '')
    return None

def get_proxy_dict():
    proxy_url = get_proxy()
    if proxy_url:
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    return None

def is_cover_enabled():
    return config.get('download', {}).get('cover', True)

def is_encode_enabled():
    return config.get('download', {}).get('encode', True)

def get_encode_quality():
    return config.get('download', {}).get('quality', 1)
