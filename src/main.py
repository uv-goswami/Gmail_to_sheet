import os
import json
import logging
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.gmail_service import GmailService
from src.sheets_service import SheetsService
from src.email_parser import EmailParser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def get_credentials():
    creds = None
    if os.path.exists(config.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                if os.path.exists(config.TOKEN_FILE):
                    os.remove(config.TOKEN_FILE)
                return get_credentials()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CREDENTIALS_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(config.TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    return creds

def load_state():
    if os.path.exists(config.STATE_FILE):
        try:
            with open(config.STATE_FILE, 'r') as f:
                data = json.load(f)
                return set(data.get("processed_ids", []))
        except json.JSONDecodeError:
            return set()
    return set()

def save_state(processed_ids):
    ids_list = list(processed_ids)[-1000:]
    with open(config.STATE_FILE, 'w') as f:
        json.dump({"processed_ids": ids_list}, f)

def main():
    logger.info("--- JOB START ---")
    
    try:
        creds = get_credentials()
    except Exception as e:
        logger.critical(f"Authentication failed: {e}")
        return

    gmail = GmailService(creds)
    sheets = SheetsService(creds)
    
    processed_ids = load_state()
    logger.info(f"Loaded state: {len(processed_ids)} previously processed emails.")

    messages = gmail.get_unread_emails()
    if not messages:
        logger.info("No unread emails found.")
        return

    new_count = 0
    
    for msg in messages:
        msg_id = msg['id']
        
        if msg_id in processed_ids:
            logger.info(f"Skipping known duplicate: {msg_id}")
            gmail.mark_as_read(msg_id) 
            continue

        try:
            full_msg = gmail.get_email_details(msg_id)
            if not full_msg: continue
            
            data = EmailParser.parse(full_msg)
            
            row = [data['from'], data['subject'], data['date'], data['content']]
            
            if sheets.append_email(row):
                gmail.mark_as_read(msg_id)
                processed_ids.add(msg_id)
                save_state(processed_ids)
                new_count += 1
                
        except Exception as e:
            logger.error(f"Error processing {msg_id}: {e}")

    logger.info(f"--- JOB DONE. Processed {new_count} new emails. ---")

if __name__ == "__main__":
    main()