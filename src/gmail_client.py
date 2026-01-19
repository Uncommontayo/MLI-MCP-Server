"""Gmail API client for reading emails and creating drafts."""

import os
import base64
import logging
from email.mime.text import MIMEText
from typing import List, Dict, Optional
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose'
]


class GmailClient:
    """Client for interacting with Gmail API."""
    
    def __init__(self, credentials_path: str = 'config/credentials.json', 
                 token_path: str = 'config/token.json'):
        """Initialize Gmail client.
        
        Args:
            credentials_path: Path to OAuth credentials JSON file
            token_path: Path to store/load OAuth token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0."""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
                logger.info("Loaded existing credentials from token file")
            except Exception as e:
                logger.warning(f"Failed to load token: {e}")
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed expired credentials")
                except Exception as e:
                    logger.error(f"Failed to refresh token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {self.credentials_path}. "
                        "Please download OAuth credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.info("Obtained new credentials via OAuth flow")
            
            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
                logger.info(f"Saved credentials to {self.token_path}")
        
        # Build Gmail service
        self.service = build('gmail', 'v1', credentials=creds)
        logger.info("Gmail API service initialized successfully")
    
    def get_unread_emails(self, max_results: int = 10) -> List[Dict]:
        """Fetch unread emails from Gmail.
        
        Args:
            max_results: Maximum number of emails to retrieve
            
        Returns:
            List of email dictionaries with sender, subject, body, etc.
        """
        try:
            # Query for unread messages
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                logger.info("No unread messages found")
                return []
            
            emails = []
            for msg in messages:
                email_data = self._get_message_details(msg['id'])
                if email_data:
                    emails.append(email_data)
            
            logger.info(f"Retrieved {len(emails)} unread emails")
            return emails
            
        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            raise Exception(f"Failed to fetch unread emails: {error}")
    
    def _get_message_details(self, msg_id: str) -> Optional[Dict]:
        """Get detailed information for a specific message.
        
        Args:
            msg_id: Gmail message ID
            
        Returns:
            Dictionary with email details or None if failed
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extract header information
            subject = self._get_header(headers, 'Subject')
            sender = self._get_header(headers, 'From')
            date = self._get_header(headers, 'Date')
            message_id = self._get_header(headers, 'Message-ID')
            
            # Get email body
            body = self._get_message_body(message['payload'])
            snippet = message.get('snippet', '')
            
            return {
                'email_id': msg_id,
                'thread_id': message['threadId'],
                'message_id': message_id,
                'sender': sender,
                'subject': subject,
                'snippet': snippet,
                'body': body,
                'date': date,
                'labels': message.get('labelIds', [])
            }
            
        except HttpError as error:
            logger.error(f"Failed to get message {msg_id}: {error}")
            return None
    
    def _get_header(self, headers: List[Dict], name: str) -> str:
        """Extract header value by name.
        
        Args:
            headers: List of email headers
            name: Header name to find
            
        Returns:
            Header value or empty string if not found
        """
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''
    
    def _get_message_body(self, payload: Dict) -> str:
        """Extract email body from message payload.
        
        Args:
            payload: Message payload from Gmail API
            
        Returns:
            Email body text
        """
        body = ''
        
        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
        else:
            # Simple message
            if 'data' in payload['body']:
                body = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8')
        
        return body
    
    def create_draft_reply(self, thread_id: str, to: str, subject: str, 
                          body: str, in_reply_to: Optional[str] = None) -> Dict:
        """Create a draft reply to an email.
        
        Args:
            thread_id: Thread ID to reply to
            to: Recipient email address
            subject: Email subject (typically "Re: original subject")
            body: Reply message body
            in_reply_to: Original message ID for proper threading
            
        Returns:
            Dictionary with draft details
        """
        try:
            # Create message
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            # Add threading headers for proper conversation grouping
            if in_reply_to:
                message['In-Reply-To'] = in_reply_to
                message['References'] = in_reply_to
            
            # Encode message
            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')
            
            # Create draft
            draft_body = {
                'message': {
                    'raw': encoded_message,
                    'threadId': thread_id
                }
            }
            
            draft = self.service.users().drafts().create(
                userId='me',
                body=draft_body
            ).execute()
            
            logger.info(f"Created draft reply in thread {thread_id}")
            
            return {
                'draft_id': draft['id'],
                'message_id': draft['message']['id'],
                'thread_id': draft['message']['threadId'],
                'success': True
            }
            
        except HttpError as error:
            logger.error(f"Failed to create draft: {error}")
            raise Exception(f"Failed to create draft reply: {error}")


# Test function for standalone execution
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Gmail Client...")
    client = GmailClient()
    
    print("\nFetching unread emails...")
    emails = client.get_unread_emails(max_results=5)
    
    for i, email in enumerate(emails, 1):
        print(f"\n--- Email {i} ---")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"Snippet: {email['snippet'][:100]}...")
        print(f"Thread ID: {email['thread_id']}")
