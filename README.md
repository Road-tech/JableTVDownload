# JableTVDownload

## 下載JableTV好幫手

每次看正要爽的時候就給我卡住轉圈圈  

直接下載到電腦看沒煩惱

---

## 🐳 Docker 一鍵啟動（推薦）

不需要手動安裝 ChromeDriver、FFmpeg、Python 環境，全部封裝在容器內。

### 前置需求
- 安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 使用方法

```bash
# 1. 建立 image
docker build -t jable-downloader .

# 2. 執行（互動模式，下載影片存至本機 downloads 資料夾）
docker run -it -v D:\downloads:/downloads jable-downloader
```

### Docker 進階使用

#### 使用設定檔 (config.json)

將本機的 `config.json` 掛載到容器內，即可使用自訂設定：

```bash
docker run -it \
  -v ./downloads:/downloads \
  -v ./config.json:/app/config.json \
  -e URL="https://jable.tv/videos/xxx/" \
  jable-downloader
```

#### 使用環境變數設定選項

也可以透過環境變數直接設定，無需修改設定檔：

```bash
docker run -it \
  -v ./downloads:/downloads \
  -v ./config.json:/app/config.json \
  -e URL="https://jable.tv/videos/xxx/" \
  -e PROXY="http://proxy.example.com:8080" \
  -e ENABLE_PROXY="true" \
  -e COVER="False" \
  -e QUALITY="2" \
  jable-downloader
```

| 環境變數 | 說明 |
| :--- | :--- |
| `SERVER` | 啟動 Webhook 伺服器 (true) |
| `HOST` | 伺服器監聽位址 (預設: 0.0.0.0) |
| `PORT` | 伺服器端口 (預設: 5000) |
| `URL` | 影片網址 |
| `RANDOM` | 下載隨機熱門影片 (true/false) |
| `ALL_URLS` | 演員頁網址，下載所有影片 |
| `CONFIG` | 自訂設定檔路徑 (容器內) |
| `PROXY` | 代理位址 |
| `ENABLE_PROXY` | 啟用代理 (true) |
| `DISABLE_PROXY` | 停用代理 (true) |
| `COVER` | 是否下載封面 (true/false) |
| `ENCODE` | 是否轉碼 (true/false) |
| `QUALITY` | 轉碼品質 (1/2/3) |

#### 使用 Docker Compose

```bash
# 1. 修改 docker-compose.yml 中的環境變數
# 2. 啟動
docker-compose up --build
```

---

## 🌐 Webhook API 服務

支援透過 HTTP API 呼叫下載任務，方便與其他系統整合。

### 啟動 Webhook 伺服器

```bash
# 直接執行
python main.py --server --host 0.0.0.0 --port 5000

# Docker 方式（推薦掛載 config.json 以持久化配置）
docker run -it -p 5000:5000 \
  -v $(pwd)/downloads:/downloads \
  -v $(pwd)/config.json:/app/config.json \
  -e SERVER="true" \
  jable-downloader
```

> ⚠️ **注意**：建議掛載 `config.json` 以確保配置持久化。透過 API 更新的配置會保存到此檔案，容器重啟後仍然有效。

### API 端點

| 端點 | 方法 | 說明 |
| :--- | :--- | :--- |
| `/health` | GET | 健康檢查 |
| `/api/download` | POST | 新增下載任務 |
| `/api/config` | GET | 取得當前配置 |
| `/api/config` | PUT/POST | 更新配置 |
| `/api/tasks` | GET | 取得下載任務列表 |

### API 使用範例

#### 1. 新增下載任務

```bash
curl -X POST http://localhost:5000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://jable.tv/videos/xxx/"}'
```

可選參數：
```json
{
  "url": "https://jable.tv/videos/xxx/",
  "cover": true,
  "encode": true,
  "quality": 1,
  "proxy": "http://proxy.example.com:8080"
}
```

#### 2. 取得當前配置

```bash
curl http://localhost:5000/api/config
```

#### 3. 更新配置

```bash
curl -X PUT http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{
    "proxy": {
      "enabled": true,
      "url": "http://proxy.example.com:8080"
    },
    "download": {
      "cover": false,
      "quality": 2
    }
  }'
```

#### 4. 查看下載任務

```bash
curl http://localhost:5000/api/tasks
```

---

## 💻 傳統安裝（Windows）

1. 請自行安裝 ffmpeg，裝完之後執行 INIT.bat 將會自動建置其餘環境。
2. 若收到可以執行 RUN.bat 之訊息，執行 RUN.bat 即可使用此神器。

### 1. 搭建並啟用虛擬環境

```
python -m venv jable
jable/Scripts/activate
```
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/createVenv.PNG)

### 2. 下載所需套件

```
pip install -r requirements.txt
```

安裝 [FFmpeg] 用於轉檔

### 3. 執行程式

```
python main.py
```

### 4. 輸入影片網址
`https://jable.tv/videos/ipx-486/`  
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/download2.PNG)

### 5. 等待下載與合成

下載和合成影片皆有即時進度條顯示：

```
⬇ 下載進度:  73%|██████████████░░░░░  | 1334/1827 [01:12<00:27, 18.2片段/s]
🎬 合成影片:  45%|█████████░░░░░░░░░░░ |  821/1827 [01:23<01:40]
```

### 6. 完成

![image](https://github.com/hcjohn463/JableDownload/blob/main/img/demo2.png)

### 如果覺得好用 再麻煩給個星星好評 謝謝!!

---

[FFmpeg]:<https://www.ffmpeg.org/>

---

## 📋 配置文件 (config.json)

程式支援透過 JSON 設定檔管理常用設定，無需每次輸入參數。預設使用 `config.json`。

### 設定檔架構

```json
{
    "proxy": {
        "enabled": false,
        "url": "http://proxy.example.com:8080"
    },
    "download": {
        "cover": true,
        "encode": true,
        "quality": 1
    }
}
```

### 設定說明

| 設定項 | 說明 | 預設值 |
| :--- | :--- | :--- |
| **proxy.enabled** | 是否啟用代理 | `false` |
| **proxy.url** | 代理伺服器位址 (需搭配 `enabled: true`) | 空字串 |
| **download.cover** | 是否下載影片封面 | `true` |
| **download.encode** | 是否使用 FFmpeg 轉碼優化 (可邊下載邊播放) | `true` |
| **download.quality** | 轉碼品質 (1=最快, 2=適中, 3=最佳) | `1` |

### 使用自訂設定檔

```bash
python main.py --config my_config.json --url <網址>
```

### 指令列參數優先順序

指令列參數優先權高於設定檔，例如：

```bash
# 使用設定檔的代理設定，但關閉封面下載
python main.py --url <網址> --cover False
```

---

## Argument Parser

```bash
python main.py -h

# Webhook 伺服器模式
python main.py --server                    # 啟動 Webhook 伺服器
python main.py --server --host 0.0.0.0 --port 5000  # 自訂監聽位址和端口

# 下載模式
python main.py --random True       # 下載隨機熱門影片
python main.py --url <網址>         # 直接指定 URL
python main.py --all-urls <演員頁>  # 下載演員所有影片

# 設定檔相關
python main.py --config my_config.json  # 使用自訂設定檔

# 代理相關
python main.py --enable-proxy                          # 啟用代理
python main.py --disable-proxy                         # 停用代理
python main.py --proxy "http://proxy.example.com:8080" # 設定代理位址

# 下載選項
python main.py --cover False  # 不下載封面
python main.py --encode False # 不進行轉碼
python main.py --quality 2    # 設定轉碼品質 (1/2/3)
```

---

## ☸️ Kubernetes 支援

`k8s/` 資料夾內含完整 Kubernetes 配置，可將下載任務部署為 K8s Job：

```bash
kubectl apply -f k8s/pvc.yaml        # 建立持久化儲存
kubectl apply -f k8s/configmap.yaml  # 套用設定
kubectl apply -f k8s/job.yaml        # 執行下載任務
kubectl get jobs                      # 查看任務狀態
```

---

## 📜 更新日誌 (Update Log)

| 版本 | 日期 | 內容 |
| :--- | :--- | :--- |
| **v2.2** | 2026/05/30 | 🌐 新增 Webhook API 服務 |
| | | 📡 支援 HTTP API 新城下載任務、更新設定 |
| **v2.1** | 2026/05/30 | ⚙️ 新增 `config.json` 設定檔系統 |
| | | 🚀 支援透過設定檔管理代理、封面下載、轉碼等選項 |
| **v2.0** | 2026/03/15 | 🐳 支援 Docker 容器化部署、☸️ K8s (Job/PVC/ConfigMap) 支援 |
| | | 📊 下載與合成加入 `tqdm` 即時進度條、🚀 優化合成與轉檔速度 |
| **v1.11**| 2023/04/19 | 🦕 新增 ffmpeg 自動轉檔 |
| **v1.10**| 2023/04/19 | 🏹 兼容 Ubuntu Server |
| **v1.9** | 2023/04/15 | 🦅 下載演員所有相關影片 |
| **v1.8** | 2022/01/25 | 🚗 下載結束後自動抓取封面 |
| **v1.7** | 2021/06/04 | 🐶 更改 m3u8 獲取方法 (正則表達式) |
| **v1.6** | 2021/05/28 | 🌏 支援 Unix 系統 (Mac, Linux 等) |
| **v1.5** | 2021/05/27 | 🍎 更新爬蟲網頁方法 |
| **v1.4** | 2021/05/20 | 🌳 修改編碼問題 |
| **v1.3** | 2021/05/06 | 🌈 增加下載進度提示、修改 Crypto 問題 |
| **v1.2** | 2021/05/05 | ⭐ 更新穩定版本 |
