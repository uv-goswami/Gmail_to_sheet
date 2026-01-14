import base64
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class EmailParser:
    @staticmethod
    def get_header(headers, name):
        if not headers:
            return "Unknown"
        for h in headers:
            if h['name'].lower() == name.lower():
                return h['value']
        return "Unknown"

    @staticmethod
    def clean_body(payload):
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode()
                elif 'parts' in part: 
                    body += EmailParser.clean_body(part)
        
        elif 'body' in payload:
             data = payload['body'].get('data')
             if data:
                body = base64.urlsafe_b64decode(data).decode()
        
        if not body.strip() and 'parts' in payload:
             for part in payload['parts']:
                if part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        try:
                            html = base64.urlsafe_b64decode(data).decode()
                            soup = BeautifulSoup(html, 'lxml')
                            body = soup.get_text(separator=' ')
                        except Exception as e:
                            logger.warning(f"Failed to parse HTML body: {e}")

        return body.strip()

    @staticmethod
    def parse(msg_obj):
        payload = msg_obj['payload']
        headers = payload.get('headers', [])

        sender = EmailParser.get_header(headers, 'From')
        subject = EmailParser.get_header(headers, 'Subject')
        date = EmailParser.get_header(headers, 'Date')
        
        content = EmailParser.clean_body(payload)

        if len(content) > 500:
            content = content[:500] + "..."

        return {
            'id': msg_obj['id'],
            'from': sender,
            'subject': subject,
            'date': date,
            'content': content
        }