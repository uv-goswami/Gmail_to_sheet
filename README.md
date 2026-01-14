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

# Design Decision & Logic
1. **OAuth 2.0 Authentication**
I used `google-auth-oauthlib` library to handle OAuth flow. Because this is more securee than storing a password. It generates a 'token.json' after the first login, then it refreshes qutomatically for further runs.

2. **Duplicate Preventation**
The script uses two layers of protection: API Filter only requests Unread emails. State File-state.json stores the processed_ids so that even if an email remains unread due to a crash.

3. **State Persistence**
I chose a simple JSON file - state.json to store the ID of processed emails rather than a full database as JSON file is lightweight.This allows for near-instant checking ($O(1)$ time complexity) regardless of how many emails are processed.

# Limitations

1. **Local State**: If state.json is deleted, the script relies on Unreead label. If you have old unread emails, they might be duplicated.

2. **Attachment Handling**: Currently the script ignores attachments and images only extracting text content. 

3. **Content truncation**: To keep the sheet readable the mail content is truncated to the first 500 characters.

4. **Rate Limiting**: The script fetches maximum of 50 emails per run to preserve API quotas.

# Proof of Execution

1. **Gmail inbox with unread emails**
![01_unread_mails](<Output and Diagrams/01_Unread_gmail_before.png>)

2. **Gmail Authentication**
![02_01](<Output and Diagrams/02_gmail_authentication.png>)<br>
![02_02](<Output and Diagrams/02_2_authentication.png>) <br>
![02_03](<Output and Diagrams/02_3_allow.png>)
![02_04](<Output and Diagrams/02_4_oauth_finished.png>)

3. **Script Execution and Logs**

![03](<Output and Diagrams/03_mainpy_logs.png>)

4. **Google Sheet after Populating**
![04](<Output and Diagrams/04_sheet_after.png>)

5. **Inbox after execution**
![05](<Output and Diagrams/05_Read_mails_after.png>)

# Testing

1. **Duplicate Preventation** 

Run script twice consecutively

```bash
python3 src/main.py
```

**Output:**
![test_01](<Output and Diagrams/test_01.png>)

2. **New Emails After Processing**
Send yourself a new mail and Re-Run the script

```
python3 src/main.py
```

**Output:**
![test 02](<Output and Diagrams/test_02.png>)