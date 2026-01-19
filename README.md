# MCP Gmail Server 📧

An MCP (Model Context Protocol) server that enables AI assistants like Claude to read unread emails from Gmail and create draft replies with proper conversation threading.

![MCP](https://img.shields.io/badge/MCP-Compatible-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Read Unread Emails**: Fetch unread messages with full details (sender, subject, body, thread ID)
- **Create Draft Replies**: Generate properly threaded draft responses
- **OAuth 2.0 Authentication**: Secure Gmail API access
- **Claude Desktop Integration**: Seamless integration with Claude Desktop via MCP
- **Conversation Threading**: Maintains email thread continuity

## 🎯 What This Server Does

This MCP server exposes two powerful tools to AI assistants:

1. **`get_unread_emails`**: Retrieves unread emails from your Gmail account
2. **`create_draft_reply`**: Creates draft replies that maintain proper email threading

When integrated with Claude Desktop, you can simply ask Claude to "check my emails" or "draft a reply to [person]" and it will handle the Gmail API interactions automatically.

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Gmail account** with API access
- **Google Cloud project** with Gmail API enabled
- **Claude Desktop** application

## 🚀 Gmail API Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "New Project" and give it a name (e.g., "MCP Gmail Server")
3. Select your new project

### Step 2: Enable Gmail API

1. Navigate to **APIs & Services** → **Library**
2. Search for "Gmail API"
3. Click **Enable**

### Step 3: Configure OAuth 2.0

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External** (for personal use)
   - App name: "MCP Gmail Server" (or your choice)
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Add the following:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.compose`
4. Continue and create the OAuth client ID:
   - Application type: **Desktop app**
   - Name: "MCP Gmail Desktop"
5. **Download** the credentials JSON file
6. Save it as `config/credentials.json` in your project directory

### Step 4: Add Test Users (Development Mode)

If your app is in development mode:
1. Go to **OAuth consent screen**
2. Under **Test users**, add your Gmail address
3. Click **Save**

## 💻 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd MLI
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Credentials

1. Create the `config` directory if it doesn't exist:
   ```bash
   mkdir config
   ```

2. Place your `credentials.json` file (from Gmail API setup) in the `config` folder

3. Copy environment template:
   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env      # macOS/Linux
   ```

### 5. Initial Authentication

Run the Gmail client once to complete OAuth flow:

```bash
python -m src.gmail_client
```

This will:
- Open a browser window for Gmail authentication
- Ask you to authorize the application
- Save the token to `config/token.json`

## ⚙️ Claude Desktop Configuration

### 1. Locate Claude Desktop Config

The config file location depends on your OS:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Update Configuration

Add the MCP server to your Claude Desktop config:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": [
        "-m",
        "src.server"
      ],
      "cwd": "C:\\Users\\Home\\Downloads\\MLI",
      "env": {
        "CREDENTIALS_PATH": "config/credentials.json",
        "TOKEN_PATH": "config/token.json"
      }
    }
  }
}
```

**Important**: Update the `cwd` path to your actual project directory.

### 3. Restart Claude Desktop

Completely quit and restart Claude Desktop for the changes to take effect.

## 📖 Usage

Once configured, you can interact with your Gmail through Claude Desktop using natural language:

### Example Prompts

**Check unread emails:**
```
Can you check my unread emails?
```

**Get specific number of emails:**
```
Show me my 5 most recent unread emails
```

**Draft a reply:**
```
Draft a professional reply to the email from John about the meeting, 
saying I'm available next Tuesday at 2pm
```

**Batch processing:**
```
Check my unread emails and draft polite acknowledgment replies for all of them
```

See [`examples/prompts.md`](examples/prompts.md) for more examples.

## 🏗️ Architecture

### Project Structure

```
mcp-gmail-server/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── gmail_client.py    # Gmail API wrapper
│   └── tools.py           # Tool implementations
├── config/
│   ├── credentials.json   # OAuth credentials (not committed)
│   └── token.json         # OAuth token (not committed)
├── examples/
│   ├── prompts.md         # Example prompts
│   └── screenshots/       # Demo screenshots
├── requirements.txt
├── .env.example
└── README.md
```

### Components

**`gmail_client.py`**: Handles Gmail API authentication and operations
- OAuth 2.0 flow management
- Fetching unread emails with full details
- Creating draft replies with proper threading
- Error handling and token refresh

**`tools.py`**: Implements MCP tool handlers
- `get_unread_emails`: Async wrapper for fetching emails
- `create_draft_reply`: Async wrapper for draft creation

**`server.py`**: Main MCP server
- Tool registration and schema definition
- JSON-RPC request handling
- stdio transport for Claude Desktop communication

## 🐛 Troubleshooting

### "Credentials file not found"
- Ensure `credentials.json` is in the `config/` directory
- Check the path in your `.env` file

### "Token has expired"
- Delete `config/token.json`
- Run `python -m src.gmail_client` to re-authenticate

### "MCP server not appearing in Claude Desktop"
- Verify `claude_desktop_config.json` syntax is valid
- Check that the `cwd` path is absolute and correct
- Restart Claude Desktop completely
- Check Claude Desktop logs for errors

### "Permission denied" errors
- Ensure you've added your Gmail as a test user in Google Cloud Console
- Verify the required scopes are configured in OAuth consent screen

### Gmail API quota exceeded
- Gmail API has daily quotas for free tier
- Wait 24 hours or request quota increase in Google Cloud Console

## 🎓 Learning Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 🚀 Stretch Goals

Future enhancements to improve reply quality:

- **Email Style Guide Integration**: Pull writing guidelines from Google Docs
- **Reply Templates**: Use pre-defined templates from Notion
- **Knowledge Base Search**: Reference local documentation when drafting
- **Smart Categorization**: Auto-categorize emails by topic/urgency
- **Multi-account Support**: Manage multiple Gmail accounts

## 📝 License

MIT License - feel free to use and modify as needed.

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## ⚠️ Security Notes

- **Never commit** `credentials.json` or `token.json` to version control
- The `.gitignore` file is configured to prevent this
- OAuth tokens are stored locally and encrypted by Google's libraries
- This server runs locally on your machine - no data is sent to external servers

## 📧 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [example prompts](examples/prompts.md)
3. Open an issue on GitHub

---

**Built for the MCP Foundation Project** 🚀
