# 🚀 Google Smart URL-Waiting Scraper

A high-performance, automated Python scraping tool designed to extract dynamic web URLs from Google Search results. This script handles background tab rendering, automates parameter filtering, flushes outputs directly into CSV streams, and includes smart mechanisms to bypass browser delays and captcha restrictions.

## ✨ Features
* **Smart Tab Handling:** Automatically switches between window handles to process individual search results sequentially.
* **Human-like Emulation:** Simulates randomized mouse offsets and uniform delays to reduce detection risks during navigation.
* **Automatic Dependency Installer:** Safely auto-installs missing core system libraries like `pyautogui` during runtime.
* **`about:blank` Bypass Engine:** Embedded logical validation timers skip frozen or failed page allocations to keep the execution moving smoothly.
* **Live CSV Streaming:** Automatically appends scraped links into target database spreadsheets instantly, preventing data loss during crashes.

## 🛠️ System Prerequisites
Before executing the application, ensure your computing machine complies with the following baseline criteria:
* **Python Runtime Engine:** Version 3.8 or higher installed (v3.10+ highly recommended).
* **Google Chrome Web Browser:** Must be installed on your desktop (Selenium automatically manages the matching drivers).

---

## 📥 How to Download and Run from GitHub

The project file downloading method is exactly identical across all platforms, but the terminal commands to initialize and run the script vary based on your operating system. Follow the specific instructions for your machine below.

### 1. Download the Project (Same for All OS)
* Click the green **"Code"** button at the top right of this GitHub page and select **"Download ZIP"**.
* Once downloaded, extract the ZIP file into a fresh folder on your computer.

### 2. Run Commands Based on Your Operating System

#### 🪟 For Windows Users
Open **Command Prompt** (cmd) or **PowerShell** *inside your extracted project folder* and run these commands sequentially:
```cmd
# 1. Initialize the virtual environment directory
python -m venv env

# 2. Activate the environment workspace
.\env\Scripts\activate

# 3. Install all package dependencies
pip install -r requirements.txt

# 4. Execute the application script
python main.py
```

#### 🍏 For macOS Users
Open your **Terminal** *inside your extracted project folder* and run these commands sequentially:
```bash
# 1. Initialize the virtual environment directory
python3 -m venv env

# 2. Activate the environment workspace
source env/bin/activate

# 3. Install all package dependencies
pip install -r requirements.txt

# 4. Execute the application script
python3 main.py
```

#### 🐧 For Linux Users
Open your **Terminal** *inside your extracted project folder* and run these commands sequentially:
```bash
# 1. Initialize the virtual environment directory
python3 -m venv env

# 2. Activate the environment workspace
source env/bin/activate

# 3. Install all package dependencies
pip install -r requirements.txt

# 4. Execute the application script
python3 main.py
```

---

## 🚀 Usage Blueprint
1. When the script boots up in your terminal, it will instantly ask for your filtration parameters:
   * **Enter Path:** Provide your filtration text boundary (e.g., `/shop` or `/product`).
   * **Enter Parameter:** Provide your target query string matching criteria (e.g., `id` or `category`).
2. An automated Chrome browser instance will open. **Type or paste your search query directly into the browser's search field and press ENTER.**
3. Sit back and watch. The script will automatically scrape organic search results page-by-page.

## 📂 Output Artifacts
* `raw_scraped_links.csv`: A live tracking repository containing every unique external link processed from the search query.
* `filtered_links_[Path_Param].csv`: A dedicated, clean spreadsheet holding only the target URLs that successfully matched your path and parameter criteria.

---
⚠️ **Disclaimer:** This script is developed purely for educational and research analytical evaluation workflows. Ensure target host compliance checks (`robots.txt`) are performed regularly to adhere to standard automated exploration usage guidelines.
