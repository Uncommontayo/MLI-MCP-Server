# Gmail API Setup Guide

This guide walks you through setting up Gmail API access for the MCP Gmail Server.

## Prerequisites

- A Google account (Gmail)
- Access to [Google Cloud Console](https://console.cloud.google.com)

## Step 1: Create a Google Cloud Project

1. Navigate to [Google Cloud Console](https://console.cloud.google.com)
2. Click on the project dropdown at the top of the page
3. Click **"New Project"**
4. Enter project details:
   - **Project name**: "MCP Gmail Server" (or your preference)
   - **Location**: Leave as default or select your organization
5. Click **"Create"**
6. Wait for the project to be created, then select it

## Step 2: Enable the Gmail API

1. In your new project, go to **APIs & Services** → **Library**
2. Search for "Gmail API"
3. Click on **Gmail API** in the results
4. Click **"Enable"**
5. Wait for the API to be enabled

## Step 3: Configure OAuth Consent Screen

Before creating credentials, you must configure the OAuth consent screen:

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **User Type**:
   - Choose **"External"** (for personal Gmail accounts)
   - Click **"Create"**

3. Fill in the **App information**:
   - **App name**: "MCP Gmail Server"
   - **User support email**: Your Gmail address
   - **App logo**: (optional, can skip)
   
4. Fill in **Developer contact information**:
   - **Email addresses**: Your Gmail address
   
5. Click **"Save and Continue"**

6. **Add Scopes**:
   - Click **"Add or Remove Scopes"**
   - Search and select:
     - `https://www.googleapis.com/auth/gmail.readonly` - View your email messages
     - `https://www.googleapis.com/auth/gmail.compose` - Manage drafts and send emails
   - Click **"Update"**
   - Click **"Save and Continue"**

7. **Test users**:
   - Click **"Add Users"**
   - Enter your Gmail address
   - Click **"Add"**
   - Click **"Save and Continue"**

8. **Summary**:
   - Review your settings
   - Click **"Back to Dashboard"**

## Step 4: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** at the top
3. Select **"OAuth client ID"**
4. Choose application type:
   - **Application type**: Desktop app
   - **Name**: "MCP Gmail Desktop Client"
5. Click **"Create"**

6. A dialog will appear with your credentials:
   - Click **"Download JSON"**
   - Save this file securely

## Step 5: Set Up Project Credentials

1. Rename the downloaded file to `credentials.json`
2. Move it to your project's `config/` directory:
   ```
   MLI/
   └── config/
       └── credentials.json  ← Place file here
   ```

3. Verify the file structure:
   ```json
   {
     "installed": {
       "client_id": "...",
       "project_id": "...",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       ...
     }
   }
   ```

## Step 6: First-time Authentication

1. Make sure you've installed dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Gmail client to complete OAuth flow:
   ```bash
   python -m src.gmail_client
   ```

3. This will:
   - Open your default web browser
   - Show a Google sign-in page
   - Ask you to select your Google account
   - Display a warning: "Google hasn't verified this app"
     - Click **"Advanced"**
     - Click **"Go to MCP Gmail Server (unsafe)"**
   - Show the permissions the app is requesting
   - Click **"Allow"**

4. After authorization:
   - The browser will show "The authentication flow has completed"
   - A `token.json` file will be created in `config/`
   - You can close the browser

## Step 7: Verify Setup

Check that both files exist:

```
MLI/
└── config/
    ├── credentials.json  ✓
    └── token.json        ✓ (created after first auth)
```

## Troubleshooting

### "Access blocked: This app's request is invalid"

**Solution**: Make sure you added your Gmail address as a test user in the OAuth consent screen.

### "The app is blocked from accessing this account"

**Solutions**:
1. Verify you're signing in with the same Gmail account you added as a test user
2. Check that the required scopes are added to the OAuth consent screen
3. Try deleting and recreating the OAuth credentials

### "redirect_uri_mismatch"

**Solution**: 
- Make sure you selected "Desktop app" as the application type
- Don't modify the redirect URIs manually

### Token expiration

The `token.json` file will automatically refresh. If you get authentication errors:
1. Delete `config/token.json`
2. Run `python -m src.gmail_client` again to re-authenticate

### "Application is running in test mode"

This is normal for development. Your app will only work for users you add to the test users list. To publish the app for broader use:
1. Complete the OAuth consent screen verification process
2. This requires additional steps and Google's review
3. For personal use, test mode is sufficient

## Security Best Practices

✅ **DO:**
- Keep `credentials.json` and `token.json` private
- Add them to `.gitignore` (already configured)
- Use environment variables for paths
- Only add trusted test users

❌ **DON'T:**
- Commit credentials to version control
- Share your OAuth credentials publicly
- Use the same credentials for production apps
- Add unknown users to your test users list

## API Quotas

Gmail API has usage quotas:
- **Free tier**: 1 billion quota units/day
- **Per-user rate limit**: 250 quota units/user/second

For this project's typical usage (reading emails and creating drafts), you're unlikely to hit these limits during normal testing.

To check your usage:
1. Go to **APIs & Services** → **Dashboard**
2. Click on **Gmail API**
3. View the **Metrics** tab

## Next Steps

After completing this setup:
1. ✅ Configure Claude Desktop (`claude_desktop_config.json`)
2. ✅ Test the MCP server with Claude
3. ✅ Try the example prompts in `examples/prompts.md`

---

**Need Help?**
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
