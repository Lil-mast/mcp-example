"""
Advanced Claude MCP Connector Client

This script demonstrates various MCP toolset configuration patterns:
1. Enable all tools (default)
2. Allowlist - enable only specific tools
3. Denylist - disable specific tools
4. Per-tool configuration with defer_loading
"""

import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MCP_SERVER_URL = "https://168b-41-90-140-53.ngrok-free.app/sse" 

# =============================================================================
# Pattern 1: Enable all tools 
# =============================================================================
response_all_tools = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What tools do you have?"}],
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
            "mcp_server_name": "hellomcp-server"
            # No default_config or configs - all tools enabled
        }
    ],
    betas=["mcp-client-2025-11-20"],
)
print("Pattern 1 - All tools:", response_all_tools)


# =============================================================================
# Pattern 2: Allowlist - enable only greet and calculate
# =============================================================================
response_allowlist = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What tools do you have?"}],
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
            "default_config": {
                "enabled": False  # Disable all by default
            },
            "configs": {
                "greet": {"enabled": True},
                "calculate": {"enabled": True}
            }
        }
    ],
    betas=["mcp-client-2025-11-20"],
)
print("Pattern 2 - Allowlist:", response_allowlist)


# =============================================================================
# Pattern 3: Denylist - disable only get_current_time
# =============================================================================
response_denylist = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What tools do you have?"}],
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
            "configs": {
                "get_current_time": {"enabled": False}  # Disable this one
            }
        }
    ],
    betas=["mcp-client-2025-11-20"],
)
print("Pattern 3 - Denylist:", response_denylist)


# =============================================================================
# Pattern 4: Mixed - allowlist with per-tool defer_loading config
# =============================================================================
response_mixed = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What tools do you have?"}],
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
            "default_config": {
                "enabled": False,
                "defer_loading": True  # Don't send descriptions initially
            },
            "configs": {
                "greet": {
                    "enabled": True,
                    "defer_loading": False  # Send description for this tool
                },
                "calculate": {
                    "enabled": True
                    # defer_loading: true (inherited from default_config)
                }
            }
        }
    ],
    betas=["mcp-client-2025-11-20"],
)
print("Pattern 4 - Mixed:", response_mixed)


# =============================================================================
# Multiple MCP Servers Example
# =============================================================================
# You can connect to multiple MCP servers in a single request
response_multi = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Use tools from both servers"}],
    mcp_servers=[
        {
            "type": "url",
            "url": MCP_SERVER_URL,
            "name": "hellomcp-server",
        },
        {
            "type": "url",
            "url": "https://another-mcp-server.example.com/sse",
            "name": "another-mcp",
            # "authorization_token": "TOKEN_FOR_ANOTHER_SERVER"
        }
    ],
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "hellomcp-server"
        },
        {
            "type": "mcp_toolset",
            "mcp_server_name": "another-mcp",
            "default_config": {"defer_loading": True}
        }
    ],
    betas=["mcp-client-2025-11-20"],
)
print("Multiple servers:", response_multi)
