# ProductivityTracker

# 🧠 AI Productivity Tracker

A Python-based productivity tracking tool that monitors active browser usage, classifies websites using AI, and generates visual reports of time spent on productive vs non-productive activities.

---

## 🚀 Overview

This application tracks which websites you visit in real time and logs activity into a local database. It uses AI to automatically classify websites as **productive** or **non-productive**, helping users better understand and optimize their time online.

---

## ✨ Features

* 🔍 **Real-Time Tracking**
  Detects active browser URLs using system process monitoring

* 🧠 **AI-Powered Classification**
  Uses OpenAI to categorize websites as productive or non-productive

* 🗄️ **Persistent Storage**
  Logs browsing activity into a local SQLite database

* 📊 **Data Visualization**
  Generates charts showing time spent per website

* ⚙️ **Customizable Tracking Interval**
  Adjustable frequency for monitoring activity

---

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:**

  * `sqlite3` – local database storage
  * `psutil` – system process monitoring
  * `matplotlib` – data visualization
  * `openai` – AI-based classification
  * `datetime`, `time` – scheduling and timestamps

---

## 🧩 How It Works

### 1. URL Detection

* Scans running processes using `psutil`
* Identifies active browser instances (Chrome, Firefox, Edge, etc.)
* Extracts the current URL from process arguments

### 2. Classification

* Checks if the domain already exists in the database
* If not, sends it to OpenAI for classification:

  * **Productive**
  * **Non-Productive**

### 3. Data Logging

* Stores:

  * Website domain
  * Timestamp of visit
* Uses SQLite for persistent storage

### 4. Reporting

* Aggregates time spent per site
* Displays a horizontal bar chart using `matplotlib`

---

## 🗃️ Database Schema

### `sites` Table

| Column   | Type | Description                 |
| -------- | ---- | --------------------------- |
| url      | TEXT | Website domain              |
| category | TEXT | productive / non-productive |

### `tracking` Table

| Column    | Type | Description    |
| --------- | ---- | -------------- |
| url       | TEXT | Website domain |
| timestamp | TEXT | Time of visit  |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/productivity-tracker.git
cd productivity-tracker
```

### 2. Install Dependencies

```bash
pip install psutil matplotlib openai pyautogui
```

### 3. Add Your OpenAI API Key

In the script:

```python
OPENAI_API_KEY = "your-openai-api-key"
```

---

## ▶️ Usage

Run the tracker:

```bash
python tracker.py
```

Generate a report (optional – call manually in code):

```python
generate_report()
```

---

## 📈 Example Output

* Tracks websites like:

  * youtube.com → non-productive
  * github.com → productive
* Generates a bar chart showing time spent per site

---

## ⚠️ Limitations

* URL detection depends on browser process arguments (may vary by system)
* AI classification may occasionally mislabel websites
* Tracks only active browser windows (not background tabs)

---

## 🔮 Future Improvements

* Real-time alerts for excessive non-productive usage
* Daily/weekly productivity summaries
* GUI dashboard
* Browser extension integration
* More granular categorization (e.g., learning, entertainment, work)

---

## 🧠 Key Learning Outcomes

* System-level process monitoring with `psutil`
* Database design with SQLite
* API integration (OpenAI)
* Data visualization with `matplotlib`
* Building end-to-end automation tools

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙌 Acknowledgements

* OpenAI API for intelligent classification
* Python open-source ecosystem

---
