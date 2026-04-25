# Deploying Your MCP Server

Your MCP server uses **SSE (Server-Sent Events)** transport, making it deployable to any cloud platform that supports Python HTTP servers.

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

1. **Push to GitHub** (if not already)
2. **Go to [railway.app](https://railway.app)** → New Project → Deploy from GitHub repo
3. **Set environment variables** (if needed):
   - `PORT=8000` (Railway sets this automatically)
4. **Deploy** — Railway provides an HTTPS URL automatically

**Railway specifics:**
- Free tier: $5/month credit (good for testing)
- Auto HTTPS
- Auto restart on crashes

### Option 2: Render

1. **Push to GitHub**
2. **Go to [render.com](https://render.com)** → New Web Service
3. **Connect your repo**
4. **Configure:**
   - **Runtime:** Python 3
   - **Build Command:** `pip install uv && uv pip install -e .`
   - **Start Command:** `uv run server.py`
5. **Set environment:** `PORT=8000`
6. **Deploy** — Get `https://your-service.onrender.com`

**Render specifics:**
- Free tier: Web services sleep after 15 min inactivity
- 512 MB RAM, 0.1 CPU
- HTTPS automatically

### Option 3: Fly.io

1. **Install flyctl:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and launch:**
   ```bash
   fly auth login
   fly launch --name my-mcp-server --region ord
   ```

3. **Deploy:**
   ```bash
   fly deploy
   ```

**Fly.io specifics:**
- Free tier: 3 small VMs (256MB RAM)
- Auto HTTPS with custom domains
- Close to bare metal performance

### Option 4: Docker (Any Platform)

Build and run locally or deploy to any container service:

```bash
# Build
docker build -t mcp-server .

# Run locally
docker run -p 8000:8000 mcp-server

# Or deploy to AWS/GCP/Azure with container services
```

## Post-Deployment: Update Your Clients

Once deployed, you'll get a public HTTPS URL like:
```
https://my-mcp-server.up.railway.app/sse
https://my-mcp-server.onrender.com/sse
https://my-mcp-server.fly.dev/sse
```

### Update Claude Desktop Config

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hello-mcp": {
      "url": "https://your-deployed-url.com/sse"
    }
  }
}
```

### Update Python Client

In `claude_client.py` or `claude_client_advanced.py`:

```python
MCP_SERVER_URL = "https://your-deployed-url.com/sse"
```

## Verifying Your Deployment

Test the SSE endpoint:

```bash
curl -N https://your-deployed-url.com/sse
```

Expected output:
```
event: endpoint
data: /messages/?session_id=xxxxx
```

Then test a tool call:

```bash
curl -X POST "https://your-deployed-url.com/messages/?session_id=test" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Environment Variables

Add these to your deployment platform if needed:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 8000 |
| `HOST` | Bind address | 0.0.0.0 |
| `LOG_LEVEL` | Logging level | INFO |

## Security Considerations

1. **Authentication** (optional but recommended):
   Add a simple token check to your server:
   ```python
   # In server.py, add before mcp.run()
   import os
   AUTH_TOKEN = os.environ.get("MCP_AUTH_TOKEN")
   ```

2. **Rate limiting**: Most platforms handle this, or add:
   ```bash
   uv pip install slowapi
   ```

3. **HTTPS**: All recommended platforms provide this automatically

## Troubleshooting Deployments

| Issue | Solution |
|-------|----------|
| "Cannot import fastmcp" | Check pyproject.toml is in repo root |
| Server starts then crashes | Check PORT env var is set |
| Connection refused | Ensure server binds to `0.0.0.0` not `127.0.0.1` |
| Tools not appearing | Verify `/sse` endpoint returns 200 |

## Cost Comparison

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Railway | $5 credit/mo | $5+ /mo |
| Render | Always free (sleeps) | $7+ /mo |
| Fly.io | 3 VMs, 3GB storage | ~$2-5 /mo |
| AWS/GCP | 12 months free | Variable |

**Recommendation:** Start with **Railway** or **Fly.io** for simplest setup and best free tier experience.
