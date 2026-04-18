# Setting up Public Access for MCP Server

The Claude MCP connector requires your MCP server to be publicly accessible via HTTP. For local development, use ngrok to expose your localhost server.

## Prerequisites

1. Install ngrok: https://ngrok.com/download
2. Sign up for a free ngrok account
3. Configure ngrok with your authtoken: `ngrok config add-authtoken YOUR_TOKEN`

## Step-by-Step Setup

### 1. Start the MCP Server

```bash
python server.py
```

The server will start on `http://localhost:8000/sse`

### 2. Expose to Internet with ngrok

In a new terminal:

```bash
ngrok http 8000
```

### 3. Get Your Public URL

ngrok will display a forwarding URL like:
```
Forwarding  https://abc123-def456.ngrok-free.app -> http://localhost:8000
```

Your MCP server URL for the Claude client is:
```
https://abc123-def456.ngrok-free.app/sse
```

### 4. Update the Client Script

Edit `claude_client.py` and replace:
```python
MCP_SERVER_URL = "https://your-public-url.ngrok.io/sse"
```

with your actual ngrok URL:
```python
MCP_SERVER_URL = "https://abc123-def456.ngrok-free.app/sse"
```

### 5. Run the Client

```bash
python claude_client.py
```

## Important Notes

- The free ngrok tier generates a new URL each time you restart ngrok
- Paid ngrok plans allow reserved domains that don't change
- For production, deploy your MCP server to a proper hosting service
- The MCP connector does not support local stdio servers directly - they must be HTTP-accessible

## Alternative: Deploy to a Cloud Service

For production use, deploy your MCP server to:
- Railway
- Render
- Fly.io
- Any service that supports Python HTTP servers

Make sure the server is accessible at an `https://` URL.
