"""MCP server for Gmail integration."""

import asyncio
import logging
import os
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from .tools import initialize_gmail_client, get_unread_emails, create_draft_reply

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server
app = Server("gmail-assistant")

# Initialize Gmail client
credentials_path = os.getenv('CREDENTIALS_PATH', 'config/credentials.json')
token_path = os.getenv('TOKEN_PATH', 'config/token.json')

logger.info(f"Initializing Gmail client with credentials: {credentials_path}")
initialize_gmail_client(credentials_path, token_path)


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_unread_emails",
            description="Fetch unread emails from Gmail. Returns sender, subject, body snippet, and thread/message IDs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of unread emails to retrieve (default: 10)",
                        "default": 10
                    }
                }
            }
        ),
        types.Tool(
            name="create_draft_reply",
            description="Create a draft reply to an email. The draft will be properly threaded with the original conversation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "thread_id": {
                        "type": "string",
                        "description": "Thread ID from the original email (required)"
                    },
                    "to": {
                        "type": "string",
                        "description": "Recipient email address (required)"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject, typically 'Re: <original subject>' (required)"
                    },
                    "body": {
                        "type": "string",
                        "description": "The reply message body (required)"
                    },
                    "in_reply_to": {
                        "type": "string",
                        "description": "Original message ID for proper threading (optional)"
                    }
                },
                "required": ["thread_id", "to", "subject", "body"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    try:
        if name == "get_unread_emails":
            result = await get_unread_emails(arguments)
        elif name == "create_draft_reply":
            result = await create_draft_reply(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        # Format result as text content
        import json
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        import json
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
        )]


async def main():
    """Run the MCP server."""
    logger.info("Starting Gmail MCP server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
