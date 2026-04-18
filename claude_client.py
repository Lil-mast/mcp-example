"""
Claude MCP Connector Client

This script demonstrates how to connect to the MCP server using Claude's
Messages API with the MCP connector feature (beta header: mcp-client-2025-11-20).

Prerequisites:
1. Run the MCP server first: python server.py
2. Set ANTHROPIC_API_KEY environment variable
3. The server will be accessible at http://localhost:8000/sse
"""

import os
import anthropic

# Get API key from environment
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Please set the ANTHROPIC_API_KEY environment variable")

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=api_key)

# The MCP server must be publicly accessible. For local testing, you can use:
# - ngrok to expose localhost:8000 to the internet
# - Or deploy the server to a public URL
#
# Example with ngrok:
# 1. Run: python server.py (starts on localhost:8000)
# 2. Run: ngrok http 8000 (get public URL like https://abc123.ngrok.io)
# 3. Use the ngrok URL below

MCP_SERVER_URL = "https://168b-41-90-140-53.ngrok-free.app/sse"  # Replace with your public URL

# Create a message with MCP server connection
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "What tools do you have available?"}
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": MCP_SERVER_URL,
            "name": "hellomcp-server",
            # "authorization_token": "YOUR_TOKEN"  # Only if your server requires auth
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "hellomcp-server"
            # Enable all tools with default config
        }
    ],
    betas=["mcp-client-2025-11-20"],  # Required beta header
)

print("Response from Claude:")
print(response)

# Example: Use a specific tool (greet)
response2 = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Greet me! My name is Alice."}
    ],
    mcp_servers=[
        {
            "type": "url",
            "url": MCP_SERVER_URL,
            "name": "hellomcp-server",
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "hellomcp-server",
            # Allowlist example: only enable greet and calculate
            # "default_config": {"enabled": False},
            # "configs": {
            #     "greet": {"enabled": True},
            #     "calculate": {"enabled": True},
            # }
        }
    ],
    betas=["mcp-client-2025-11-20"],
)

print("\nResponse with tool use:")
print(response2)
