from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("tutorial_3")


# Prompt extension example
@mcp.prompt()
def prompt_extension(contents: str) -> str:
    """Distinguishes facts from opinions in the prompt."""
    return f"""{contents}

Please respond to this prompt according to the template below.

* Facts:

* Opinions:
"""


# Run server
if __name__ == "__main__":
    mcp.run()
