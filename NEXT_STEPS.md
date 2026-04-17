# Next Steps

Now that you have a basic MCP server running, here are some ways to expand and improve it:

## Add More Tools

Extend your MCP server with additional capabilities:

```python
@mcp.tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@mcp.tool
def get_current_time() -> str:
    """Return the current time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

## Add Resources

Expose data sources as MCP resources:

```python
@mcp.resource("config://app")
def get_config() -> str:
    """Return application configuration."""
    return "{\"version\": \"1.0.0\", \"name\": \"HelloMCP\"}"
```

## Add Prompts

Create reusable prompt templates:

```python
@mcp.prompt
def greeting_prompt(name: str) -> str:
    """Create a greeting prompt for the user."""
    return f"Please greet {name} warmly and ask how you can help them today."
```

## Connect to Claude Desktop

1. Install Claude Desktop
2. Add your MCP server to Claude's configuration:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "python",
      "args": ["/path/to/mcp-example/mcp.py"]
    }
  }
}
```

## Deploy as a Remote Server

For production use, deploy your MCP server with SSE transport:

```bash
# Run with SSE transport
python mcp.py --transport sse --host 0.0.0.0 --port 8000
```

Consider containerizing with Docker for easier deployment.

## Add Authentication

For production servers, implement authentication:

```python
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

middleware = [Middleware(AuthenticationMiddleware, backend=YourAuthBackend())]
mcp = FastMCP("HelloMCP", middleware=middleware)
```

## Explore Advanced Features

- **Streaming responses** - For long-running operations
- **Progress reporting** - Keep clients informed of operation status
- **Image content** - Return images as base64-encoded data
- **Tool annotations** - Add metadata to tools for better discoverability

## Documentation

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
