import logging
from googleapiclient.discovery import build
import config

logger = logging.getLogger(__name__)

class GmailService:
    def __init__(self, creds):
        self.service = build('gmail', 'v1', credentials=creds)

    def get_unread_emails(self):
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                q='in:inbox',
                maxResults=config.MAX_RESULTS
            ).execute()
            messages = results.get('messages', [])
            return messages 
        except Exception as e:
            logger.error(f"Gmail API Error: {e}")
            return []

    def get_email_details(self, msg_id):
        try:
            return self.service.users().messages().get(
                userId='me', id=msg_id, format='full'
            ).execute()
        except Exception as e:
            logger.error(f"Failed to get details for {msg_id}: {e}")
            return None

    def mark_as_read(self, msg_id):
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            logger.info(f"Marked {msg_id} as read")
            return True
        except Exception as e:
            logger.error(f"Failed to mark read {msg_id}: {e}")
            return False