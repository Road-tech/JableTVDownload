import threading
import json
import os
from flask import Flask, request, jsonify
from config import load_config, save_config, config
from download import download
import args

app = Flask(__name__)

# 下载任务队列（简单实现）
download_tasks = []

def download_task_wrapper(url, proxy_url, download_cover, download_encode, quality):
    """包装下载函数，用于线程中执行"""
    try:
        print(f"[Webhook] 开始下载: {url}")
        download(url, proxy_url, download_cover, download_encode, quality)
        print(f"[Webhook] 下载完成: {url}")
    except Exception as e:
        print(f"[Webhook] 下载失败: {url}, 错误: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "ok",
        "service": "jable-downloader-webhook"
    }), 200

@app.route('/api/download', methods=['POST'])
def download_endpoint():
    """下载任务端点"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: url"
            }), 400
        
        url = data['url']
        
        # 可选参数
        download_cover = data.get('cover', config.get('download', {}).get('cover', True))
        download_encode = data.get('encode', config.get('download', {}).get('encode', True))
        quality = data.get('quality', config.get('download', {}).get('quality', 1))
        
        # 获取代理配置
        if config.get('proxy', {}).get('enabled', False):
            proxy_url = config.get('proxy', {}).get('url', '')
        else:
            proxy_url = data.get('proxy', None)
        
        # 在新线程中执行下载
        thread = threading.Thread(
            target=download_task_wrapper,
            args=(url, proxy_url, download_cover, download_encode, quality)
        )
        thread.start()
        
        # 记录任务
        task_id = len(download_tasks) + 1
        download_tasks.append({
            "id": task_id,
            "url": url,
            "status": "started"
        })
        
        return jsonify({
            "status": "success",
            "message": "下载任务已添加",
            "task_id": task_id,
            "url": url
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    try:
        return jsonify({
            "status": "success",
            "config": config
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/config', methods=['PUT', 'POST'])
def update_config():
    """更新配置"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "请求体不能为空"
            }), 400
        
        # 合并配置
        for key, value in data.items():
            if key in config:
                if isinstance(config[key], dict) and isinstance(value, dict):
                    config[key].update(value)
                else:
                    config[key] = value
            else:
                config[key] = value
        
        # 保存配置
        save_config()
        
        return jsonify({
            "status": "success",
            "message": "配置已更新",
            "config": config
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取所有下载任务"""
    return jsonify({
        "status": "success",
        "tasks": download_tasks
    }), 200

def run_server(host='0.0.0.0', port=5000, debug=False):
    """运行 webhook 服务器"""
    print(f"[Webhook] 启动服务器: {host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)
