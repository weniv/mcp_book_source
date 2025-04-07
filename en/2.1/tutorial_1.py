from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="tutorial_1")


@mcp.tool()
def echo(message: str) -> str:
    """
    A tool that returns the input message as is.
    """
    return message + " was the message entered. Can't help but print it! hello world!"


# Run server
if __name__ == "__main__":
    mcp.run()
