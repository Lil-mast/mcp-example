# mcp-example

A simple MCP (Model Context Protocol) server built with FastMCP, demonstrating how to expose custom tools to AI assistants.

## What This Repo Is About

This project provides a minimal example of creating an MCP server using the `fastmcp` library. It exposes a single tool (`greet`) that AI assistants can call to generate personalized greetings.

The MCP protocol allows AI assistants to interact with external tools and data sources in a standardized way.

## Requirements

- Python 3.10+
- `uv` - A fast Python package manager and runner
- `fastmcp` library

## Installation

### Install uv (if you don't have it)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup the Project

```bash
# Create a virtual environment
uv venv

# Install dependencies
uv pip install fastmcp
```

## How to Run the Server

### Development Mode with MCP Inspector

Use the built-in MCP Inspector to test your server:

```bash
uv run fastmcp dev inspector mcp.py
```

This will start the MCP Inspector UI where you can interact with your tools:

![MCP Inspector](mcp-inspector.png)

### Production Mode (SSE transport)

```bash
uv run mcp.py --transport sse --port 8000
```

## Available Tools

- **`greet(name: str)`** - Returns a personalized greeting message
- **`calculate(expression: str)`** - Evaluates a mathematical expression (e.g., "2 + 2 * 3")
- **`get_current_time()`** - Returns the current date and time

## Available Resources

- **`config://app`** - Returns the application configuration (version, name)

## Available Prompts

- **`greeting_prompt(name: str)`** - Creates a warm greeting prompt for the user
