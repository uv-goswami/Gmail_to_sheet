# Gmail to Google Sheet Automation

**Author:** Yuvraj Singh

---

# Project Overview

A python automation script that integrates with Gmail API and Google Sheets API to read unread emails from a Gmail inbox and marks them as read. It extracts the Sender, Subject, Date and Content and append to the sheet.

---

# Setup Instructions

### 1. Prerequisites

* Python 3.8+
* A Google Cloud Project with **Gmail API** and **Google Sheets API** enabled.
* `credentials.json` from the Google Cloud Console (OAuth 2.0 Client ID).

### 2. Installation

1. **Clone the repository:**

```
git clone https://github.com/uv-goswami/Gmail_to_sheet
cd Gmail_to_sheet
```


2. **Create and activate a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate
```


3. **Install dependencies:**
```
pip install -r requirements.txt

```


4. **Configuration:**
* Place your downloaded `credentials.json` inside the `credentials/` folder.
* Create a `.env` file in the root directory:
```env
SPREADSHEET_ID=your_spreadsheet_id_here
SHEET_NAME=Sheet1
```





### 3. Running the Script

Run the main entry point:

```bash
python src/main.py
```

On the first run, a browser window will open asking you to log in and authorize the app.

---
