import sqlite3
import psutil
import time
import webbrowser
import pyautogui
import matplotlib.pyplot as plt
from datetime import datetime
import openai

# ===========================
# CONFIGURATION
# ===========================
OPENAI_API_KEY = "your-openai-api-key"  # Replace with your OpenAI API key
TRACKING_INTERVAL = 5  # Time interval in seconds


# ===========================
# STEP 1: Initialize Database
# ===========================
def init_db():
    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS sites (
                        url TEXT PRIMARY KEY, 
                        category TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tracking (
                        url TEXT, 
                        timestamp TEXT)''')

    non_productive_sites = [
        ("youtube.com", "non-productive"),
        ("netflix.com", "non-productive"),
        ("reddit.com", "non-productive"),
        ("instagram.com", "non-productive"),
        ("twitter.com", "non-productive"),
        ("tiktok.com", "non-productive"),
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO sites (url, category) VALUES (?, ?)", non_productive_sites)
    conn.commit()
    conn.close()

init_db()


# ===========================
# STEP 2: Get Active Browser URL
# ===========================
def get_active_browser_url():
    browser_processes = ["chrome", "firefox", "msedge", "brave", "opera"]

    for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        try:
            process_name = process.info["name"].lower()
            if any(browser in process_name for browser in browser_processes):
                cmdline = process.info["cmdline"]
                for arg in cmdline:
                    if "http" in arg or "www." in arg:
                        return arg
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None


# ===========================
# STEP 3: AI-Based Site Classification
# ===========================
def classify_website_with_ai(url):
    if not OPENAI_API_KEY:
        return "unknown"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Classify websites into productive or non-productive."},
                      {"role": "user", "content": f"Is {url} a productive or non-productive site?"}]
        )
        category = response["choices"][0]["message"]["content"].strip().lower()
        return category if category in ["productive", "non-productive"] else "unknown"
    except:
        return "unknown"


# ===========================
# STEP 4: Check Productivity & Alert
# ===========================
def check_productivity(url):
    if not url:
        return

    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    domain = url.replace("https://", "").replace("http://", "").split("/")[0]

    cursor.execute("SELECT category FROM sites WHERE url=?", (domain,))
    result = cursor.fetchone()

    if result:
        category = result[0]
    else:
        category = classify_website_with_ai(domain)
        cursor.execute("INSERT OR IGNORE INTO sites (url, category) VALUES (?, ?)", (domain, category))
        conn.commit()

    cursor.execute("INSERT INTO tracking (url, timestamp) VALUES (?, ?)", (domain, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


# ===========================
# STEP 5: Generate Productivity Report
# ===========================
def generate_report():
    conn = sqlite3.connect("productivity.db")
    cursor = conn.cursor()

    cursor.execute("SELECT url, COUNT(*) FROM tracking GROUP BY url ORDER BY COUNT(*) DESC")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No data to generate report.")
        return

    sites = [row[0] for row in data]
    times = [row[1] for row in data]

    plt.figure(figsize=(10, 10))
    plt.barh(sites, times, color="red")
    plt.xlabel("Time Spent")
    plt.ylabel("Website")
    plt.title("Productivity Report: Time Spent on Websites")
    plt.gca().invert_yaxis()
    plt.show()


# ===========================
# STEP 6: Run the Tracker
# ===========================
def run_tracker():
    print("🔵 Productivity Tracker Running...")
    while True:
        url = get_active_browser_url()
        check_productivity(url)
        time.sleep(TRACKING_INTERVAL)  # Check every 5 seconds

if __name__ == "__main__":
    run_tracker()
