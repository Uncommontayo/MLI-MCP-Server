"""MCP tools for Gmail operations."""

import logging
from typing import Any, Dict
from .client import GmailClient

logger = logging.getLogger(__name__)

# Global Gmail client instance
gmail_client: GmailClient = None


def initialize_gmail_client(credentials_path: str = 'config/credentials.json',
                            token_path: str = 'config/token.json'):
    """Initialize the Gmail client.
    
    Args:
        credentials_path: Path to OAuth credentials
        token_path: Path to OAuth token
    """
    global gmail_client
    gmail_client = GmailClient(credentials_path, token_path)
    logger.info("Gmail client initialized")


async def get_unread_emails(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Tool: Get unread emails from Gmail.
    
    Args:
        arguments: Dictionary with optional 'max_results' parameter
        
    Returns:
        Dictionary with emails array or error
    """
    try:
        max_results = arguments.get('max_results', 10)
        
        if not gmail_client:
            raise Exception("Gmail client not initialized")
        
        emails = gmail_client.get_unread_emails(max_results=max_results)
        
        return {
            'success': True,
            'count': len(emails),
            'emails': emails
        }
        
    except Exception as e:
        logger.error(f"Error in get_unread_emails: {e}")
        return {
            'success': False,
            'error': str(e),
            'emails': []
        }


async def create_draft_reply(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Tool: Create a draft reply to an email.
    
    Args:
        arguments: Dictionary with required fields:
            - thread_id: Thread ID to reply to
            - to: Recipient email address
            - subject: Reply subject
            - body: Reply message body
            - in_reply_to: (optional) Original message ID
            
    Returns:
        Dictionary with draft details or error
    """
    try:
        # Validate required parameters
        required_params = ['thread_id', 'to', 'subject', 'body']
        for param in required_params:
            if param not in arguments:
                raise ValueError(f"Missing required parameter: {param}")
        
        if not gmail_client:
            raise Exception("Gmail client not initialized")
        
        result = gmail_client.create_draft_reply(
            thread_id=arguments['thread_id'],
            to=arguments['to'],
            subject=arguments['subject'],
            body=arguments['body'],
            in_reply_to=arguments.get('in_reply_to')
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in create_draft_reply: {e}")
        return {
            'success': False,
            'error': str(e)
        }
