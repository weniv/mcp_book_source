from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="server")


@mcp.tool()
def create_folder(folder_name: str) -> str:
    """
    Creates a folder under c:/test/

    Parameters
    ----------
    folder_name : str
        Name of the folder to create

    Returns
    -------
    str
        Creation result message
    """
    import os

    folder_path = os.path.join("c:/test", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"Folder '{folder_name}' has been created."
    else:
        return f"Folder '{folder_name}' already exists."


@mcp.tool()
def delete_folder(folder_name: str) -> str:
    """
    Deletes a folder under c:/test/

    Parameters
    ----------
    folder_name : str
        Name of the folder to delete

    Returns
    -------
    str
        Deletion result message
    """
    import os

    folder_path = os.path.join("c:/test", folder_name)
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
        return f"Folder '{folder_name}' has been deleted."
    else:
        return f"Folder '{folder_name}' does not exist."


@mcp.tool()
def list_folders() -> list:
    """
    Returns the list of folders under c:/test/

    Returns
    -------
    list
        List of folders
    """
    import os

    folder_path = "c:/test"
    folders = [
        f
        for f in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, f))
    ]
    return folders


# Run server
if __name__ == "__main__":
    mcp.run()
