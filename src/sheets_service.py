import logging
from googleapiclient.discovery import build
import config

logger = logging.getLogger(__name__)

class SheetsService:
    def __init__(self, creds):
        self.service = build('sheets', 'v4', credentials=creds)
        self.spreadsheet_id = config.SPREADSHEET_ID

    def append_email(self, row_data):
        body = {'values': [row_data]}
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{config.SHEET_NAME}!A:D",
                valueInputOption="RAW",
                body=body
            ).execute()
            logger.info(f"Appended: {row_data[1][:30]}...")
            return True
        except Exception as e:
            logger.error(f"Sheets API Error: {e}")
            return False