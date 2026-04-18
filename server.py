from fastmcp import FastMCP

mcp = FastMCP("HelloMCP")

@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name. """
    return f"Hello, {name}!"

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

@mcp.resource("config://app")
def get_config() -> str:
    """Return application configuration."""
    return '{"version": "1.0.0", "name": "HelloMCP"}'

@mcp.prompt
def greeting_prompt(name: str) -> str:
    """Create a greeting prompt for the user."""
    return f"Please greet {name} warmly and ask how you can help them today."

if __name__ == "__main__":
    mcp.run(transport="sse")