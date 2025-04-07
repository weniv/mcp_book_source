from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="server")

# Existing functions (file and Excel related functions)
# Add web crawling related function here


@mcp.tool()
def crawl_url_return_book_name(url: str) -> str:
    """
    Receives a URL and crawls it to return book titles. Each data item is connected by a comma. Therefore, when showing to the user, please display with line breaks instead of commas.

    Parameters
    ----------
    url : str
        URL of the web page to crawl

    Returns
    -------
    str
        Comma-separated list of book titles
    """
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    result = []

    for book in soup.select(".book_name"):
        result.append(book.text.strip())

    return ", ".join(result)
