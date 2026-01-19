# Gmail MCP Server 📧

A high-performance Model Context Protocol (MCP) server that enables AI assistants to interact with Gmail securely.

![MCP](https://img.shields.io/badge/MCP-Compatible-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Smart Email Retrieval**: Fetch unread messages with rich metadata.
- **Thread-Aware Drafting**: Create replies that maintain conversation context.
- **Secure Authentication**: Robust OAuth 2.0 implementation with token management.
- **Enterprise Ready**: Structured for scalability and maintainability.

## 🏗️ Architecture

### System Data Flow

```mermaid
graph TD
    User([👤 User]) <-->|Natural Language| Claude([🤖 Claude Desktop])
    
    subgraph "MCP Server (Local Machine)"
        Claude <-->|JSON-RPC (stdio)| Main[src/main.py]
        Main -->|Dispatch| Handler[src/handlers.py]
        Handler -->|Call| Client[src/client.py]
    end
    
    Client <-->|HTTPS / OAuth 2.0| Gmail([☁️ Google Gmail API])
    
    style User fill:#f9f,stroke:#333
    style Claude fill:#e1f5fe,stroke:#01579b
    style Gmail fill:#fce4ec,stroke:#880e4f
```

The project follows standard engineering practices:

```
MLI/
├── src/
│   ├── main.py          # Application Entry Point
│   ├── client.py        # Gmail API Client
│   └── handlers.py      # Request Handlers
├── config/              # Configuration & Credentials
├── tests/               # Unit Tests
└── requirements.txt     # Dependencies
```

## 🚀 Quick Start

### 1. Prerequisite
- Python 3.8+
- Google Cloud Project with Gmail API enabled

### 2. Installation

```bash
# Clone and setup environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Place your Google Cloud `credentials.json` in `config/`.
2. Copy the environment config:
   ```bash
   copy .env.example .env
   ```

### 4. Claude Integration

Add to your **Claude Desktop** config (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "gmail": {
      "command": "C:\\Path\\To\\MLI\\.venv\\Scripts\\python.exe",
      "args": ["-m", "src.main"],
      "cwd": "C:\\Path\\To\\MLI",
      "env": {
        "CREDENTIALS_PATH": "config/credentials.json",
        "TOKEN_PATH": "config/token.json"
      }
    }
  }
}
```

## 🛠️ Usage

**Check Emails:**
> "Check my unread emails"

**Draft Reply:**
> "Draft a reply to the email from [Name]"

## 🛡️ Security

- Credentials are never committed to version control.
- Tokens are stored locally in `config/`.
- Communication happens directly between your machine and Google API.

